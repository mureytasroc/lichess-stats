def load_sql(file_name: str) -> str:
    """
    Load SQL from a file.
    """
    with open(f"app/sql/{file_name}.sql", "r") as f:
        return f.read()


drop_tables = load_sql("drop_tables")
create_tables = load_sql("create_tables")

upsert_players = load_sql("upsert_players")

upsert_game = load_sql("upsert_game")
upsert_moves = load_sql("upsert_moves")
upsert_time_remaining = load_sql("upsert_time_remaining")
upsert_evaluation = load_sql("upsert_evaluation")
