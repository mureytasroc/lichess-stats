from typing import Optional

from fastapi import APIRouter, Path, Query

from app.database.util import GameType, RatingType
from app.models.rating import (
    AccuracyByRating,
    CumulativeResultPercentagesByRating,
    GameLengthByRating,
    GameTerminationTypeByRating,
    NumOpeningsByRating,
    PercentPatronByRating,
    PercentTOSViolatorsByRating,
    PlayTimeByRating,
    RatingByCountry,
    RatingByRating,
    RatingByTitle,
    RatingDistribution,
    ResultPercentagesByRating,
    ResultPercentagesByRating2D,
    StdDevAccuracyByRating,
)
from app.database.connect import get_db_connection, get_dict_cursor
from app.database.util import get_rating_col


router = APIRouter()

dict_cursor = get_dict_cursor(get_db_connection())


@router.get(
    "/{rating_type}/distribution",
    description="Get the distribution of player ratings (rating taken from player profile).",
    response_model=RatingDistribution,
)
async def distribution(
    rating_type: RatingType = Path(..., description="The rating type."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    with dict_cursor() as cur:
        rating_col = get_rating_col(rating_type)
        cur.execute(
            f"""
            SELECT
                FLOOR({rating_col}/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR({rating_col}/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                COUNT(*) as count
            FROM Player
            WHERE {rating_col} IS NOT NULL
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {"bin_size": bin_size},
        )
        result = cur.fetchall()
    return {"bins": result}


@router.get(
    "/{rating_type}/compare",
    description="Get the average rating (for each game type), broken down by rating in a specific game type (ratings taken from player profile).",  # noqa: E501
    response_model=RatingByRating,
)
async def compare(
    rating_type: RatingType = Path(..., description="The rating type over which to bin."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    with dict_cursor() as cur:
        rating_col = get_rating_col(rating_type)
        cur.execute(
            f"""
            SELECT
                FLOOR({rating_col}/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR({rating_col}/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                AVG(ultrabullet_rating) as ultrabullet_rating,
                AVG(bullet_rating) as bullet_rating,
                AVG(blitz_rating) as blitz_rating,
                AVG(rapid_rating) as rapid_rating,
                AVG(classical_rating) as classical_rating,
                AVG(correspondence_rating) as correspondence_rating,
                AVG(fide_rating) as fide_rating,
                AVG(uscf_rating) as uscf_rating,
                AVG(ecf_rating) as ecf_rating
            FROM Player
            WHERE {rating_col} IS NOT NULL
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {"bin_size": bin_size},
        )
        result = cur.fetchall()
    return {"bins": result}


@router.get(
    "/{rating_type}/title",
    description="Get statistics on player ratings by title.",  # noqa: E501
    response_model=RatingByTitle,
)
async def title(
    rating_type: RatingType = Path(..., description="The rating type to analyze."),
):
    # TODO
    return {
        "titles": [
            {
                "title": "GM",
                "avg_rating": 3000,
                "stddev_rating": 200,
            }
        ]
    }


@router.get(
    "/{rating_type}/country",
    description="Get statistics on player ratings by country.",  # noqa: E501
    response_model=RatingByCountry,
)
async def country(
    rating_type: RatingType = Path(..., description="The rating type to analyze."),
):
    # TODO
    return {
        "countries": [
            {
                "country": "US",
                "avg_rating": 3000,
                "stddev_rating": 200,
            }
        ]
    }


@router.get(
    "/{rating_type}/play-time",
    description="Get the average total play time (in seconds), broken down by player rating (rating taken from player profile).",  # noqa: E501
    response_model=PlayTimeByRating,
)
async def play_time(
    rating_type: RatingType = Path(..., description="The rating type over which to bin."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "play_time": 100000}]}


@router.get(
    "/{rating_type}/percent-patron",
    description="Get the percentage of players who are Lichess patrons, broken down by rating (rating taken from player profile).",  # noqa: E501
    response_model=PercentPatronByRating,
)
async def percent_patron(
    rating_type: RatingType = Path(..., description="The rating type over which to bin."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "percent_patron": 5.2}]}


@router.get(
    "/{rating_type}/percent-tos-violators",
    description="Get the percentage of players who have violated TOS, broken down by rating (rating taken from player profile).",  # noqa: E501
    response_model=PercentTOSViolatorsByRating,
)
async def percent_tos_violators(
    rating_type: RatingType = Path(..., description="The rating type over which to bin."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "percent_tos_violators": 1.1}]}


@router.get(
    "/{rating_type}/cumulative-result-percentages",
    description="Get the average cumulative win/draw/loss percentages by player rating range (rating taken from player profile).",  # noqa: E501
    response_model=CumulativeResultPercentagesByRating,
)
async def cumulative_result_percentages(
    rating_type: RatingType = Path(..., description="The rating type over which to bin."),
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {
        "bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "win_percentage": 48.5,
                "draw_percentage": 5,
                "loss_percentage": 46.5,
            }
        ],
    }


