from multiprocessing import connection
from statistics import mode
from tokenize import String
from typing import Optional

from fastapi import APIRouter, Path, Query

from app.database.util import GameType
from app.models.games import *
from app.models.profile import CountryDistribution
import pymysql.cursors
from app.database.connect import get_db_connection, get_dict_cursor

router = APIRouter()

dict_cursor = get_dict_cursor(get_db_connection())


@router.get(
    "/date-distribution",
    description="Get the distribution of game dates.",
    response_model=DateDistribution,
)
async def title_distribution():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT DATE_FORMAT(DATE(start_timestamp), '%Y-%m-%d') as start_date, COUNT(*) as count
            FROM Game
            GROUP BY DATE(start_timestamp)
            """
        )
        result = cur.fetchall()
    return {"dates": result}


@router.get(
    "/CastlingPercentage",
    description="Castling Percentage by player",
)
async def castle(username: Optional[str] = None):
    with dict_cursor() as curr:
        if not username:
            sql = """WITH player_game AS (SELECT username, lichess_id FROM
                        Player JOIN Game on Player.username = Game.white_username
                            UNION ALL SELECT username, lichess_id FROM
                        Player JOIN Game on Player.username = Game.black_username
                        ),
                total_games AS (SELECT username, COUNT(lichess_id) as total FROM
                player_game GROUP BY username),
                castleOnly AS (SELECT DISTINCT game_id FROM GameMove
                WHERE move_notation IN ('O-O', 'O-O-O')),
                game_moves_castle AS (SELECT username, COUNT(DISTINCT game_id) as castle FROM (
                player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
                ) GROUP BY username)
                SELECT total_games.username, castle*100/(total) as Castling_Percentage  FROM (
                game_moves_castle JOIN total_games ON game_moves_castle.username = total_games.username
                );"""
        else:
            sql = (
                """
            WITH player_game AS (SELECT username, lichess_id FROM
                        Player JOIN Game on Player.username = Game.white_username
                            UNION ALL SELECT username, lichess_id FROM
                        Player JOIN Game on Player.username = Game.black_username
                        ),
                total_games AS (SELECT username, COUNT(lichess_id) as total FROM
                player_game GROUP BY username),
                castleOnly AS (SELECT DISTINCT game_id FROM GameMove
                WHERE move_notation IN ('O-O', 'O-O-O')),
                game_moves_castle AS (SELECT username, COUNT(DISTINCT game_id) as castle FROM (
                player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
                ) GROUP BY username)
                SELECT total_games.username, castle*100/(total) as Castling_Percentage  FROM (
                game_moves_castle JOIN total_games ON game_moves_castle.username = total_games.username
                ) WHERE total_games.username = \'"""
                + username
                + "' ; "
            )

        curr.execute(sql)
        result = curr.fetchall()

        return {
            "players": [
                {
                    "username": r["username"],
                    "CastlingPercentage": r["Castling_Percentage"],
                }
                for r in result
            ],
        }


@router.get("/RatioKtoQ", description="Ratio of King to Queen Castling by player")
async def ratio(username: Optional[str] = None):
    with dict_cursor() as curr:
        if not username:
            sql = """WITH player_game AS (SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.white_username
                    UNION ALL SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.black_username
                    ),
        castleOnly AS (SELECT DISTINCT game_id, move_notation FROM GameMoves
        WHERE move_notation IN ('O-O', 'O-O-O')),
        castle_king AS (SELECT username, COUNT(DISTINCT game_id) as king FROM (
        player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
        ) WHERE move_notation  = 'O-O'
        GROUP BY username
            HAVING king > 0),
    castle_queen AS (SELECT username, COUNT(DISTINCT game_id) as queen FROM (
        player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
        ) WHERE move_notation  = 'O-O-O'
    GROUP BY username
        HAVING queen > 0)
        SELECT castle_king.username, king/queen as ratio FROM (
        castle_king JOIN castle_queen ON castle_king.username = castle_queen.username
        );"""
        else:
            sql = (
                """
            WITH player_game AS (SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.white_username
                    UNION ALL SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.black_username
                    ),
        castleOnly AS (SELECT DISTINCT game_id, move_notation FROM GameMoves
        WHERE move_notation IN ('O-O', 'O-O-O')),
        castle_king AS (SELECT username, COUNT(DISTINCT game_id) as king FROM (
        player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
        ) WHERE move_notation  = 'O-O'
        GROUP BY username
            HAVING king > 0),
    castle_queen AS (SELECT username, COUNT(DISTINCT game_id) as queen FROM (
        player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
        ) WHERE move_notation  = 'O-O-O'
    GROUP BY username
        HAVING queen > 0)
        SELECT castle_king.username, king/queen as ratio  FROM (
        castle_king JOIN castle_queen ON castle_king.username = castle_queen.username
        ) WHERE castle_king.username = \'"""
                + username
                + "' ; "
            )

        curr.execute(sql)
        result = curr.fetchall()

        return {
            "players": [
                {
                    "username": r["username"],
                    "RatioKtoQ": r["ratio"],
                }
                for r in result
            ],
        }


