import argparse
import asyncio
import re
import selectors
from datetime import datetime

import aiohttp
from tqdm import tqdm

from app.database.connect import get_async_db_pool, get_db_connection
from app.load_data_helpers.get_games_files import get_games_files
from app.sql.statements import upsert_player


parser = argparse.ArgumentParser(description="Load user profiles from https://lichess.org/api.")

parser.add_argument(
    "--queue-limit",
    "-q",
    type=int,
    default=100,
    help=(
        "The max size of the username and profile queues (used for concurrent processing/loading)."
    ),
)

parser.add_argument(
    "--num-profile-consumers",
    "-c",
    type=int,
    default=1,
    help=("The number of profile consumer tasks (committing profiles to the db)."),
)

parser.add_argument(
    "--num-workers",
    "-w",
    type=int,
    default=1,
    help=("The number of workers (on different computers) to use."),
)

parser.add_argument(
    "--worker-num",
    "-n",
    type=int,
    default=0,
    help=("The number of this machine's worker, in the range [0..worker_num)."),
)

args = parser.parse_args()


assert args.queue_limit > 0
assert args.num_profile_consumers > 0
assert args.num_workers > 0
assert 0 <= args.worker_num < args.num_workers


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


def get_games_db_usernames():
    """
    Loads the set of usernames from the Game table of the database.
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT white_username FROM Game UNION SELECT black_username FROM Game")
            game_usernames = {row[0] for row in cursor.fetchall()}
        connection.commit()
    return game_usernames


existing_usernames = get_existing_usernames()


username_re = re.compile(r'^\[(?:White|Black) "(.+)"\]$')


async def username_producer(username_queue):
    while True:
        no_new_usernames = True
        for i, username in enumerate(get_games_db_usernames()):
            existing_usernames.add(username)
            if i % args.num_workers != args.worker_num:
                continue
            no_new_usernames = False
            await username_queue.put(username)
        if no_new_usernames:
            break
    await username_queue.put(None)


async def get_profile(session, username):
    while True:
        try:
            async with session.get(f"https://lichess.org/api/user/{username}") as response:
                response_json = await response.json()
                response_code = response.status
                if response_code == 429:
                    tqdm.write("Lichess API rate limit exceeded.")
                    await asyncio.sleep(60)
                    continue
                if response_code != 200:
                    tqdm.write(f"Error loading profile for {username}: {response_code}.")
                    return None, None
                return response_json, response_code
        except aiohttp.client_exceptions.ServerDisconnectedError:
            tqdm.write(f"Server disconnected for {username}.")
            return None, None
        except aiohttp.client_exceptions.ContentTypeError:
            tqdm.write(f"Content-Type error for {username}.")
            return None, None
        except asyncio.TimeoutError:
            tqdm.write(f"Timeout error for {username}.")
            return None, None


def parse_timestamp(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")


async def profile_producer(username_queue, profile_queue):
    async with aiohttp.ClientSession() as session:
        while True:
            username = await username_queue.get()
            if username is None:
                await profile_queue.put(None)
                break

            profile, response_code = await get_profile(session, username)
            if response_code is None:
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

            record.append(profile["playTime"].get("total", 0))
            record.append(profile["playTime"].get("tv", 0))

            record.append(profile.get("patron", False))
            record.append(profile.get("verified", False))
            record.append(profile.get("tosViolation", False))

            await profile_queue.put(tuple(record))


async def profile_consumer(queue, pbar):
    pool = await get_async_db_pool()

    async with pool.acquire() as conn:
        while True:
            tup = await queue.get()
            if tup is None:
                break
            async with conn.cursor() as cur:
                await cur.execute(upsert_player, tup)
            await conn.commit()
            pbar.update(1)

    pool.close()
    await pool.wait_closed()


async def load_profiles():
    username_queue = asyncio.Queue(maxsize=args.queue_limit)
    profile_queue = asyncio.Queue(maxsize=args.queue_limit)
    with tqdm() as pbar:
        username_producer_task = asyncio.create_task(username_producer(username_queue))
        profile_producer_task = asyncio.create_task(profile_producer(username_queue, profile_queue))
        profile_consumer_tasks = [
            asyncio.create_task(profile_consumer(profile_queue, pbar))
            for _ in range(args.num_profile_consumers)
        ]

        await asyncio.gather(
            username_producer_task,
            profile_producer_task,
            *profile_consumer_tasks,
        )
        await username_queue.join()
        await profile_queue.join()


selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
asyncio.run(load_profiles())
