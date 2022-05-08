import csv


def get_allowed_eco():
    with open("app/load_data_helpers/eco_code_to_name.csv") as f:
        return {row["eco_code"] for row in csv.DictReader(f, skipinitialspace=True)}
