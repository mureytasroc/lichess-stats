from multiprocessing import connection
from statistics import mode
from tokenize import String
from typing import Optional

import pymysql.cursors
from fastapi import APIRouter, Path, Query

from app.database.connect import get_db_connection, get_dict_cursor
from app.database.util import GameType
from app.models.games import CastlingPercentage, DateDistribution


router = APIRouter()

dict_cursor = get_dict_cursor(get_db_connection())


@router.get(
    "/date-distribution",
    description="Get the distribution of game dates.",
    response_model=DateDistribution,
)
async def date_distribution():
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
    "/castling-percentage",
    description="Get the castling percentage by player",
    response_model=CastlingPercentage,
)
async def castling_percentage(
    username: Optional[str] = Query(
        default=None,
        description="Optionally, provide a specific username for which to get castling statistics.",  # noqa: E501
    ),
    game_type: Optional[GameType] = Query(default=None, description="The game type to analyze."),
    start_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify a start date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify an end date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
):
    with dict_cursor() as curr:
        curr.execute(
            """
            WITH FlatGame as (
                SELECT
                    white_username as username,
                    lichess_id,
                    (CASE WHEN EXISTS(
                        SELECT * FROM GameMove m
                        WHERE m.game_id = lichess_id
                            AND move_notation IN ('O-O', 'O-O-O')
                            AND MOD(ply, 2) = 1
                    ) THEN 100 ELSE 0 END) as castle
                FROM Game
                WHERE %(username)s IS NULL OR white_username = %(username)s
                    AND (%(game_type)s IS NULL OR %(game_type)s = category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(start_timestamp) <= %(end_date)s)
                UNION ALL
                SELECT
                    black_username as username,
                    lichess_id,
                    (CASE WHEN EXISTS(
                        SELECT * FROM GameMove m
                        WHERE m.game_id = lichess_id
                            AND move_notation IN ('O-O', 'O-O-O')
                            AND MOD(ply, 2) = 0
                    ) THEN 100 ELSE 0 END) as castle
                FROM Game
                WHERE %(username)s IS NULL OR black_username = %(username)s
                    AND (%(game_type)s IS NULL OR %(game_type)s = category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(start_timestamp) <= %(end_date)s)
            )
            SELECT 
                username,
                SUM(castle) / COUNT(*) as castling_percentage
            FROM FlatGame
            GROUP BY username
            """,
            {
                "username": username,
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        result = curr.fetchall()

        return {"players": result}


@router.get("/RatioKtoQ", description="Ratio of King to Queen Castling by player")
async def ratio(username: Optional[str] = None):
    with dict_cursor() as curr:
        if not username:
            sql = """WITH player_game AS (SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.white_username
                    UNION ALL SELECT username, lichess_id FROM
                Player JOIN Game on Player.username = Game.black_username
                    ),
        castleOnly AS (SELECT DISTINCT game_id, move_notation FROM GameMove
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
        castleOnly AS (SELECT DISTINCT game_id, move_notation FROM GameMove
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
