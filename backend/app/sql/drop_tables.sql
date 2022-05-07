DROP TABLE IF EXISTS GameMove;

DROP TABLE IF EXISTS Evaluation;

DROP TABLE IF EXISTS TimeRemaining;

DROP INDEX game_white_username_idx ON Game;
DROP INDEX game_black_username_idx ON Game;
DROP INDEX opening_eco_idx ON Game;

DROP TABLE IF EXISTS Game;

DROP TABLE IF EXISTS EcoCodes;

DROP TABLE IF EXISTS Player;
