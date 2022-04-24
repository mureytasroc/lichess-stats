from datetime import datetime

from app.database.connect import get_db_connection


def min_game_date():
    """
    Returns the date of the earliest game in the database,
    in the form YYYY-MM-DD.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT MIN(start_timestamp) FROM Game")
            min_date = cursor.fetchone()[0]
            min_date = datetime.strptime(min_date).strftime("%Y-%m-%d")
        connection.commit()
        return min_date


def max_game_date():
    """
    Returns the date of the latest game in the database,
    in the form YYYY-MM-DD.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(start_timestamp) FROM Game")
            max_date = cursor.fetchone()[0]
            max_date = datetime.strptime(max_date).strftime("%Y-%m-%d")
        connection.commit()
        return max_date
