from app.config import settings
import pymysql


def get_db_connection():
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        port=settings.db_port,
        database=settings.db_name,
    )
