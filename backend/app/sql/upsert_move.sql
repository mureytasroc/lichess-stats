REPLACE INTO GameMove (
     game_id,
     ply,
     move_notation
  )
VALUES (%s, %s, %s);