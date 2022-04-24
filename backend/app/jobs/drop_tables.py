from app.database.connect import get_db_connection
from app.sql.statements import drop_tables


with get_db_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(drop_tables)
    connection.commit()
