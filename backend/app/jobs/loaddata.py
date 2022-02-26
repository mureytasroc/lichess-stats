import requests
from collections import deque
import pymysql
from decimal import *


headers = {
    "User-Agent": "cunningham3c@gmail.com (filling a db for finding win paths between players)"
}


mydb = pymysql.connect(
    host="chess-wins.ctd4memhbq4f.us-west-2.rds.amazonaws.com",
    user="admin",
    password=None,
    port=3306,
    database="chesswins",
)


def validate_player(profile, stats):
    if "avatar" in profile and len(profile["avatar"]) > 200:
        profile["avatar"] = None

    return (
        profile["username"].lower(),
        profile["url"],
        profile["name"][:100] if "name" in profile else None,
        profile.get("title"),
        profile.get("avatar"),
        profile["country"].split("/")[-1] if "country" in profile else None,
        profile.get("location"),
        profile.get("last_online"),
        profile.get("joined"),
        profile.get("followers"),
        profile.get("status"),
        profile.get("twitch_url"),
        stats.get("chess_rapid", {}).get("last", {}).get("rating"),
        stats.get("chess_rapid", {}).get("last", {}).get("date"),
        stats.get("chess_rapid", {}).get("last", {}).get("rd"),
        stats.get("chess_rapid", {}).get("best", {}).get("rating"),
        stats.get("chess_rapid", {}).get("best", {}).get("date"),
        stats.get("chess_rapid", {}).get("best", {}).get("game"),
        stats.get("chess_rapid", {}).get("record", {}).get("win"),
        stats.get("chess_rapid", {}).get("record", {}).get("loss"),
        stats.get("chess_rapid", {}).get("record", {}).get("draw"),
        stats.get("chess_blitz", {}).get("last", {}).get("rating"),
        stats.get("chess_blitz", {}).get("last", {}).get("date"),
        stats.get("chess_blitz", {}).get("last", {}).get("rd"),
        stats.get("chess_blitz", {}).get("best", {}).get("rating"),
        stats.get("chess_blitz", {}).get("best", {}).get("date"),
        stats.get("chess_blitz", {}).get("best", {}).get("game"),
        stats.get("chess_blitz", {}).get("record", {}).get("win"),
        stats.get("chess_blitz", {}).get("record", {}).get("loss"),
        stats.get("chess_blitz", {}).get("record", {}).get("draw"),
        stats.get("chess_bullet", {}).get("last", {}).get("rating"),
        stats.get("chess_bullet", {}).get("last", {}).get("date"),
        stats.get("chess_bullet", {}).get("last", {}).get("rd"),
        stats.get("chess_bullet", {}).get("best", {}).get("rating"),
        stats.get("chess_bullet", {}).get("best", {}).get("date"),
        stats.get("chess_bullet", {}).get("best", {}).get("game"),
        stats.get("chess_bullet", {}).get("record", {}).get("win"),
        stats.get("chess_bullet", {}).get("record", {}).get("loss"),
        stats.get("chess_bullet", {}).get("record", {}).get("draw"),
        stats.get("fide"),
        stats.get("tactics", {}).get("best", {}).get("rating"),
        stats.get("tactics", {}).get("best", {}).get("date"),
        stats.get("puzzle_rush", {}).get("best", {}).get("score"),
    )


def load_profile(username, commit=True):
    """
    Loads a row into the players table for the given username.
    commit: optionally specify whether to commit the changes to the database
    Returns True if the player was successfully loaded, None otherwise.
    """
    profile_res = requests.get(f"https://api.chess.com/pub/player/{username}/")
    stats_res = requests.get(f"https://api.chess.com/pub/player/{username}/stats/")
    if profile_res.status_code != 200 or stats_res.status_code != 200:
        if profile_res.status_code != 404:
            print(
                f"Error fetching profile for {username} (code {profile_res.status_code}): {profile_res.json()}"
            )
        if stats_res.status_code != 404:
            print(
                f"Error fetching stats for {username} (code {stats_res.status_code}): {stats_res.json()}"
            )
        return
    validated_player = validate_player(profile_res.json(), stats_res.json())
    if not validated_player:
        return
    with mydb.cursor() as cursor:
        cursor.execute(
            """
        INSERT INTO `Players` 
            (`username`, `url`, `name`, `title`, `photo_url`, `country`, `location`, `last_online_date`, `joined_date`, 
            `followers`, `status`, `streamer_url`, `rapid_rating`, `rapid_last_date`, `rapid_rd`, `rapid_best_rating`, 
            `rapid_best_rating_date`, `rapid_best_rating_url`, `rapid_wins`, `rapid_losses`, `rapid_draws`, `blitz_rating`, 
            `blitz_last_date`, `blitz_rd`, `blitz_best_rating`, `blitz_best_rating_date`, `blitz_best_rating_url`, `blitz_wins`, 
            `blitz_losses`, `blitz_draws`, `bullet_rating`, `bullet_last_date`, `bullet_rd`, `bullet_best_rating`, `bullet_best_rating_date`,
            `bullet_best_rating_url`, `bullet_wins`, `bullet_losses`, `bullet_draws`, `fide`, `tactics_best_rating`, 
            `tactics_best_rating_date`, `puzzle_rush_best`) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        """,
            validated_player,
        )
    if commit:
        mydb.commit()
    return True


