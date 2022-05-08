from typing import Optional

from fastapi import APIRouter, Query
import pymysql
from app.database.connect import get_db_connection
from app.database.util import exclusive_end_date, game_type_case, TerminationParity
from contextlib import contextmanager


from app.database.util import GameType, title_to_desc
from app.models.profile import (
    CompletionRateByCountry,
    CompletionRateByTitle,
    CountryDistribution,
    GameLengthByCountry,
    GameLengthByTitle,
    GameTerminationTypeByCountry,
    GameTerminationTypeByTitle,
    ResultPercentagesByCountry,
    ResultPercentagesByTitle,
    TitleDistribution,
    TitleDescription,
)
from collections import defaultdict


router = APIRouter()

db_connection = get_db_connection()


@contextmanager
def dict_cursor():
    with db_connection.cursor(pymysql.cursors.DictCursor) as cur:
        yield cur
        db_connection.commit()


# Titles


@router.get(
    "/title/description",
    description="Get an array of title descriptions.",
    response_model=TitleDescription,
)
async def title_description():
    return {"titles": [{"title": k, "description": v} for k, v in title_to_desc.items()]}


@router.get(
    "/title/distribution",
    description="Get the distribution of players by title.",
    response_model=TitleDistribution,
)
async def title_distribution():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT title, COUNT(*) as count
            FROM Player
            GROUP BY title
            """
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/title/completion-rate",
    description="Get statistics on game completion rate by title.",
    response_model=CompletionRateByTitle,
)
async def completion_rate_by_title():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT 
                title,
                AVG(completion_rate) as avg_completion_rate,
                STDDEV(completion_rate) as stddev_completion_rate
            FROM Player
            GROUP BY title
            """
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/title/results",
    description="Get win/draw/loss percentages by title.",
    response_model=ResultPercentagesByTitle,
)
async def result_percentages_by_title():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT 
                title,
                100 * AVG(wins / num_games) as win_percentage,
                100 * AVG(draws / num_games) as draw_percentage,
                100 * AVG(losses / num_games) as loss_percentage
            FROM Player
            GROUP BY title
            """
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/title/termination-type",
    description="Get game termination type percentages by title.",
    response_model=GameTerminationTypeByTitle,
)
async def termination_type_by_title(
    termination_parity: Optional[TerminationParity] = Query(
        default=None,
        description="Optionally, specify the parity of the result (win, draw, or loss) from the perspective of the player with the relevant title.",  # noqa: E501
    ),
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
    ),
    start_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify a start month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify an end month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGames as (
                SELECT * FROM (
                    SELECT 
                        p.title as title,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.termination as termination,
                        g.result as result,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION
                    SELECT 
                        p.title as title,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.termination as termination,
                        g.result as result,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.black_username = p.username
                ) t
                WHERE 
                    (
                        %(termination_parity)s IS NULL
                        OR %(termination_parity)s = 'win' 
                            AND t.white_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'loss' 
                            AND t.white_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'win' 
                            AND t.black_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'loss' 
                            AND t.black_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'draw' AND t.result = '1/2-1/2'
                    )
                    AND (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= t.start_timestamp)
                    AND (%(end_date)s IS NULL OR t.start_timestamp < %(end_date)s)
            ),
            ProfileGameCounts as (
                SELECT username, COUNT(*) as count FROM ProfileGames g2
                GROUP BY username
            )
            SELECT
                t.title as title,
                t.termination as termination,
                AVG(t.percentage) as avg_percentage
            FROM (
                SELECT
                    g.title as title,
                    g.termination as termination,
                    COUNT(*) / c.count as percentage
                FROM ProfileGames g INNER JOIN ProfileGameCounts c ON g.username = c.username
                GROUP BY g.username, g.title, g.termination
            ) t
            GROUP BY t.title, t.termination
            """,
            {
                "game_type": game_type_case(game_type),
                "start_date": start_date,
                "end_date": exclusive_end_date(end_date),
                "termination_parity": termination_parity and termination_parity.lower(),
            },
        )
        flat_result = cur.fetchall()

    result = defaultdict(list)
    for r in flat_result:
        print(r["termination"])
        result[r["title"]].append(
            {
                "termination_type": r["termination"],
                "percentage": r["avg_percentage"],
            }
        )

    return {
        "titles": [{"title": title, "termination_types": result[title]} for title in result],
    }


@router.get(
    "/title/game-length",
    description="Get statistics on game length (number of moves) by title.",
    response_model=GameLengthByTitle,
)
async def game_length_by_title(
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
    ),
    start_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify a start month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify an end month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
):
    # TODO
    return {
        "titles": [
            {
                "title": "GM",
                "avg_game_length": 30,
                "stddev_game_length": 10,
            }
        ]
    }


# Countries


@router.get(
    "/country/distribution",
    description="Get the distribution of players by country.",
    response_model=CountryDistribution,
)
async def country_distribution():
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "count": 10000,
            }
        ]
    }


@router.get(
    "/country/completion-rate",
    description="Get statistics on player ratings by country.",
    response_model=CompletionRateByCountry,
)
async def completion_rate_by_country():
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "avg_completion_rate": 80,
                "stddev_completion_rate": 10,
            }
        ]
    }


@router.get(
    "/country/results",
    description="Get win/draw/loss percentages by country.",
    response_model=ResultPercentagesByCountry,
)
async def result_percentages_by_country():
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "win_percentage": 80,
                "draw_percentage": 80,
                "loss_percentage": 80,
            }
        ]
    }


@router.get(
    "/country/termination-type",
    description="Get game termination type percentages by country.",
    response_model=GameTerminationTypeByCountry,
)
async def termination_type_by_country(
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
    ),
    start_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify a start month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify an end month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
):
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "normal_percentage": 80,
                "resignation_percentage": 80,
                "time_forfeit_percentage": 80,
                "abandoned_percentage": 80,
            }
        ]
    }


@router.get(
    "/country/game-length",
    description="Get statistics on game length (number of moves) by country.",  # noqa: E501
    response_model=GameLengthByCountry,
)
async def game_length_by_country(
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
    ),
    start_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify a start month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}$",
        description="Optionally, specify an end month of games to analyze (inclusive), of the form YYYY-MM.",  # noqa: E501
    ),
):
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "avg_game_length": 30,
                "stddev_game_length": 10,
            }
        ]
    }
