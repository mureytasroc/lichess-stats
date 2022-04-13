from ..sql.statements import drop_tables
from ..database.connect import get_db_connection


with get_db_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(drop_tables)
    connection.commit()
