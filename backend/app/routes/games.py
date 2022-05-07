from multiprocessing import connection
from statistics import mode
from tokenize import String
from typing import Optional

from fastapi import APIRouter, Path, Query

from app.database.util import GameType
from app.models.games import *
from app.models.profile import CountryDistribution
import pymysql.cursors
router = APIRouter()
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


connection = pymysql.connect(host='chess-db.ccwnen4yavww.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='aaaaaaaa',
                             database='chesswins',
                             cursorclass=pymysql.cursors.DictCursor)



@router.get(
    "/CastlingPercentage",
    description="Get the distribution of players by country.",  # noqa: E,
)
async def castle(username: Optional[str] = None):
    curr = connection.cursor()
    if not username:
        sql = '''WITH player_game AS (SELECT username, lichess_id FROM
                    Player JOIN Game on Player.username = Game.white_username
                        UNION ALL SELECT username, lichess_id FROM
                    Player JOIN Game on Player.username = Game.black_username
                    ),
            total_games AS (SELECT username, COUNT(lichess_id) as total FROM
            player_game GROUP BY username),
            castleOnly AS (SELECT DISTINCT game_id FROM Moves
            WHERE move_notation IN ('O-O', 'O-O-O')),
            game_moves_castle AS (SELECT username, COUNT(DISTINCT game_id) as castle FROM (
            player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
            ) GROUP BY username)
            SELECT total_games.username, castle*100/(total) as "Castling Percentage"  FROM (
            game_moves_castle JOIN total_games ON game_moves_castle.username = total_games.username
            );'''
    else:
        sql = '''
        WITH player_game AS (SELECT username, lichess_id FROM
                    Player JOIN Game on Player.username = Game.white_username
                        UNION ALL SELECT username, lichess_id FROM
                    Player JOIN Game on Player.username = Game.black_username
                    ),
            total_games AS (SELECT username, COUNT(lichess_id) as total FROM
            player_game GROUP BY username),
            castleOnly AS (SELECT DISTINCT game_id FROM Moves
            WHERE move_notation IN ('O-O', 'O-O-O')),
            game_moves_castle AS (SELECT username, COUNT(DISTINCT game_id) as castle FROM (
            player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
            ) GROUP BY username)
            SELECT total_games.username, castle*100/(total) as "Castling Percentage"  FROM (
            game_moves_castle JOIN total_games ON game_moves_castle.username = total_games.username
            ) WHERE total_games.username = \'''' + username + "\' ; "
    
    print(sql)
    curr.execute(sql)
    result = curr.fetchall()
    print(result)
    #print(sql)
    return {JSONResponse(content=jsonable_encoder(result))}

@router.get(
    "/RatioKtoQ",
    description="Ratio of King to Queen Castling." # noqa: E,
)
async def ratio(username: Optional[str] = None):
    curr = connection.cursor()
    if not username:
        sql = '''WITH player_game AS (SELECT username, lichess_id FROM
              Player JOIN Game on Player.username = Game.white_username
                   UNION ALL SELECT username, lichess_id FROM
              Player JOIN Game on Player.username = Game.black_username
                  ),
     castleOnly AS (SELECT DISTINCT game_id, move_notation FROM Moves
    WHERE move_notation IN ('O-O', 'O-O-O')),
    castle_king AS (SELECT username, COUNT(DISTINCT game_id) as king FROM (
    player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
    ) WHERE move_notation  = 'O-O'
    GROUP BY username
        HAVING king > 0),
  castle_queen AS (SELECT username, COUNT(DISTINCT game_id) as queen FROM (
    player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
    ) WHERE move_notation  = 'O-O-O'
  GROUP BY username
      HAVING queen > 0)
     SELECT castle_king.username, king/queen as "Ratio of King to Queen Castling"  FROM (
     castle_king JOIN castle_queen ON castle_king.username = castle_queen.username
    );'''
    else:
        sql = '''
        WITH player_game AS (SELECT username, lichess_id FROM
              Player JOIN Game on Player.username = Game.white_username
                   UNION ALL SELECT username, lichess_id FROM
              Player JOIN Game on Player.username = Game.black_username
                  ),
     castleOnly AS (SELECT DISTINCT game_id, move_notation FROM Moves
    WHERE move_notation IN ('O-O', 'O-O-O')),
    castle_king AS (SELECT username, COUNT(DISTINCT game_id) as king FROM (
    player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
    ) WHERE move_notation  = 'O-O'
    GROUP BY username
        HAVING king > 0),
  castle_queen AS (SELECT username, COUNT(DISTINCT game_id) as queen FROM (
    player_game JOIN castleOnly on player_game.lichess_id = castleOnly.game_id
    ) WHERE move_notation  = 'O-O-O'
  GROUP BY username
      HAVING queen > 0)
     SELECT castle_king.username, king/queen as "Ratio of King to Queen Castling"  FROM (
     castle_king JOIN castle_queen ON castle_king.username = castle_queen.username
    ) WHERE castle_king.username = \'''' + username + "\' ; "
    
    print(sql)
    curr.execute(sql)
    result = curr.fetchall()
    print(result)
    return {JSONResponse(content=jsonable_encoder(result))}


