import argparse
import gc
from collections import deque
from decimal import *

import pymysql
import requests

from app.config import settings


parser = argparse.ArgumentParser(description="Process some integers.")


headers = {"User-Agent": "cunningham3c@gmail.com"}


mydb = pymysql.connect(
    host=settings.db_host,
    user=settings.db_user,
    password=settings.db_password,
    port=settings.db_port,
    database=settings.db_name,
)

GAMES_RE = None

games_urls = requests.get(settings.games_index_url).text.splitlines()

# for game_match in GAMES_RE.finditer(requests.get(settings.games_index_url).text):
