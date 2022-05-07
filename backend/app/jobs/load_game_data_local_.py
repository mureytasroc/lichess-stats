import re
import chess.pgn
import pymysql

# TODO: Make stuff async

mydb = pymysql.connect(
    host="chess-db.ccwnen4yavww.us-east-1.rds.amazonaws.com",
    user="admin",
    password="aaaaaaaa",
    port=3306,
    db="chesswins",
)


def read_data():
    c = 0
    start_idx = 0  # Offset to prevent dupe reads

    with open("/Users/rohangupta/Downloads/lichess_db_standard_rated_2022-03.pgn") as f:
        for _ in range(start_idx):
            game = chess.pgn.skip_game(f)
        while c < 2000:
            game = chess.pgn.read_game(f)
            headers = game.headers
            flag = 1

            game_ = game

            while game_.next():
                game_ = game_.next()
                if game_.eval():
                    break
                else:
                    flag = 0
                    break

            if not flag:
                continue

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
            opening_eco = headers["ECO"]

            result = headers["Result"]
            termination = (
                headers["Termination"]
                if headers["Termination"] != "Normal"
                else (
                    "Checkmate"
                    if hasattr(game.end(), "san") and game.end().san()[-1] == "#"
                    else "Resignation"
                )
            )

            moves = []
            times = []
            evals = []

            w_time = time_control_base
            b_time = time_control_base

            while game.next():
                game = game.next()
                ply = game.ply()
                if ply % 2 == 1:
                    w_time = int(game.clock())
                if ply % 2 == 0:
                    b_time = int(game.clock())
                moves.append((lichess_id, ply, game.san()))
                times.append((lichess_id, ply, w_time, b_time))

                score = game.eval()
                eval = score.white().score() or score.white().mate() if score else None
                mate_in = score.is_mate() if score else None

                evals.append(
                    (
                        lichess_id,
                        ply,
                        eval / 100 if not mate_in and isinstance(eval, int) else None,
                        eval if mate_in else None,
                    )
                )

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
                opening_eco,
                result,
                termination,
            ), moves, evals, times


def insert_into_db(game_values, move_values, eval_values, time_values, cur):
    q = """
    INSERT IGNORE INTO `Game` (lichess_id, tournament_id, start_timestamp, category, time_control_base, time_control_increment, white_username, black_username, white_elo, 
    black_elo, white_title, black_title, white_rating_diff, black_rating_diff, opening_name, opening_eco, result, termination)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(q, game_values)

    q2 = """
    INSERT IGNORE INTO `GameMove` (game_id, ply, move_notation) VALUES (%s, %s, %s)"""
    cur.executemany(q2, move_values)

    q3 = """
    INSERT IGNORE INTO `Evaluation` (game_id, ply, eval, mate_in) VALUES (%s, %s, %s, %s)"""

    cur.executemany(q3, eval_values)

    q4 = """
    INSERT IGNORE INTO `TimeRemaining` (game_id, move_num, white_hundredths, black_hundredths) VALUES (%s, %s, %s, %s) """

    cur.executemany(q4, time_values)
    return True


def push_data():
    with mydb.cursor() as cur:
        # Batch write, and commit more frequently.
        c = 0
        for output in read_data():
            assert insert_into_db(*output, cur)
            c += 1
            if c % 300 == 0:
                mydb.commit()


def pull_data():
    q = """ select * from Evaluation """
    with mydb.cursor() as cur:
        cur.execute(q)
        print(cur.fetchall())


pull_data()
