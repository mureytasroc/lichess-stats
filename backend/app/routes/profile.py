from typing import Optional

from fastapi import APIRouter, Query
import pymysql


from app.database.util import GameType
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
)


router = APIRouter()

mydb = pymysql.connect(
    host="chess-db.ccwnen4yavww.us-east-1.rds.amazonaws.com",
    user="admin",
    password="aaaaaaaa",
    port=3306,
    db="chesswins",
)

# Titles


@router.get(
    "/title/distribution",
    description="Get the distribution of players by title.",  # noqa: E501
    response_model=TitleDistribution,
)
async def title_distribution():
    # TODO
    print("SHOULD FETCH")
    q = """
    SELECT title, COUNT(*) as count
    FROM Player
    GROUP BY title
    """
    with mydb.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(q, [])
        result = cur.fetchall()
    return {
        "titles": result
    }


@ router.get(
    "/title/completion-rate",
    description="Get statistics on game completion rate by title.",  # noqa: E501
    response_model=CompletionRateByTitle,
)
async def completion_rate_by_title():
    # TODO
    return {
        "titles": [
            {
                "title": "GM",
                "avg_completion_rate": 80,
                "stddev_completion_rate": 10,
            }
        ]
    }


@router.get(
    "/title/results",
    description="Get win/draw/loss percentages by title.",  # noqa: E501
    response_model=ResultPercentagesByTitle,
)
async def result_percentages_by_title():
    # TODO
    return {
        "titles": [
            {
                "title": "GM",
                "win_percentage": 80,
                "draw_percentage": 80,
                "loss_percentage": 80,
            }
        ]
    }


@router.get(
    "/title/termination-type",
    description="Get game termination type percentages by title.",  # noqa: E501
    response_model=GameTerminationTypeByTitle,
)
async def termination_type_by_title(
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
                "normal_percentage": 80,
                "resignation_percentage": 80,
                "time_forfeit_percentage": 80,
                "abandoned_percentage": 80,
            }
        ]
    }


@router.get(
    "/title/game-length",
    description="Get statistics on game length (number of moves) by title.",  # noqa: E501
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
    description="Get the distribution of players by country.",  # noqa: E501
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
    description="Get statistics on player ratings by country.",  # noqa: E501
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
    description="Get win/draw/loss percentages by country.",  # noqa: E501
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
    description="Get game termination type percentages by country.",  # noqa: E501
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
