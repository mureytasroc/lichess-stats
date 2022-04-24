from app.database.connect import get_db_connection
from app.sql.statements import create_tables


with get_db_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(create_tables)
    connection.commit()