@router.get(
    "/{rating_type}/completion-rate",
    description="Get the average cumulative completion rate, broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=PlayTimeByRating,
)
async def completion_rate(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "completion_rate": 80.2}]}


@router.get(
    "/{game_type}/result-percentages",
    description="Get the average win/draw/loss percentages broken down by color and player rating range (rating at the time of the game).",  # noqa: E501
    response_model=ResultPercentagesByRating,
)
async def result_percentages(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {
        "white_bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "win_percentage": 50,
                "draw_percentage": 5,
                "loss_percentage": 45,
            }
        ],
        "black_bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "win_percentage": 47,
                "draw_percentage": 5,
                "loss_percentage": 48,
            }
        ],
    }


@router.get(
    "/{game_type}/result-percentages-2d",
    description="Get the average win/draw/loss percentages broken down by white rating and black rating (rating at the time of the game).",  # noqa: E501
    response_model=ResultPercentagesByRating2D,
)
async def result_percentages_2d(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(
        default=10, ge=1, description="Optionally, specify the rating bin size (for each color)."
    ),
):
    # TODO
    return {
        "bins": [
            {
                "white_rating_min": 1000,
                "white_rating_max": 1010,
                "black_rating_min": 1000,
                "black_rating_max": 1010,
                "white_win_percentage": 60.2,
                "white_draw_percentage": 60.2,
                "white_loss_percentage": 60.2,
                "black_win_percentage": 45,
                "black_draw_percentage": 45,
                "black_loss_percentage": 45,
            }
        ]
    }


@router.get(
    "/{game_type}/game-length",
    description="Get the average game length (number of moves) broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=GameLengthByRating,
)
async def game_length(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(
        default=10, ge=1, description="Optionally, specify the rating bin size (for each color)."
    ),
):
    # TODO
    return {
        "bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "game_length": 22.5,
            }
        ],
    }


@router.get(
    "/{game_type}/num-openings",
    description="Get the average number of distinct openings per player broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=NumOpeningsByRating,
)
async def num_openings(
    game_type: GameType = Path(..., description="The game type to analyze."),
    minimum_frequency: Optional[float] = Query(
        default=None,
        ge=0,
        le=100,
        description="Optionally, specify the minimum percentage (0-100) of games in which an opening is used by a player, in order to count the opening for that player. By default, there is no minimum frequency.",  # noqa: E501
    ),
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
    bin_size: int = Query(
        default=100,
        ge=10,
        description="Optionally, specify the rating bin size (for each color). For this route, bin size should be higher to get enough per-player data.",  # noqa: E501
    ),
):
    # TODO
    return {
        "bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "num_openings": 3.5,
            }
        ],
    }


@router.get(
    "/{game_type}/termination-type",
    description="Get game termination type percentages broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=GameTerminationTypeByRating,
)
async def termination_type(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(
        default=10, ge=1, description="Optionally, specify the rating bin size (for each color)."
    ),
):
    # TODO
    return {
        "bins": [
            {
                "rating_min": 1000,
                "rating_max": 1010,
                "normal_percentage": 22.5,
                "resignation_percentage": 22.5,
                "time_forfeit_percentage": 22.5,
                "abandoned_percentage": 22.5,
            }
        ],
    }


# NOTE: we can't complete the following routes until we add white_accuracy and black_accuracy
# fields to the game table and analyze games with a chess engine (this is computationally
# expensive so it might take too long to run for a meaningful number of games; if so
# we will abandon the following routes)


@router.get(
    "/{game_type}/accuracy",
    description="Get the average game accuracy, broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=AccuracyByRating,
)
async def avg_accuracy(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "avg_accuracy": 70.2}]}


@router.get(
    "/{game_type}/stddev-accuracy",
    description="Get the standard deviation of game accuracies, broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=StdDevAccuracyByRating,
)
async def stddev_accuracy(
    game_type: GameType = Path(..., description="The game type to analyze."),
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
    bin_size: int = Query(default=10, ge=1, description="Optionally, specify the rating bin size."),
):
    # TODO
    return {"bins": [{"rating_min": 1000, "rating_max": 1010, "stddev_accuracy": 10.1}]}
