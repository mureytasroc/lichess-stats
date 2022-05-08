REPLACE INTO Player (
     username,
     
     first_name,
     last_name,
     bio,
     country,

     fide_rating,
     uscf_rating,
     ecf_rating,
     title,
     
     created_at,
     seen_at,
     
     ultrabullet_rating,
     ultrabullet_rd,
     ultrabullet_prog,
     ultrabullet_num_games,

     bullet_rating,
     bullet_rd,
     bullet_prog,
     bullet_num_games,

     blitz_rating,
     blitz_rd,
     blitz_prog,
     blitz_num_games,

     rapid_rating,
     rapid_rd,
     rapid_prog,
     rapid_num_games,

     classsical_rating,
     classsical_rd,
     classsical_prog,
     classsical_num_games,

     correspondence_rating,
     correspondence_rd,
     correspondence_prog,
     correspondence_num_games,
     
     num_games,
     num_rated,
     wins,
     losses,
     draws,
     
     play_time,
     lichess_tv_time,

     patron,
     verified,
     tos_violation
  )
VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
