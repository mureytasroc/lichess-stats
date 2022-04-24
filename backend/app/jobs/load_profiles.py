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

parser.add_argument(
    "--save-files",
    action="store_true",
    help=(
        "Use this flag to prevent game files from being deleted from the /tmp directory "
        "after being downloaded (to speed up future runs)."
    ),
)

args = parser.parse_args()


assert args.batch_size > 0


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
        response = requests.get(f"https://lichess.org/api/user/{username}")
        if response.status_code != 429:
            break
        print(f"Lichess API rate limit exceeded.")
        time.sleep(60)
    return response.json(), response.status_code


def parse_timestamp(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")


def load_usernames(pbar):
    global existing_usernames
    global usernames_to_load

    with get_db_connection() as connection:
        for username in usernames_to_load:
            profile, response_code = get_profile(username)

            if response_code != 200:
                print(f"Error loading profile for {username}: {response_code}")
                continue

            profile["profile"] = profile.get("profile", dict())
            profile["perfs"] = profile.get("perfs", dict())
            profile["count"] = profile.get("count", dict())
            profile["playTime"] = profile.get("playTime", dict())

            record = [username]

            record.append(profile["profile"].get("firstName") or None)
            record.append(profile["profile"].get("lastName") or None)
            record.append(profile["profile"].get("bio") or None)
            record.append(profile["profile"].get("country") or None)

            record.append(profile["profile"].get("fideRating"))
            record.append(profile["profile"].get("uscfRating"))
            record.append(profile["profile"].get("ecfRating"))
            record.append(profile.get("title"))

            record.append(parse_timestamp(profile["seenAt"]) if profile.get("createdAt") else None)
            record.append(parse_timestamp(profile["seenAt"]) if profile.get("seenAt") else None)

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
                profile["perfs"].get(category, dict()).get(attribute)
                for category in rating_categories
                for attribute in rating_attributes
            ]

            record.append(profile["count"].get("all", 0))
            record.append(profile["count"].get("rated", 0))
            record.append(profile["count"].get("win", 0))
            record.append(profile["count"].get("loss", 0))
            record.append(profile["count"].get("draw", 0))

            record.append(profile.get("completionRate"))
            record.append(profile["playTime"].get("total", 0))
            record.append(profile["playTime"].get("tv", 0))

            record.append(profile.get("patron", False))
            record.append(profile.get("verified", False))
            record.append(profile.get("tosViolation", False))

            with connection.cursor() as cursor:
                cursor.execute(upsert_players, tuple(record))
            connection.commit()
            pbar.update(1)
        existing_usernames |= usernames_to_load
        usernames_to_load.clear()


username_re = re.compile(r'^\[(?:White|Black) "(.+)"\]$')

for game_file_context in get_games_files(
    from_date=args.from_date,
    to_date=args.to_date,
    ascending=args.ascending,
    save_files=args.save_files,
):
    with game_file_context() as game_file:
        print(f"Loading profiles...")
        with tqdm() as pbar:
            for line in game_file:
                match = username_re.match(line)
                if not match:
                    continue
                username = match.group(1)
                if username in existing_usernames:
                    continue
                usernames_to_load.add(username)
                if len(usernames_to_load) >= args.batch_size:
                    load_usernames(pbar)
