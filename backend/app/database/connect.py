from contextlib import contextmanager

import aiomysql
import pymysql

from app.config import settings


def get_db_connection():
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        port=settings.db_port,
        database=settings.db_name,
    )


def get_dict_cursor():
    """
    Given a database connection (as returned by `get_db_connection()`),
    return a dict cursor context manager that also auto-commits when the context is closed.
    Example usage:
    ```
    with dict_cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    ```
    """

    @contextmanager
    def dict_cursor():
        with get_db_connection() as db_connection:
            with db_connection.cursor(pymysql.cursors.DictCursor) as cur:
                yield cur
                db_connection.commit()

    return dict_cursor


def get_async_db_pool():
    return aiomysql.create_pool(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
    )
