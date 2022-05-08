from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, Query

from app.database.connect import get_db_connection, get_dict_cursor
from app.database.util import (
    GameType,
    TerminationParity,
    convert_country_codes,
    country_codes,
    title_to_desc,
)
from app.models.profile import (
    CompletionRateByCountry,
    CompletionRateByTitle,
    CountryDistribution,
    GameLengthByCountry,
    GameLengthByTitle,
    GameTerminationTypeByCountry,
    GameTerminationTypeByTitle,
    ResultCountsByCountry,
    ResultPercentagesByCountry,
    ResultPercentagesByTitle,
    TitleDescription,
    TitleDistribution,
    ResultCountsByTitle,
)


router = APIRouter()

dict_cursor = get_dict_cursor(get_db_connection())


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
                100 * AVG(wins / (wins+draws+losses)) as win_percentage,
                100 * AVG(draws / (wins+draws+losses)) as draw_percentage,
                100 * AVG(losses / (wins+draws+losses)) as loss_percentage
            FROM Player
            GROUP BY title
            """
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/title/results/counts",
    description="Get win/draw/loss counts by title.",
    response_model=ResultCountsByTitle,
)
async def result_counts_by_title():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT
                title,
                SUM(wins) as win_count,
                SUM(draws) as draw_count,
                SUM(losses) as loss_count
            FROM Player
            GROUP BY title
            ORDER BY -win_count
            """
        )
        result = cur.fetchall()
    return {"titles": result}


@router.get(
    "/title/completion-rate",
    description="Get statistics on game completion rate by title.",
    response_model=CompletionRateByTitle,
)
async def completion_rate_by_title(
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
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
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
                SELECT * FROM (
                    SELECT
                        p.title as title,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.result as result,
                        g.termination as termination,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT
                        p.title as title,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.result as result,
                        g.termination as termination,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.black_username = p.username
                ) t
                WHERE
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                t.title as title,
                AVG(t.completion_percentage) as avg_completion_rate,
                STDDEV(t.completion_percentage) as stddev_completion_rate
            FROM (
                SELECT
                    title,
                    AVG(
                        CASE WHEN termination = 'Resignation' AND (
                            (username = white_username AND result = '0-1')
                            OR (username = black_username AND result = '1-0')
                        ) THEN 0
                        ELSE 100 END
                    ) as completion_percentage
                FROM ProfileGame
                GROUP BY username, title
            ) t
            GROUP BY t.title
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
            },
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
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify a start date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify an end date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
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
                    UNION ALL
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
                        OR %(termination_parity)s = 'Win'
                            AND t.white_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'Loss'
                            AND t.white_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'Win'
                            AND t.black_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'Loss'
                            AND t.black_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'Draw' AND t.result = '1/2-1/2'
                    )
                    AND (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            ),
            ProfileGameCount as (
                SELECT username, COUNT(*) as count FROM ProfileGame
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
                    100 * COUNT(*) / c.count as percentage
                FROM ProfileGame g INNER JOIN ProfileGameCount c ON g.username = c.username
                GROUP BY g.username, c.count, g.title, g.termination
            ) t
            GROUP BY t.title, t.termination
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "termination_parity": termination_parity,
            },
        )
        flat_result = cur.fetchall()

    result = defaultdict(list)
    for r in flat_result:
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
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify a start date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify an end date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
                SELECT * FROM (
                    SELECT
                        p.title as title,
                        g.game_length as game_length,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT
                        p.title as title,
                        g.game_length as game_length,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.black_username = p.username
                ) t
                WHERE
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                title,
                AVG(game_length) as avg_game_length,
                STDDEV(game_length) as stddev_game_length
            FROM ProfileGame
            GROUP BY title
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        result = cur.fetchall()

    return {"titles": result}


# Countries


@router.get(
    "/country/distribution",
    description="Get the distribution of players by country.",
    response_model=CountryDistribution,
)
async def country_distribution():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT country, COUNT(*) as count
            FROM Player
            GROUP BY country
            """
        )
        result = cur.fetchall()
    return {"countries": convert_country_codes(result)}


@router.get(
    "/country/results",
    description="Get win/draw/loss percentages by country.",
    response_model=ResultPercentagesByCountry,
)
async def result_percentages_by_country():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT
                country,
                100 * AVG(wins / (wins+draws+losses)) as win_percentage,
                100 * AVG(draws / (wins+draws+losses)) as draw_percentage,
                100 * AVG(losses / (wins+draws+losses)) as loss_percentage
            FROM Player
            GROUP BY country
            ORDER BY -win_percentage
            """
        )
        result = cur.fetchall()
    return {"countries": convert_country_codes(result)}


