from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "ChessWins.net"

    games_index_url: str = "https://database.lichess.org/standard/list.txt"

    db_host: str = os.environ["DB_HOST"]
    db_port: int = int(os.environ["DB_PORT"])
    db_user: str = os.environ["DB_USER"]
    db_password: str = os.environ["DB_PASSWORD"]
    db_name: str = os.environ["DB_NAME"]


settings = Settings()
