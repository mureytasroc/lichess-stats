def load_sql(file_name: str) -> str:
    """
    Load SQL from a file.
    """
    with open(file_name + ".sql", "r") as f:
        return f.read()


drop_tables = load_sql("drop_tables")
create_tables = load_sql("create_tables")