@router.get(
    "/CountryWinPercent",
    description="Descending order of Country Win Percentages",
)
async def win_percent():
    with dict_cursor() as curr:
        sql = """SELECT  Country, SUM(wins)*100/ (SUM(losses) + SUM(wins)) as Win_Percentage FROM Player
    WHERE Country is not NULL
    GROUP BY Country
    ORDER BY Win_Percentage DESC;"""
        curr.execute(sql)
        result = curr.fetchall()
        return {
            "countries": [
                {
                    "country": r["Country"],
                    "win_percent": r["Win_Percentage"],
                }
                for r in result
            ],
        }


@router.get(
    "/totalWins",
    description="Descending order of total wins by country",
)
async def total_wins():
    with dict_cursor() as curr:
        sql = """SELECT Country, SUM(num_games) as Total_Games FROM Player
    WHERE Country is not NULL
    GROUP BY Country
    ORDER BY Total_Games DESC;"""

        curr.execute(sql)
        result = curr.fetchall()

        return {
            "countries": [
                {
                    "country": r["Country"],
                    "total_games": r["Total_Games"],
                }
                for r in result
            ],
        }


@router.get("/AvgTimeToWin", description="Average Time Taken for a Player to Win")
async def avgTime(username: Optional[str] = None):
    with dict_cursor() as curr:
        if not username:
            sql = """WITH player_game_white AS (SELECT DISTINCT username, lichess_id FROM
                    Player CROSS JOIN Game on Player.username = Game.white_username
                where result = '1-0'),
            white_time AS (SELECT username, lichess_id, (MAX(white_hundredths) - MIN(white_hundredths)) as time FROM
                player_game_white JOIN TimeRemaining on player_game_white.lichess_id = TimeRemaining.game_id
                GROUP BY username, lichess_id
                ),
        player_game_black AS (SELECT DISTINCT username, lichess_id,result FROM
                    Player JOIN Game on Player.username = Game.black_username
            where result = '0-1'
        ),
            black_time AS (SELECT username, game_id, (MAX(black_hundredths) - MIN(black_hundredths)) as time FROM
                player_game_black JOIN TimeRemaining on player_game_black.lichess_id = TimeRemaining.game_id
                GROUP BY username, game_id
            ),
        time_union as (SELECT * FROM white_time UNION ALL SELECT * FROM black_time)
        SELECT username, AVG(time) as avgTime
        FROM time_union
        GROUP BY username;"""
        else:
            sql = (
                """
            WITH player_game_white AS (SELECT DISTINCT username, lichess_id FROM
                    Player CROSS JOIN Game on Player.username = Game.white_username
                where result = '1-0'),
            white_time AS (SELECT username, lichess_id, (MAX(white_hundredths) - MIN(white_hundredths)) as time FROM
                player_game_white JOIN TimeRemaining on player_game_white.lichess_id = TimeRemaining.game_id
                GROUP BY username, lichess_id
                ),
        player_game_black AS (SELECT DISTINCT username, lichess_id,result FROM
                    Player JOIN Game on Player.username = Game.black_username
            where result = '0-1'
        ),
            black_time AS (SELECT username, game_id, (MAX(black_hundredths) - MIN(black_hundredths)) as time FROM
                player_game_black JOIN TimeRemaining on player_game_black.lichess_id = TimeRemaining.game_id
                GROUP BY username, game_id
            ),
        time_union as (SELECT * FROM white_time UNION ALL SELECT * FROM black_time)
        SELECT username, AVG(time) as avgTime
        FROM time_union
        WHERE username = \'"""
                + username
                + "' ; "
            )

        curr.execute(sql)
        result = curr.fetchall()
        return {
            "players": [
                {
                    "username": r["username"],
                    "avgTime": r["avgTime"],
                }
                for r in result
            ],
        }
