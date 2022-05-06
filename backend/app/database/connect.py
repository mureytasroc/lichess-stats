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


def get_async_db_connection():
    return aiomysql.create_pool(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
    )