def validate_game_sql(game):
    if len(game["pgn"]) >= 20000:
        return None
    return (
        game["url"],
        game["pgn"],
        game["time_class"],
        game["time_control"],
        game["end_time"],
        game["white"]["username"].lower(),
        game["white"]["rating"],
        game["white"]["result"],
        game.get("accuracies", {}).get("white"),
        game["black"]["username"].lower(),
        game["black"]["rating"],
        game["black"]["result"],
        game.get("accuracies", {}).get("black"),
    )


def get_opponent(game, username):
    """
    Gets the opponent of the given username in the given game.
    """
    return [
        uname
        for uname in [game["white"]["username"], game["black"]["username"]]
        if uname != username
    ][0]


def get_games(username, loaded_usernames, month=None, min_month=None, commit=True):
    """
    Gets all the games played by a given username.
    Profiles of opponents will be loaded into the database to satisfy foreign key constraints.
    Pass in a set of usernames that have already been loaded to avoid duplicates.
    month: optionally specify a specific month "YYYY/MM" to get games from
    min_month: optionally specify the minimum year/month of games to fetch (in the form "YYYY/MM")
    commit: optionally specify whether to commit the changes to the database
    Returns None if an error occured.
    """
    assert month is None or min_month is None
    games = []
    if not month:
        urls = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives").json()[
            "archives"
        ]
    else:
        urls = [f"https://api.chess.com/pub/player/{username}/games/{month}"]
    if min_month:
        urls = [
            url
            for url in urls
            if url >= f"https://api.chess.com/pub/player/{username}/games/{min_month}"
        ]

    for url in urls:
        res = requests.get(url)
        if res.status_code == 200:
            games += res.json()["games"]
        elif res.status_code != 404:
            print(f"Error fetching {url} (code {res.status_code}): {res.json()}")

    if not games:
        return

    if username not in loaded_usernames:
        if not load_profile(username, commit=False):
            return

    opponents = set()
    for game in games:
        opponents.add(get_opponent(validated_game, username))
    for opponent in opponents - loaded_usernames:
        if not load_profile(opponent, commit=False):
            opponents.remove(opponent)

    validated_games = []
    for game in games:
        validated_game = validate_game_sql(game)
        if validated_game is not None and get_opponent(game, username) in opponents:
            validated_games.append(validated_game)

    with mydb.cursor() as cursor:
        cursor.executemany(
            """
        INSERT IGNORE INTO `Games` 
            (`url`, `pgn`, `time_class`, `time_control`, `end_time`, `white_username`, 
            `white_rating`, `white_result`, `white_accuracy`, `black_username`, `black_rating`, 
            `black_result`, `black_accuracy`) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        """,
            validated_games,
        )

    if commit:
        mydb.commit()

    return games


def get_opponents(username, games):
    """
    Gets a set of the opponents a given username has played, among a list of played games.
    """
    opponents = set()
    for game in games:
        opponents.add(get_opponent(game, username))
    return opponents


def bfs_players(get_games, starting_usernames=None, max_games=None, max_depth=None):
    """
    get_games: provide a function to get the games of a given username
    starting_usernames: optionally specify a set of usernames consisting the root of the BFS
    max_depth: optionally specify the max depth the BFS can reach before terminating
    min_date: optionally specify the minimum year/month of games to consider (in the form "YYYY/MM")
    max_games: optionally specify the max number of total games to fetch
    """
    if starting_usernames is None:
        with mydb.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                """
            SELECT DISTINCT `username` FROM 
            `Players` p LEFT OUTER JOIN `Games` g 
            ON p.`username` = g.`white_username` OR p.`username` = g.`black_username` 
            WHERE g.`white_username` IS NULL AND g.`black_username` IS NULL
            """
            )
    usernames = set(starting_usernames)
    games = set()
    queue = deque([(username, 0) for username in starting_usernames])
    while len(queue) > 0:
        username, depth = queue.popleft()
        if max_depth is not None and depth > max_depth:
            print("Reached depth limit")
            break
        games_played = get_games(username, usernames)
        if games_played is None:
            continue
        games |= games_played
        for opponent in get_opponents(username, games_played):
            if opponent not in usernames:
                usernames.add(opponent)
                queue.append((opponent, depth + 1))
    return usernames
