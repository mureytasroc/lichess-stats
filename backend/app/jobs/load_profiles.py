from app.data_helpers.get_games_files import get_games_files
import argparse
from app.database.connect import get_db_connection
from app.sql.statements import upsert_players
import re
import requests
import time
from datetime import datetime
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Load user profiles from https://lichess.org/api.")

parser.add_argument(
    "--batch-size",
    type=int,
    default=100,
    help=(
        "The number of usernames to load at once from game files. "
        "Regardless, profiles are always individually committed."
    ),
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


def get_profile(username):
    while True:
        response = requests.get(f"https://lichess.org/@/{username}")
        if response.status != 429:
            break
        print(f"Lichess API rate limit exceeded.")
        time.sleep(60)
    assert response.status_code == 200
    return response.json()


def parse_timestamp(ts):
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def load_usernames():
    global usernames_to_load

    with get_db_connection() as connection:
        for username in load_usernames:
            profile = get_profile(username)

            record = [username]

            record.append(profile["profile"]["firstName"] or None)
            record.append(profile["profile"]["lastName"] or None)
            record.append(profile["profile"]["bio"] or None)
            country = profile["profile"]["country"] or None
            assert country is None or len(country) == 2, f"Invalid country code: {country}"
            record.append(country)

            record.append(profile["profile"]["fideRating"] or None)
            record.append(profile["profile"]["uscfRating"] or None)
            record.append(profile["profile"]["ecfRating"] or None)
            record.append(profile["title"] or None)

            created_at = profile["createdAt"]
            assert created_at
            record.append(parse_timestamp(created_at))
            record.append(parse_timestamp(profile["seenAt"]) if profile["seenAt"] else None)

            rating_categories = [
                "ultraBullet",
                "bullet",
                "blitz",
                "rapid",
                "classical",
                "correspondence",
            ]
            rating_attributes = ["rating", "rd", "prog", "games"]
            record += [
                profile["perfs"][category][attribute]
                for category in rating_categories
                for attribute in rating_attributes
            ]

            record.append(profile["count"]["all"])
            record.append(profile["count"]["rated"])
            record.append(profile["count"]["win"])
            record.append(profile["count"]["loss"])
            record.append(profile["count"]["draw"])

            record.append(profile["completionRate"])
            record.append(profile["playTime"]["total"])
            record.append(profile["playTime"]["tv"])

            record.append(profile["patron"])
            record.append(profile["verified"])
            record.append(profile["tosViolation"])

            with connection.cursor() as cursor:
                cursor.execute(upsert_players, record)
            connection.commit()
        existing_usernames |= usernames_to_load
        usernames_to_load.clear()


username_re = re.compile(r'^\[?:(White|Black) "(\s+)"\]$')

for game_file_context in get_games_files(
    from_date=args.from_date, to_date=args.to_date, ascending=args.ascending
):
    with game_file_context() as game_file:
        print(f"Loading profiles...")
        for line in tqdm(game_file):
            match = username_re.match(line)
            if not match:
                continue
            username = match.group(1)
            if username in existing_usernames:
                continue
            usernames_to_load.add(username)
            if len(usernames_to_load) > args.batch_size:
                load_usernames()
