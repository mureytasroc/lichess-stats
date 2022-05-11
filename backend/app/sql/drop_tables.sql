DROP TABLE IF EXISTS GameMove;

DROP TABLE IF EXISTS Evaluation;

DROP TABLE IF EXISTS TimeRemaining;

DROP INDEX game_white_username_idx ON Game;
DROP INDEX game_black_username_idx ON Game;

DROP INDEX game_category_idx ON Game;
DROP INDEX game_start_timestamp_idx ON Game;
DROP INDEX game_result_idx ON Game;
DROP INDEX game_termination_idx ON Game;

DROP TABLE IF EXISTS Game;

DROP TABLE IF EXISTS EcoCode;

DROP INDEX profile_country_idx;
DROP INDEX profile_title_idx;

DROP TABLE IF EXISTS Player;
