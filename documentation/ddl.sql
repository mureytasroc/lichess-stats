CREATE DATABASE chesswins;
USE chesswins;

CREATE TABLE Players
(
    username                 varchar(50) PRIMARY KEY,
    url                      varchar(100),
    name                     varchar(100),
    title                    varchar(10),
    photo_url                varchar(200),
    country                  varchar(5),
    location                 varchar(100),
    last_online_date         int,
    joined_date              int,
    followers                int,
    status                   varchar(50),
    streamer_url             varchar(100),
    rapid_rating             int,
    rapid_last_date          int,
    rapid_rd                 int,
    rapid_best_rating        int,
    rapid_best_rating_date   int,
    rapid_best_rating_url    varchar(100),
    rapid_wins               int,
    rapid_losses             int,
    rapid_draws              int,
    blitz_rating             int,
    blitz_last_date          int,
    blitz_rd                 int,
    blitz_best_rating        int,
    blitz_best_rating_date   int,
    blitz_best_rating_url    varchar(100),
    blitz_wins               int,
    blitz_losses             int,
    blitz_draws              int,
    bullet_rating            int,
    bullet_last_date         int,
    bullet_rd                int,
    bullet_best_rating       int,
    bullet_best_rating_date  int,
    bullet_best_rating_url   varchar(100),
    bullet_wins              int,
    bullet_losses            int,
    bullet_draws             int,
    fide                     int,
    tactics_best_rating      int,
    tactics_best_rating_date int,
    puzzle_rush_best         int
);

CREATE TABLE Games
(
    url                      varchar(100) PRIMARY KEY,
    pgn                      TEXT,
    time_class               varchar(20),
    time_control             int,
    end_time                 int,
    white_username           varchar(50),
    white_rating             int,
    white_result             varchar(20),
    white_accuracy           DECIMAL(2,2),
    black_username           varchar(50),
    black_rating             int,
    black_result             varchar(20),
    black_accuracy           DECIMAL(2,2),

    FOREIGN KEY (white_username)
      REFERENCES Players(username),

    FOREIGN KEY (black_username)
      REFERENCES Players(username)
);

--- Makes profile creation a lot harder and prob isn't that useful:
--- ALTER TABLE Players ADD CONSTRAINT fk_rapid_best_rating_url FOREIGN KEY (rapid_best_rating_url) REFERENCES Games(url);
--- ALTER TABLE Players ADD CONSTRAINT fk_blitz_best_rating_url FOREIGN KEY (blitz_best_rating_url) REFERENCES Games(url);
--- ALTER TABLE Players ADD CONSTRAINT fk_bullet_best_rating_url FOREIGN KEY (bullet_best_rating_url) REFERENCES Games(url);
