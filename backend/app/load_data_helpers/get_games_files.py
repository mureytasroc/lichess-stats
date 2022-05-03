import bz2
import contextlib
import os
import re
import shutil

import requests
from tqdm import tqdm

from app.config import settings


extract_date_re = re.compile(
    r"^^https:\/\/database\.lichess\.org\/standard\/lichess_db_standard_rated_(\d{4}\-\d{2})\.pgn\.bz2$"  # noqa: E501
)


def download_game(game_url):
    """
    Downloads the file at the given URL to /tmp/filename
    and returns local_filepath, already_downloaded
    """
    os.makedirs("/tmp", exist_ok=True)
    filepath = "/tmp/" + game_url.split("/")[-1]
    if os.path.exists(filepath):
        return filepath, True
    with requests.get(game_url, stream=True) as r:
        file_size = int(r.headers.get("Content-Length", 0)) or None
        with open(filepath, "wb") as f:
            with tqdm.wrapattr(r.raw, "read", total=file_size) as r_raw:
                shutil.copyfileobj(r_raw, f)
    return filepath, False


def get_games_files(
    from_date: str = None, to_date: str = None, ascending: bool = False, save_files: bool = False
):
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
    :param bool save_files: Whether to keep the downloaded files in /tmp.
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
        filepath, already_downloaded = download_game(game_url)

        @contextlib.contextmanager
        def get_context():
            with bz2.open(filepath, "rt") as f:
                yield f
            if not save_files and not already_downloaded:
                os.remove(filepath)

        yield get_context
