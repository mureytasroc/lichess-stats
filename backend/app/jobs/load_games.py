import argparse
import asyncio
import re
import selectors

import chess.pgn
from tqdm import tqdm

from app.database.connect import get_async_db_connection, get_db_connection
from app.database.util import categories
from app.load_data_helpers.get_games_files import get_games_files
from app.sql.statements import upsert_evaluation, upsert_game, upsert_moves, upsert_time_remaining


parser = argparse.ArgumentParser(description="Load user profiles from https://lichess.org/api.")


parser.add_argument(
    "--queue-limit",
    "-q",
    type=int,
    default=100,
    help=("The max size of the game queue (used for concurrent processing/loading)."),
)

parser.add_argument(
    "--num-consumers",
    "-c",
    type=int,
    default=1,
    help=("The number of game consumer tasks (committing games to the db)."),
)

parser.add_argument(
    "--from-date",
    type=str,
    default=None,
    help=(
        "The date of the earliest game file to get usernames from, "
        "of the form YYYY-MM (defaults to the beginning of lichess's game history)."
    ),
)

parser.add_argument(
    "--to-date",
    type=str,
    default=None,
    help=(
        "The date of the latest game file to get usernames from, "
        "of the form YYYY-MM (defaults to the end of lichess's game history)."
    ),
)

parser.add_argument(
    "--ascending",
    action="store_true",
    help=(
        "Use this flag to load game files in ascending chronological order "
        "(default behavior is to load files in reverse chronological order)."
    ),
)

parser.add_argument(
    "--save-files",
    "-s",
    action="store_true",
    help=(
        "Use this flag to prevent game files from being deleted from the /tmp directory "
        "after being downloaded (to speed up future runs)."
    ),
)

parser.add_argument(
    "--num-workers",
    "-w",
    type=int,
    default=1,
    help=("The number of workers (on different computers) to use."),
)

parser.add_argument(
    "--worker-num",
    "-n",
    type=int,
    default=0,
    help=("The number of this machine's worker, in the range [0..worker_num)."),
)

args = parser.parse_args()


assert args.queue_limit > 0
assert args.num_consumers > 0
assert args.num_workers > 0
assert 0 <= args.worker_num < args.num_workers


def get_existing_game_ids():
    """
    Loads the set of existing game IDs from the Game table of the database.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT lichess_id FROM Game")
            game_ids = {row[0] for row in cursor.fetchall()}
        connection.commit()
    return game_ids


existing_game_ids = get_existing_game_ids()

id_re = re.compile(r"org/(.*)")
tournament_id_re = re.compile(r"tournament/(.*)\"")


async def game_producer(game_file, game_queue):
    i = -1
    while True:
        i += 1
        game = chess.pgn.read_game(game_file)
        if not game:
            break
        headers = game.headers

        lichess_id = id_re.search(headers["Site"]).group(1)
        if lichess_id in existing_game_ids:
            continue

        existing_game_ids.add(lichess_id)
        if i % args.num_workers != args.worker_num:
            continue

        tournament_id_match = tournament_id_re.search(headers["Event"])
        tournament_id = tournament_id_match.group(1) if tournament_id_match else None

        start_timestamp = headers["UTCDate"].replace(".", "-") + " " + headers["UTCTime"]

        category = (categories & set(headers["Event"].split())).pop()

        time_control_base, time_control_increment = (
            list(map(int, headers["TimeControl"].split("+")))
            if headers["TimeControl"] != "-"
            else (None, None)
        )
        white_username = headers["White"]
        black_username = headers["Black"]

        white_elo = int(headers["WhiteElo"])
        black_elo = int(headers["BlackElo"])

        white_title = headers.get("WhiteTitle")
        black_title = headers.get("BlackTitle")

        white_rating_diff = (
            int(headers["WhiteRatingDiff"]) if headers.get("WhiteRatingDiff") else None
        )
        black_rating_diff = (
            int(headers["BlackRatingDiff"]) if headers.get("BlackRatingDiff") else None
        )

        opening_name = headers["Opening"]
        opening_ec0 = headers["ECO"]

        result = headers["Result"]
        if result not in {"1-0", "0-1", "1/2-1/2"}:
            print(f"Unexpected result: '{result}'. Skipping game.")
            continue
        termination = headers["Termination"]

        game_tup = (
            lichess_id,
            start_timestamp,
            tournament_id,
            category,
            time_control_base,
            time_control_increment,
            white_username,
            white_elo,
            white_title,
            black_username,
            black_elo,
            black_title,
            opening_name,
            opening_ec0,
            result,
            termination,
            white_rating_diff,
            black_rating_diff,
        )

        move_nodes = []
        move = game.next()
        while move:
            move_nodes.append(move)
            move = move.next()

        moves = [(lichess_id, move.ply(), move.san()) for move in move_nodes]

        time_remaining = [
            (
                lichess_id,
                move.ply() // 2,
                round(move.clock() * 100),
                move.next() and round(move.next().clock() * 100),
            )
            for move in move_nodes[::2]
            if move.clock() is not None
        ]

        evaluation = []
        for move in move_nodes:
            if not move.eval():
                continue
            relative_eval = move.eval().relative
            score = relative_eval.score()
            forced_mate = relative_eval.mate()
            if score is None and forced_mate is None:
                continue
            evaluation.append(
                (
                    lichess_id,
                    move.ply(),
                    score if forced_mate is not None else None,
                    forced_mate,
                    move.eval_depth(),
                )
            )

        await game_queue.put((game_tup, moves, time_remaining, evaluation))
    await game_queue.put((None,) * 4)


async def game_consumer(queue, pbar):
    pool = await get_async_db_connection()

    async with pool.acquire() as conn:
        while True:
            game, moves, time_remaining, evaluation = await queue.get()
            if game is None:
                break
            async with conn.cursor() as cur:
                await cur.execute(upsert_game, game)
                if moves:
                    await cur.executemany(upsert_moves, moves)
                if time_remaining:
                    await cur.executemany(upsert_time_remaining, time_remaining)
                if evaluation:
                    await cur.executemany(upsert_evaluation, evaluation)
            await conn.commit()
            pbar.update(1)

    pool.close()
    await pool.wait_closed()


async def load_games():
    for game_file_context in get_games_files(
        from_date=args.from_date,
        to_date=args.to_date,
        ascending=args.ascending,
        save_files=args.save_files,
    ):
        with game_file_context() as game_file:
            game_queue = asyncio.Queue(maxsize=args.queue_limit)
            with tqdm() as pbar:
                game_producer_task = asyncio.create_task(game_producer(game_file, game_queue))
                game_consumer_tasks = [
                    asyncio.create_task(game_consumer(game_queue, pbar))
                    for _ in range(args.num_consumers)
                ]

                await asyncio.gather(
                    game_producer_task,
                    *game_consumer_tasks,
                )
                await game_queue.join()


selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
asyncio.run(load_games())
