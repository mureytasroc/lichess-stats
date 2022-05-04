REPLACE INTO TimeRemaining (
     game_id,
     move_num,
     white_hundredths,
     black_hundredths
  )
VALUES (%s, %s, %s, %s);