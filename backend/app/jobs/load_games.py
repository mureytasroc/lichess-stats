import requests
from collections import deque
import pymysql
from decimal import *
from app.config import settings
import argparse
import gc


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
