from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ChessWins.net"

    games_index_url: str = "https://database.lichess.org/standard/list.txt"

    db_host: str = "chess-wins.ctd4memhbq4f.us-west-2.rds.amazonaws.com"
    db_port: int = 3306
    db_user: str = "admin"
    db_password: str = None
    db_name: str = "chesswins"


settings = Settings()
