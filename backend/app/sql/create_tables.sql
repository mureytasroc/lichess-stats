CREATE TABLE IF NOT EXISTS Player (
    username VARCHAR(32) PRIMARY KEY, -- get player url as f"https://lichess.org/@/{username}"
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    bio VARCHAR(1024),
    country CHAR(2),

    created_at TIMESTAMP NOT NULL,
    seen_at TIMESTAMP,
    
    bullet_rating SMALLINT UNSIGNED, -- glicko2
    blitz_rating SMALLINT UNSIGNED, -- glicko2
    rapid_rating SMALLINT UNSIGNED, -- glicko2
    classsical_rating SMALLINT UNSIGNED, -- glicko2
    correspondence_rating SMALLINT UNSIGNED, -- glicko2

    fide_rating SMALLINT UNSIGNED,
    uscf_rating SMALLINT UNSIGNED,
    ecf_rating SMALLINT UNSIGNED,
    title ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM', 'LM', 'BOT'),

    patron BOOLEAN,
    verified BOOLEAN,
    tos_violation BOOLEAN, -- user has violated lichess TOS

    num_games INT UNSIGNED,
    num_rated INT UNSIGNED, -- number of rated games
    wins INT UNSIGNED,
    losses INT UNSIGNED,
    draws INT UNSIGNED,

    completion_rate TINYINT UNSIGNED, -- 0-100

    play_time INT UNSIGNED, -- total seconds played on lichess
    lichess_tv_time INT UNSIGNED, -- total seconds displayed on lichess tv
);


CREATE TABLE IF NOT EXISTS Game (
  lichess_id CHAR(8) PRIMARY KEY, -- get game url as f"https://lichess.org/{lichess_id}"
  
  tournament_id CHAR(8), -- if not null, get tournament url as f"https://lichess.org/tournament/{tournament_id}"
  category ENUM('Bullet', 'Blitz', 'Rapid', 'Classical', 'Correspondence') NOT NULL,
  start_timestamp TIMESTAMP NOT NULL,
  time_control_base TINYINT UNSIGNED, -- base time in minutes
  time_control_increment TINYINT UNSIGNED, -- increment in seconds
  
  white_username VARCHAR(32), -- NOT NULL FOREIGN KEY REFERENCES Player(username)
  white_elo SMALLINT UNSIGNED NOT NULL, -- glicko2
  white_title ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM', 'LM', 'BOT'),
  
  black_username VARCHAR(32), -- NOT NULL FOREIGN KEY REFERENCES Player(username)
  black_elo SMALLINT UNSIGNED NOT NULL, -- glicko2
  black_title ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM', 'LM', 'BOT'),
  
  opening_name VARCHAR(256) NOT NULL,
  opening_ec0 CHAR(3) NOT NULL, -- less specific than opening_name
  
  result ENUM('1-0', '0-1', '1/2-1/2') NOT NULL,
  termination ENUM('Checkmate', 'Resignation', 'Time forfeit', 'Abandoned', 'Rules infraction') NOT NULL,
  
  white_rating_diff SMALLINT, -- white's rating change from game
  black_rating_diff SMALLINT -- ^
);


CREATE TABLE IF NOT EXISTS Moves (
  game_id CHAR(8) FOREIGN KEY REFERENCES Game(lichess_id),
  ply SMALLINT UNSIGNED NOT NULL, -- 1-indexed (move number = ply//2, white move = odd ply)
  
  move_notation VARCHAR(16) NOT NULL,
  
  PRIMARY KEY(game_id, ply)
);


CREATE TABLE IF NOT EXISTS Evaluation (
  game_id CHAR(8) FOREIGN KEY REFERENCES Game(lichess_id),
  ply SMALLINT UNSIGNED NOT NULL, -- 1-indexed (move number = ply//2, white move = odd ply)
  
  eval DECIMAL(5,2), -- null if missing or forced mate found
  mate_in TINYINT, -- negative for black, positive for white, null if no forced mate found
  
  PRIMARY KEY(game_id, ply)
);


CREATE TABLE IF NOT EXISTS TimeRemaining (
  game_id CHAR(8) FOREIGN KEY REFERENCES Game(lichess_id),
  move_num SMALLINT UNSIGNED NOT NULL, -- move number
  
  white_hundredths INT UNSIGNED, -- hundredths of a second; null if missing or forced mate found
  black_hundredths INT UNSIGNED, -- ^
  
  PRIMARY KEY(game_id, move_num)
);
