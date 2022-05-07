INSERT IGNORE INTO Game (
     lichess_id,
     start_timestamp,
     
     tournament_id,
     category,
     time_control_base,
     time_control_increment,
     
     white_username,
     white_elo,
     white_title,
     
     black_username,
     black_elo,
     black_title,
     
     opening_name,
     opening_eco,
     
     result,
     termination,
     white_rating_diff,
     black_rating_diff
  )
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);