import asyncio
import aiomysql
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
    CompletionRateByRating,
)
from app.database.connect import (
    get_db_connection,
    get_dict_cursor,
    get_async_db_pool,
)
from collections import defaultdict
from app.database.util import get_rating_col, TerminationParity


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
    with dict_cursor() as cur:
        rating_col = get_rating_col(rating_type)
        cur.execute(
            f"""
            SELECT
                title,
                AVG({rating_col}) as avg_rating,
                STDDEV({rating_col}) as stddev_rating
            FROM Player
            GROUP BY title
            """,
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/{rating_type}/country",
    description="Get statistics on player ratings by country.",  # noqa: E501
    response_model=RatingByCountry,
)
async def country(
    rating_type: RatingType = Path(..., description="The rating type to analyze."),
):
    with dict_cursor() as cur:
        rating_col = get_rating_col(rating_type)
        cur.execute(
            f"""
            SELECT
                country,
                AVG({rating_col}) as avg_rating,
                STDDEV({rating_col}) as stddev_rating
            FROM Player
            GROUP BY country
            """,
        )
        result = cur.fetchall()
    return {"countries": result}


@router.get(
    "/{rating_type}/play-time",
    description="Get the average total play time (in seconds), broken down by player rating (rating taken from player profile).",  # noqa: E501
    response_model=PlayTimeByRating,
)
async def play_time(
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
                AVG(play_time) as avg_play_time,
                STDDEV(play_time) as stddev_play_time
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
    "/{rating_type}/percent-patron",
    description="Get the percentage of players who are Lichess patrons, broken down by rating (rating taken from player profile).",  # noqa: E501
    response_model=PercentPatronByRating,
)
async def percent_patron(
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
                AVG(patron * 100) as percent_patron
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
    "/{rating_type}/percent-tos-violators",
    description="Get the percentage of players who have violated TOS, broken down by rating (rating taken from player profile).",  # noqa: E501
    response_model=PercentTOSViolatorsByRating,
)
async def percent_tos_violators(
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
                AVG(tos_violation * 100) as percent_tos_violators
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
    "/{rating_type}/cumulative-result-percentages",
    description="Get the average cumulative win/draw/loss percentages by player rating range (rating taken from player profile).",  # noqa: E501
    response_model=CumulativeResultPercentagesByRating,
)
async def cumulative_result_percentages(
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
                100 * AVG(wins / (wins+draws+losses)) as win_percentage,
                100 * AVG(draws / (wins+draws+losses)) as draw_percentage,
                100 * AVG(losses / (wins+draws+losses)) as loss_percentage
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
    "/{game_type}/completion-rate",
    description="Get the average cumulative completion rate, broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=CompletionRateByRating,
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
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH FilteredGame as (
                SELECT * FROM (
                    SELECT 
                        white_elo as rating,
                        (
                            CASE WHEN termination = 'Resignation' AND result = '0-1' THEN 0
                            ELSE 100 END
                        ) as completion,
                        category,
                        start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT 
                        black_elo as rating,
                        (
                            CASE WHEN termination = 'Resignation' AND result = '0-1' THEN 0
                            ELSE 100 END
                        ) as completion,
                        category,
                        start_timestamp
                    FROM Game
                ) t
                WHERE 
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                FLOOR(rating/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR(rating/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                AVG(completion) as avg_completion_rate,
                STDDEV(completion) as stddev_completion_rate
            FROM FilteredGame
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        result = cur.fetchall()
    return {"bins": result}


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
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH FilteredGame as (
                SELECT * FROM (
                    SELECT 
                        white_elo as rating,
                        (CASE WHEN result = '1-0' THEN 1 ELSE 0 END) as white_win,
                        NULL as black_win,
                        (CASE WHEN result = '1/2-1/2' THEN 1 ELSE 0 END) as white_draw,
                        NULL as black_draw,
                        (CASE WHEN result = '0-1' THEN 1 ELSE 0 END) as white_loss,
                        NULL as black_loss,
                        category,
                        start_timestamp
                    FROM Game
                    UNION ALL
                    SELECT 
                        black_elo as rating,
                        NULL as white_win,
                        (CASE WHEN result = '0-1' THEN 1 ELSE 0 END) as black_win,
                        NULL as white_draw,
                        (CASE WHEN result = '1/2-1/2' THEN 1 ELSE 0 END) as black_draw,
                        NULL as white_loss,
                        (CASE WHEN result = '1-0' THEN 1 ELSE 0 END) as black_loss,
                        category,
                        start_timestamp
                    FROM Game
                ) t
                WHERE 
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                FLOOR(rating/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR(rating/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                100 * AVG(white_win) as white_win_percentage,
                100 * AVG(black_win) as black_win_percentage,
                100 * AVG(white_draw) as white_draw_percentage,
                100 * AVG(black_draw) as black_draw_percentage,
                100 * AVG(white_loss) as white_loss_percentage,
                100 * AVG(black_loss) as black_loss_percentage
            FROM FilteredGame
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        result = cur.fetchall()
    return {"bins": result}


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
        default=50, ge=1, description="Optionally, specify the rating bin size (for each color)."
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT
                FLOOR(white_elo/%(bin_size)s) * %(bin_size)s as white_rating_min,
                FLOOR(white_elo/%(bin_size)s + 1) * %(bin_size)s as white_rating_max,
                FLOOR(black_elo/%(bin_size)s) * %(bin_size)s as black_rating_min,
                FLOOR(black_elo/%(bin_size)s + 1) * %(bin_size)s as black_rating_max,
                100 * AVG(CASE WHEN result = '1-0' THEN 1 ELSE 0 END) as white_win_percentage,
                100 * AVG(CASE WHEN result = '0-1' THEN 1 ELSE 0 END) as black_win_percentage,
                100 * AVG(CASE WHEN result = '1/2-1/2' THEN 1 ELSE 0 END) as white_draw_percentage,
                100 * AVG(CASE WHEN result = '1/2-1/2' THEN 1 ELSE 0 END) as black_draw_percentage,
                100 * AVG(CASE WHEN result = '0-1' THEN 1 ELSE 0 END) as white_loss_percentage,
                100 * AVG(CASE WHEN result = '1-0' THEN 1 ELSE 0 END) as black_loss_percentage
            FROM Game
            WHERE 
                (%(game_type)s IS NULL OR %(game_type)s = category)
                AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(start_timestamp))
                AND (%(end_date)s IS NULL OR  DATE(start_timestamp) <= %(end_date)s)
            GROUP BY white_rating_min, black_rating_min
            ORDER BY white_rating_min, black_rating_min
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        result = cur.fetchall()
    return {"bins": result}


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
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH FilteredGame as (
                SELECT * FROM (
                    SELECT 
                        white_elo as rating,
                        game_length,
                        category,
                        start_timestamp
                    FROM Game
                    UNION ALL
                    SELECT 
                        black_elo as rating,
                        game_length,
                        category,
                        start_timestamp
                    FROM Game
                ) t
                WHERE 
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                FLOOR(rating/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR(rating/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                AVG(game_length) as game_length
            FROM FilteredGame
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        result = cur.fetchall()
    return {"bins": result}


@router.get(
    "/{game_type}/num-openings",
    description="Get the average number of distinct openings per player broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=NumOpeningsByRating,
)
async def num_openings(
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
        default=100,
        ge=10,
        description="Optionally, specify the rating bin size (for each color). For this route, bin size should be higher to get enough per-player data.",  # noqa: E501
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH FilteredGame as (
                SELECT * FROM (
                    SELECT 
                        white_elo as rating,
                        white_username as username,
                        opening_eco,
                        game_length,
                        category,
                        start_timestamp
                    FROM Game
                    UNION ALL
                    SELECT 
                        black_elo as rating,
                        black_username as username,
                        opening_eco,
                        game_length,
                        category,
                        start_timestamp
                    FROM Game
                ) t
                WHERE 
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                t.rating_min as rating_min,
                t.rating_max as rating_max,
                AVG(t.num_openings) as num_openings
            FROM (
                SELECT
                    FLOOR(rating/%(bin_size)s) * %(bin_size)s as rating_min,
                    FLOOR(rating/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                    COUNT(DISTINCT(opening_eco)) as num_openings
                FROM FilteredGame
                GROUP BY rating_min, username
            ) t
            GROUP BY rating_min
            ORDER BY rating_min
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        result = cur.fetchall()
    return {"bins": result}


@router.get(
    "/{game_type}/termination-type",
    description="Get game termination type percentages broken down by player rating (rating at the time of the game).",  # noqa: E501
    response_model=GameTerminationTypeByRating,
)
async def termination_type(
    termination_parity: Optional[TerminationParity] = Query(
        default=None,
        description="Optionally, specify the parity of the result (win, draw, or loss) from the perspective of the player from the relevant country.",  # noqa: E501
    ),
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
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH FilteredGame as (
                SELECT * FROM (
                    SELECT 
                        white_elo as rating,
                        game_length,
                        category,
                        termination,
                        start_timestamp
                    FROM Game
                    WHERE
                        %(termination_parity)s IS NULL
                        OR %(termination_parity)s = 'Win' AND result = '1-0'
                        OR %(termination_parity)s = 'Loss' AND result = '0-1'
                        OR %(termination_parity)s = 'Draw' AND result = '1/2-1/2'
                    UNION ALL
                    SELECT 
                        black_elo as rating,
                        game_length,
                        category,
                        termination,
                        start_timestamp
                    FROM Game
                    WHERE
                        %(termination_parity)s IS NULL
                        OR %(termination_parity)s = 'Win' AND result = '0-1'
                        OR %(termination_parity)s = 'Loss' AND result = '1-0'
                        OR %(termination_parity)s = 'Draw' AND result = '1/2-1/2'
                ) t
                WHERE 
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            ),
            FilteredGameCount as (
                SELECT 
                    FLOOR(rating/%(bin_size)s) * %(bin_size)s as rating_min,
                    COUNT(*) as count
                FROM FilteredGame
                GROUP BY rating_min
            )
            SELECT
                FLOOR(g.rating/%(bin_size)s) * %(bin_size)s as rating_min,
                FLOOR(g.rating/%(bin_size)s + 1) * %(bin_size)s as rating_max,
                g.termination as termination,
                100 * COUNT(*) / c.count as percentage
            FROM FilteredGame g INNER JOIN FilteredGameCount c ON
                FLOOR(g.rating/%(bin_size)s) * %(bin_size)s = c.rating_min
            GROUP BY rating_min, g.termination
            ORDER BY rating_min
            """,
            {
                "termination_parity": termination_parity,
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "bin_size": bin_size,
            },
        )
        flat_result = cur.fetchall()
    result = defaultdict(list)
    for r in flat_result:
        result[r["rating_min"], r["rating_max"]].append(
            {
                "termination_type": r["termination"],
                "percentage": r["percentage"],
            }
        )
    return {
        "bins": [
            {
                "rating_min": rating_min,
                "rating_max": rating_max,
                "termination_types": result[rating_min, rating_max],
            }
            for rating_min, rating_max in result
        ],
    }


# NOTE: we can't complete the following routes until we add white_accuracy and black_accuracy
# fields to the game table and analyze games with a chess engine (this is computationally
# expensive so it might take too long to run for a meaningful number of games; if so
# we will abandon the following routes)

"""
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
"""
