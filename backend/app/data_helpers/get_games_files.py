import requests
from decimal import *
from ..config import settings
import re
import os
import shutil
import contextlib
import bz2


extract_date_re = re.compile(
    r"^https:\/\/database\.lichess\.org\/standard\/lichess_db_standard_rated_(\s{7})\.pgn\.bz2$"
)


def download_game(game_url):
    """
    Downloads the file at the given URL to /tmp/filename
    and returns the local filepath.
    """
    os.makedirs("/tmp", exist_ok=True)
    filepath = "/tmp/" + game_url.split("/")[-1]
    with requests.get(game_url, stream=True) as r:
        with open(filepath, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return filepath


def get_games_files(from_date: str = None, to_date: str = None, ascending: bool = False):
    """
    A lazy generator of game files from database.lichess.org.
    Yields a context you can use to access the downloaded file:
    ```
    for game_file_context in get_games_files():
        with game_file_context() as game_file:
            for line in game_file:
                pass
    ```
    The context manager makes sure the file is deleted when you're done with it
    (these files are very large).
    :param str from_date: The date of the earliest file to get, of the form YYYY-MM.
    :param str to_date: The date of the latest file to get, of the form YYYY-MM.
    :param bool ascending: Whether to load files in ascending chronological order.
    """
    game_urls = requests.get(settings.games_index_url).text.splitlines()
    if ascending:
        game_urls = reversed(game_urls)
    for game_url in game_urls:
        game_url = game_url.strip()

        match = extract_date_re.match(game_url)
        assert match, f"Game url could not be parsed: {game_url}"
        date = match.group(1)

        if to_date and to_date < date:
            continue
        if from_date and from_date > date:
            break

        print(f"Downloading game file for {date}...")
        filepath = download_game(game_url)

        @contextlib.contextmanager
        def get_context():
            with bz2.open(filepath, "rt") as f:
                yield f
            os.remove(filepath)

        yield get_context
