from typing import Optional

from fastapi import APIRouter, Query
from fastapi_redis_cache import cache

from app.database.connect import get_dict_cursor
from app.database.util import GameType, convert_to_float
from app.models.games import (
    AvgTimeToWin,
    CastlingPercentage,
    CastlingSidePercentages,
    DateDistribution,
)


router = APIRouter()

dict_cursor = get_dict_cursor()


@router.get(
    "/date-distribution",
    description="Get the distribution of game dates.",
    response_model=DateDistribution,
)
@cache()
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
    return {"dates": convert_to_float(result)}


@router.get(
    "/castling-percentage",
    description="Get the castling percentage by player.",
    response_model=CastlingPercentage,
)
@cache()
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
    return {"players": convert_to_float(result)}


@router.get(
    "/castling-side-percentages",
    description="Get kingside and queenside castling percentages by player.",
    response_model=CastlingSidePercentages,
)
@cache()
async def castling_side_percentages(
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
                            AND move_notation = 'O-O'
                            AND MOD(ply, 2) = 1
                    ) THEN 100 ELSE 0 END) as castle_king,
                    (CASE WHEN EXISTS(
                        SELECT * FROM GameMove m
                        WHERE m.game_id = lichess_id
                            AND move_notation = 'O-O-O'
                            AND MOD(ply, 2) = 1
                    ) THEN 100 ELSE 0 END) as castle_queen
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
                            AND move_notation = 'O-O'
                            AND MOD(ply, 2) = 0
                    ) THEN 100 ELSE 0 END) as castle_king,
                    (CASE WHEN EXISTS(
                        SELECT * FROM GameMove m
                        WHERE m.game_id = lichess_id
                            AND move_notation = 'O-O-O'
                            AND MOD(ply, 2) = 0
                    ) THEN 100 ELSE 0 END) as castle_queen
                FROM Game
                WHERE %(username)s IS NULL OR black_username = %(username)s
                    AND (%(game_type)s IS NULL OR %(game_type)s = category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(start_timestamp) <= %(end_date)s)
            )
            SELECT
                username,
                SUM(castle_king) / COUNT(*) as kingside_percentage,
                SUM(castle_queen) / COUNT(*) as queenside_percentage
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
    return {"players": convert_to_float(result)}