@router.get(
    "/country/results/counts",
    description="Get win/draw/loss counts by country.",
    response_model=ResultCountsByCountry,
)
async def result_counts_by_country():
    with dict_cursor() as cur:
        cur.execute(
            """
            SELECT
                country,
                SUM(wins) as win_count,
                SUM(draws) as draw_count,
                SUM(losses) as loss_count
            FROM Player
            GROUP BY country
            ORDER BY -win_count
            """
        )
        result = cur.fetchall()
    return {"countries": convert_country_codes(result)}


@router.get(
    "/country/completion-rate",
    description="Get statistics on player ratings by country.",
    response_model=CompletionRateByCountry,
)
async def completion_rate_by_country(
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
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
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
                SELECT * FROM (
                    SELECT
                        p.country as country,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.result as result,
                        g.termination as termination,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT
                        p.country as country,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.result as result,
                        g.termination as termination,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.black_username = p.username
                ) t
                WHERE
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                t.country as country,
                AVG(t.completion_percentage) as avg_completion_rate,
                STDDEV(t.completion_percentage) as stddev_completion_rate
            FROM (
                SELECT
                    country,
                    AVG(
                        CASE WHEN termination = 'Resignation' AND (
                            (username = white_username AND result = '0-1')
                            OR (username = black_username AND result = '1-0')
                        ) THEN 0
                        ELSE 100 END
                    ) as completion_percentage
                FROM ProfileGame
                GROUP BY username, country
            ) t
            GROUP BY t.country
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        result = cur.fetchall()
    return {"countries": convert_country_codes(result)}


@router.get(
    "/country/termination-type",
    description="Get game termination type percentages by country.",
    response_model=GameTerminationTypeByCountry,
)
async def termination_type_by_country(
    termination_parity: Optional[TerminationParity] = Query(
        default=None,
        description="Optionally, specify the parity of the result (win, draw, or loss) from the perspective of the player from the relevant country.",  # noqa: E501
    ),
    game_type: Optional[GameType] = Query(
        default=None, description="Optionally, specify a game type to analyze."
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
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
                SELECT * FROM (
                    SELECT
                        p.country as country,
                        p.username as username,
                        g.white_username as white_username,
                        g.black_username as black_username,
                        g.termination as termination,
                        g.result as result,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT
                        p.country as country,
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
                        OR %(termination_parity)s = 'Win'
                            AND t.white_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'Loss'
                            AND t.white_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'Win'
                            AND t.black_username = t.username AND t.result = '0-1'
                        OR %(termination_parity)s = 'Loss'
                            AND t.black_username = t.username AND t.result = '1-0'
                        OR %(termination_parity)s = 'Draw' AND t.result = '1/2-1/2'
                    )
                    AND (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            ),
            ProfileGameCount as (
                SELECT username, COUNT(*) as count FROM ProfileGame
                GROUP BY username
            )
            SELECT
                t.country as country,
                t.termination as termination,
                AVG(t.percentage) as avg_percentage
            FROM (
                SELECT
                    g.country as country,
                    g.termination as termination,
                    100 * COUNT(*) / c.count as percentage
                FROM ProfileGame g INNER JOIN ProfileGameCount c ON g.username = c.username
                GROUP BY g.username, c.count, g.country, g.termination
            ) t
            GROUP BY t.country, t.termination
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
                "termination_parity": termination_parity,
            },
        )
        flat_result = cur.fetchall()

    result = defaultdict(list)
    for r in flat_result:
        result[r["country"]].append(
            {
                "termination_type": r["termination"],
                "percentage": r["avg_percentage"],
            }
        )

    return {
        "countries": [
            {"country": country_codes.get(country, country), "termination_types": result[country]}
            for country in result
        ],
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
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify a start date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
    end_date: Optional[str] = Query(
        default=None,
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="Optionally, specify an end date of games to analyze (inclusive), of the form YYYY-MM-DD (UTC).",  # noqa: E501
    ),
):
    with dict_cursor() as cur:
        cur.execute(
            """
            WITH ProfileGame as (
                SELECT * FROM (
                    SELECT
                        p.country as country,
                        g.game_length as game_length,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.white_username = p.username
                    UNION ALL
                    SELECT
                        p.country as country,
                        g.game_length as game_length,
                        g.category as category,
                        g.start_timestamp as start_timestamp
                    FROM Game g INNER JOIN Player p ON g.black_username = p.username
                ) t
                WHERE
                    (%(game_type)s IS NULL OR %(game_type)s = t.category)
                    AND (%(start_date)s IS NULL OR %(start_date)s <= DATE(t.start_timestamp))
                    AND (%(end_date)s IS NULL OR  DATE(t.start_timestamp) <= %(end_date)s)
            )
            SELECT
                country,
                AVG(game_length) as avg_game_length,
                STDDEV(game_length) as stddev_game_length
            FROM ProfileGame
            GROUP BY country
            """,
            {
                "game_type": game_type,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        result = cur.fetchall()
    return {"countries": convert_country_codes(result)}
