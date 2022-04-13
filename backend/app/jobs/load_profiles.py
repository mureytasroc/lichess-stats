from ..data_helpers.get_games_files import get_games_files
import argparse
from ..database.connect import get_db_connection
from ..sql.statements import upsert_players
import re

parser = argparse.ArgumentParser(description="Load user profiles from https://lichess.org/api.")

parser.add_argument(
    "--batch-size",
    type=int,
    default=100,
    help=("The number of users to load at once, in a single transaction."),
)

parser.add_argument(
    "--from-date",
    type=str,
    default=None,
    help=(
        "The date of the earliest game file to get usernames from, "
        "of the form YYYY-MM (defaults to the beginning of lichess's game history)."
    ),
)

parser.add_argument(
    "--to-date",
    type=str,
    default=None,
    help=(
        "The date of the latest game file to get usernames from, "
        "of the form YYYY-MM (defaults to the end of lichess's game history)."
    ),
)

parser.add_argument(
    "--ascending",
    type=str,
    action="store_true",
    help=(
        "Use this flag to load game files in ascending chronological order "
        "(default behavior is to load files in reverse chronological order)."
    ),
)

args = parser.parse_args()


def get_existing_usernames():
    """
    Loads the set of existing usernames from the Player table of the database.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM Player")
            usernames = {row[0] for row in cursor.fetchall()}
        connection.commit()
    return usernames


existing_usernames = get_existing_usernames()
usernames_to_load = set()


def load_usernames():
    global usernames_to_load
    player_tuples = []

    for username in load_usernames:
        pass

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(upsert_players, player_tuples)
        connection.commit()


username_re = re.compile(r'^\[?:(White|Black) "(\s+)"\]$')

for game_file_context in get_games_files(
    from_date=args.from_date, to_date=args.to_date, ascending=args.ascending
):
    with game_file_context() as game_file:
        for line in game_file:
            match = username_re.match(line)
            if not match:
                continue
            username = match.group(1)
            if username in existing_usernames:
                continue
            usernames_to_load.add(username)
            if len(usernames_to_load) > args.batch_size:
                load_usernames()
