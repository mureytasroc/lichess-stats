import re

import chess.pgn
import pymysql


mydb = pymysql.connect(
    host="chess-db.ccwnen4yavww.us-east-1.rds.amazonaws.com",
    user="admin",
    password="aaaaaaaa",
    port=3306,
    db="chesswins",
)


async def read_batch(batch_size):
    all_games = []
    all_moves = []
    for _ in range(batch_size):
        game, moves = read_data()
        all_games.append(game)
        all_moves += moves
    return all_games, all_moves


def read_data():
    c = 0
    with open("/Users/rohangupta/Downloads/lichess_db_standard_rated_2022-03.pgn") as f:
        while c < 1000:
            game = chess.pgn.read_game(f)
            headers = game.headers

            tournament_id = (
                t[0] if (t := re.findall(r"tournament/(.*)\"", headers["Event"])) else None
            )

            lichess_id = re.findall(r"org/(.*)", headers["Site"])[0]

            start_timestamp = headers["UTCDate"].replace(".", "-") + " " + headers["UTCTime"]

            categories = {
                "Bullet",
                "Blitz",
                "Rapid",
                "Classical",
                "Correspondence",
                "UltraBullet",
            }

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

            white_title = headers.get("WhiteTitle", None)
            black_title = headers.get("BlackTitle", None)

            white_rating_diff = (
                int(headers["WhiteRatingDiff"]) if headers.get("WhiteRatingDiff") else None
            )
            black_rating_diff = (
                int(headers["BlackRatingDiff"]) if headers.get("WhiteRatingDiff") else None
            )

            opening_name = headers["Opening"]
            opening_ec0 = headers["ECO"]

            result = headers["Result"]
            termination = (
                headers["Termination"]
                if headers["Termination"] != "Normal"
                else ("Checkmate" if game.end().san()[-1] == "#" else "Resignation")
            )

            moves = []

            while game.next():
                game = game.next()
                moves.append((lichess_id, game.ply(), game.san()))
            c += 1
            yield (
                lichess_id,
                tournament_id,
                start_timestamp,
                category,
                time_control_base,
                time_control_increment,
                white_username,
                black_username,
                white_elo,
                black_elo,
                white_title,
                black_title,
                white_rating_diff,
                black_rating_diff,
                opening_name,
                opening_ec0,
                result,
                termination,
            ), moves


def insert_into_db(game_values, move_values, cur):
    q = """
    INSERT IGNORE INTO `Game` (lichess_id, tournament_id, start_timestamp, category, time_control_base, time_control_increment, white_username, black_username, white_elo, 
    black_elo, white_title, black_title, white_rating_diff, black_rating_diff, opening_name, opening_ec0, result, termination)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(q, game_values)

    q2 = """
    INSERT IGNORE INTO `Moves` (game_id, ply, move_notation)
    VALUES (%s, %s, %s)"""
    cur.executemany(q2, move_values)
    return True


def push_data():
    with mydb.cursor() as cur:
        games, moves = asyncio.wait([read_batch(BATCH_SIZE)])
    try:
        while True:
            insert_into_db(games, moves, cur)
    except StopIteration:
        pass
        mydb.commit()


def pull_data():
    q = """ select Count(*) from Game"""
    with mydb.cursor() as cur:
        cur.execute(q)
        print(cur.fetchall())


pull_data()
