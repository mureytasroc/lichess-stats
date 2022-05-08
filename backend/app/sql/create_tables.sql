CREATE TABLE IF NOT EXISTS Player
  (
     username                  VARCHAR(32) PRIMARY KEY, -- get player url as f"https://lichess.org/@/{username}"
     profile_updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     
     first_name                VARCHAR(64),
     last_name                 VARCHAR(64),
     bio                       VARCHAR(1024),
     country                   VARCHAR(64),

     fide_rating               SMALLINT UNSIGNED,
     uscf_rating               SMALLINT UNSIGNED,
     ecf_rating                SMALLINT UNSIGNED,
     title                     ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM' , 'LM', 'BOT'),
     
     created_at                TIMESTAMP, -- timestamp of Lichess account creation
     seen_at                   TIMESTAMP, -- timestamp of last Lichess visit
     
     ultrabullet_rating        SMALLINT UNSIGNED, -- glicko2 rating
     ultrabullet_rd            SMALLINT UNSIGNED, -- glicko2 rating deviation
     ultrabullet_prog          SMALLINT, -- recent rating change
     ultrabullet_num_games     INT UNSIGNED, -- number of games played in this category

     bullet_rating             SMALLINT UNSIGNED, -- glicko2 rating
     bullet_rd                 SMALLINT UNSIGNED, -- glicko2 rating deviation
     bullet_prog               SMALLINT, -- recent rating change
     bullet_num_games          INT UNSIGNED, -- number of games played in this category

     blitz_rating              SMALLINT UNSIGNED, -- glicko2 rating
     blitz_rd                  SMALLINT UNSIGNED, -- glicko2 rating deviation
     blitz_prog                SMALLINT, -- recent rating change
     blitz_num_games           INT UNSIGNED, -- number of games played in this category

     rapid_rating              SMALLINT UNSIGNED, -- glicko2 rating
     rapid_rd                  SMALLINT UNSIGNED, -- glicko2 rating deviation
     rapid_prog                SMALLINT, -- recent rating change
     rapid_num_games           INT UNSIGNED, -- number of games played in this category

     classsical_rating         SMALLINT UNSIGNED, -- glicko2 rating
     classsical_rd             SMALLINT UNSIGNED, -- glicko2 rating deviation
     classsical_prog           SMALLINT, -- recent rating change
     classsical_num_games      INT UNSIGNED, -- number of games played in this category

     correspondence_rating     SMALLINT UNSIGNED, -- glicko2 rating
     correspondence_rd         SMALLINT UNSIGNED, -- glicko2 rating deviation
     correspondence_prog       SMALLINT, -- recent rating change
     correspondence_num_games  INT UNSIGNED, -- number of games played in this category
     
     num_games                 INT UNSIGNED NOT NULL, -- total number of games played
     num_rated                 INT UNSIGNED NOT NULL, -- total number of rated games played
     wins                      INT UNSIGNED NOT NULL,
     losses                    INT UNSIGNED NOT NULL,
     draws                     INT UNSIGNED NOT NULL,
     
     play_time                 INT UNSIGNED NOT NULL, -- total seconds played on lichess
     lichess_tv_time           INT UNSIGNED NOT NULL, -- total seconds displayed on lichess tv

     patron                    BOOLEAN NOT NULL,
     verified                  BOOLEAN NOT NULL,
     tos_violation             BOOLEAN NOT NULL -- user has violated lichess TOS
  );

CREATE TABLE EcoCode
(
    code                       CHAR(3) PRIMARY KEY,
    opening_name               VARCHAR(256),
    opening_moves              VARCHAR(512)
);

CREATE TABLE IF NOT EXISTS Game
  (
     lichess_id                CHAR(8) PRIMARY KEY, -- get game url as f"https://lichess.org/{lichess_id}"
     start_timestamp           TIMESTAMP NOT NULL,
     
     tournament_id             CHAR(8), -- if not null, get tournament url as f"https://lichess.org/tournament/{tournament_id}"
     category                  ENUM('UltraBullet', 'Bullet', 'Blitz', 'Rapid', 'Classical', 'Correspondence') NOT NULL,
     time_control_base         SMALLINT UNSIGNED, -- base time in seconds
     time_control_increment    TINYINT UNSIGNED, -- increment in seconds
     
     white_username            VARCHAR(32) NOT NULL, -- references Player(username) and indexed, but not FOREIGN KEY (profile may not be loaded)
     white_elo                 SMALLINT UNSIGNED NOT NULL, -- glicko2
     white_title               ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM' , 'LM', 'BOT'),
     
     black_username            VARCHAR(32) NOT NULL, -- references Player(username) and indexed, but not FOREIGN KEY (profile may not be loaded)
     black_elo                 SMALLINT UNSIGNED NOT NULL, -- glicko2
     black_title               ENUM('GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'CM', 'WCM', 'WNM' , 'LM', 'BOT'),
     
     opening_name              VARCHAR(256) NOT NULL, -- not necessarily the same as EcoCode.opening_name
     opening_eco               CHAR(3), -- less specific than opening_name

     game_length               DECIMAL(4, 1) NOT NULL, -- number of moves with 0.5 for half-moves (denormalized for performance)
     result                    ENUM('1-0', '0-1', '1/2-1/2') NOT NULL,
     termination               ENUM('Checkmate', 'Resignation', 'DrawAgreement', 'Stalemate', 'InsufficientMaterial', 'FiftyMoveRule', 'ThreefoldRepetition', 'SeventyFiveMoveRule', 'FivefoldRepetition', 'TimeForfeit', 'RulesInfraction') NOT NULL,
     white_rating_diff         SMALLINT, -- white's rating change from game
     black_rating_diff         SMALLINT, -- ^

     FOREIGN KEY (opening_eco) REFERENCES EcoCode(code)
  );

CREATE INDEX game_white_username_idx ON Game(white_username); -- TODO: turn into foreign key after data is loaded
CREATE INDEX game_black_username_idx ON Game(black_username); -- TODO: turn into foreign key after data is loaded


CREATE TABLE IF NOT EXISTS GameMove
  (
     game_id                   CHAR(8),
     ply                       SMALLINT UNSIGNED NOT NULL, -- 1-indexed (move number = (ply-1)//2+1, white move = odd ply)
     move_notation             VARCHAR(16) NOT NULL,
     
     PRIMARY KEY(game_id, ply),
     FOREIGN KEY (game_id) REFERENCES Game(lichess_id)
  );


CREATE TABLE IF NOT EXISTS Evaluation
  (
     game_id                   CHAR(8),
     ply                       SMALLINT UNSIGNED NOT NULL, -- 1-indexed (move number = (ply-1)//2+1, white move = odd ply)
     eval                      DECIMAL(5, 2), -- null if missing or forced mate found, otherwise centipawn/100
     mate_in                   TINYINT, -- number of PLIES to mate; negative for black, positive for white, null if no forced mate found
     
     PRIMARY KEY(game_id, ply),
     FOREIGN KEY (game_id) REFERENCES Game(lichess_id)
  );


CREATE TABLE IF NOT EXISTS TimeRemaining
  (
     game_id                   CHAR(8),
     move_num                  SMALLINT UNSIGNED NOT NULL, -- 1-indexed move number
     white_hundredths          INT UNSIGNED, -- hundredths of a second; null if missing or forced mate found
     black_hundredths          INT UNSIGNED, -- ^
     
     PRIMARY KEY(game_id, move_num),
     FOREIGN KEY (game_id) REFERENCES Game(lichess_id)
  );