@router.get(
    "/avg-time-to-win",
    description="Average time taken for a player to win.",
    response_model=AvgTimeToWin,
)
@cache()
async def avg_time_to_win(
    username: Optional[str] = Query(
        default=None,
        description="Optionally, provide a specific username for which to get average time to win.",  # noqa: E501
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
            WITH FilteredGame as (
                SELECT * FROM Game
                WHERE
                    (%(game_type)s IS NULL OR %(game_type)s = category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(start_timestamp) <= %(end_date)s)
            ),
            WhiteWin AS (
                SELECT * FROM FilteredGame
                WHERE
                    %(username)s IS NULL OR white_username = %(username)s
                    AND result = '1-0'
            ),
            BlackWin AS (
                SELECT * FROM FilteredGame
                WHERE
                    %(username)s IS NULL OR black_username = %(username)s
                    AND result = '0-1'
            ),
            TimeToWin AS (
                SELECT
                    g.white_username as username,
                    MAX(white_hundredths) - MIN(white_hundredths) as time_to_win
                FROM WhiteWin g INNER JOIN TimeRemaining t ON g.lichess_id = t.game_id
                GROUP BY g.white_username, g.lichess_id
                UNION ALL
                SELECT
                    g.black_username as username,
                    MAX(black_hundredths) - MIN(black_hundredths) as time_to_win
                FROM BlackWin g INNER JOIN TimeRemaining t ON g.lichess_id = t.game_id
                GROUP BY g.black_username, g.lichess_id
            )
            SELECT
                username,
                AVG(time_to_win) / 100 as avg_time_to_win
            FROM TimeToWin
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
    return {"players": convert_to_float(result)}


@router.get("/MostCommonOpeningsElo", description="Most Common Openings Played in an Elo Range")
@cache()
async def mostCommonOpenings(
    elo_lower: Optional[int] = Query(
        default=0, description="Optionally, provide a lower bound for elo search"
    ),
    elo_upper: Optional[int] = Query(
        default=3000, description="Optionally, provide an upper bound for elo search"
    ),
    game_type: Optional[GameType] = Query(
        default=GameType.Blitz, description="Optionally, specify a game type to analyze."
    ),
):
    with dict_cursor() as curr:
        curr.execute(
            """
            WITH PLAYER_ELO_FILTER AS (
                SELECT *
                FROM Player
                WHERE %(game_type)s >= %(elo_lower)s
                AND %(game_type)s <= %(elo_upper)s
            ),
            WHITE_OPENINGS AS (
                SELECT g.opening_eco AS opening_code, COUNT(*) AS COUNT
                FROM PLAYER_ELO_FILTER p
                        INNER JOIN Game g ON (p.username = g.white_username)
                GROUP BY g.opening_eco
                ORDER BY g.opening_eco),
            BLACK_OPENINGS AS (
                SELECT g.opening_eco AS opening_code, COUNT(*) AS COUNT
                FROM PLAYER_ELO_FILTER p
                        INNER JOIN Game g ON (p.username = g.black_username)
                GROUP BY g.opening_eco
                ORDER BY g.opening_eco),
            OPENINGS AS (
                SELECT opening_code, SUM(COUNT) AS COUNT
                FROM (SELECT *
                    FROM WHITE_OPENINGS
                    UNION
                    SELECT *
                    FROM BLACK_OPENINGS) AS tbl
                GROUP BY opening_code
            )
            SELECT opening_code,
                e.opening_name,
                e.opening_moves,
                ROUND(count / (SELECT SUM(count) FROM OPENINGS), 3) AS frequency
            FROM OPENINGS o
                    INNER JOIN EcoCode e ON o.opening_code = e.code
            ORDER BY frequency DESC
            """,
            {
                "game_type": game_type,
                "elo_lower": elo_lower,
                "elo_upper": elo_upper,
            },
        )

        result = curr.fetchall()
        return convert_to_float(result)


@router.get("/BiggestComebacks", description="Ordered list of biggest comebacks made for players")
@cache()
async def biggestComebacks():
    with dict_cursor() as curr:
        curr.execute(
            """
            WITH white_wins AS (SELECT lichess_id AS id, white_username AS winner_username
                    FROM Game
                    WHERE result = '1-0'),
            black_wins AS (
                SELECT lichess_id AS id, black_username AS winner_username
                FROM Game
                WHERE result = '0-1'),
            worst_white_positions AS (
                SELECT w.id AS game_id, ABS(MIN(e.eval)) AS worst_position
                FROM white_wins w
                        INNER JOIN Evaluation e ON w.id = e.game_id
                GROUP BY w.id
            ),
            worst_black_positions AS (
                SELECT b.id AS game_id, ABS(MAX(e.eval)) AS worst_position
                FROM black_wins b
                        INNER JOIN Evaluation e ON b.id = e.game_id
                GROUP BY b.id)
            SELECT winner_username, MAX(results.worst_position) AS comeback_deficit
            FROM (SELECT winner_username, MAX(b.worst_position) AS worst_position
                FROM white_wins a
                        INNER JOIN worst_white_positions b ON a.id = b.game_id
                GROUP BY winner_username
                UNION
                SELECT winner_username, MAX(b.worst_position) AS worst_position
                FROM black_wins a
                        INNER JOIN worst_black_positions b ON a.id = b.game_id
                GROUP BY winner_username) AS results
            GROUP BY winner_username
            ORDER BY comeback_deficit DESC
            """
        )

        result = curr.fetchall()
        return convert_to_float(result)
