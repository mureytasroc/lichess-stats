REPLACE INTO Evaluation (
     game_id,
     ply,
     eval,
     mate_in,
     depth
  )
VALUES (%s, %s, %s, %s, %s);