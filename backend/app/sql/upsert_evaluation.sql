REPLACE INTO Evaluation (
     game_id,
     ply,
     eval,
     mate_in
  )
VALUES (%s, %s, %s, %s);