@router.get(
    "/CountryWinPercent",
    description="Descending order of Country Win Percentages",  # noqa: E,
)

async def win_percent():
    curr = connection.cursor()
    sql = '''SELECT  Country, SUM(wins)*100/ (SUM(losses) + SUM(wins)) as Win_Percentage FROM Player
WHERE Country is not NULL
GROUP BY Country
ORDER BY Win_Percentage DESC;'''
    print(sql)
    curr.execute(sql)
    result = curr.fetchall()
    print(result)
    #print(sql)
    return {JSONResponse(content=jsonable_encoder(result))}


@router.get(
    "/totalWins",
    description="Descending order of Country Win Percentages",  # noqa: E,
)

async def total_wins():
    curr = connection.cursor()
    sql = '''SELECT Country, SUM(num_games) as Total_Games FROM Player
WHERE Country is not NULL
GROUP BY Country
ORDER BY Total_Games DESC;'''
    print(sql)
    curr.execute(sql)
    result = curr.fetchall()
    print(result)
    #print(sql)
    return {JSONResponse(content=jsonable_encoder(result))}


router.get(
    "/totalWins",
    description="Descending order of Country Win Percentages",  # noqa: E,
)

async def total_wins():
    curr = connection.cursor()
    sql = '''SELECT Country, SUM(num_games) as Total_Games FROM Player
WHERE Country is not NULL
GROUP BY Country
ORDER BY Total_Games DESC;'''
    print(sql)
    curr.execute(sql)
    result = curr.fetchall()
    print(result)
    #print(sql)
    return {JSONResponse(content=jsonable_encoder(result))}



@router.get(
    "/AvgTimeToWin",
    description="Ratio of King to Queen Castling." # noqa: E,
)
async def ratio(username: Optional[str] = None):
    curr = connection.cursor()
    if not username:
        sql = '''WITH player_game_white AS (SELECT DISTINCT username, lichess_id FROM
              Player CROSS JOIN Game on Player.username = Game.white_username
            where result = '1-0'),
     white_time AS (SELECT username, lichess_id, (MAX(white_hundredths) - MIN(white_hundredths)) as time FROM
         player_game_white JOIN TimeRemaining on player_game_white.lichess_id = TimeRemaining.game_id
         GROUP BY username, lichess_id
         ),
    player_game_black AS (SELECT DISTINCT username, lichess_id,result FROM
              Player JOIN Game on Player.username = Game.black_username
        where result = '0-1'
    ),
     black_time AS (SELECT username, game_id, (MAX(black_hundredths) - MIN(black_hundredths)) as time FROM
         player_game_black JOIN TimeRemaining on player_game_black.lichess_id = TimeRemaining.game_id
         GROUP BY username, game_id
       ),
  time_union as (SELECT * FROM white_time UNION ALL SELECT * FROM black_time)
SELECT username, AVG(time) as "Average Time to Win"
FROM time_union
GROUP BY username;'''
    else:
        sql = '''
        WITH player_game_white AS (SELECT DISTINCT username, lichess_id FROM
              Player CROSS JOIN Game on Player.username = Game.white_username
            where result = '1-0'),
     white_time AS (SELECT username, lichess_id, (MAX(white_hundredths) - MIN(white_hundredths)) as time FROM
         player_game_white JOIN TimeRemaining on player_game_white.lichess_id = TimeRemaining.game_id
         GROUP BY username, lichess_id
         ),
    player_game_black AS (SELECT DISTINCT username, lichess_id,result FROM
              Player JOIN Game on Player.username = Game.black_username
        where result = '0-1'
    ),
     black_time AS (SELECT username, game_id, (MAX(black_hundredths) - MIN(black_hundredths)) as time FROM
         player_game_black JOIN TimeRemaining on player_game_black.lichess_id = TimeRemaining.game_id
         GROUP BY username, game_id
       ),
  time_union as (SELECT * FROM white_time UNION ALL SELECT * FROM black_time)
SELECT username, AVG(time) as "Average Time to Win"
FROM time_union
WHERE username = \'''' + username + "\' ; "
    
    curr.execute(sql)
    result = curr.fetchall()
    return {JSONResponse(content=jsonable_encoder(result))}