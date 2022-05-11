from typing import Dict

from app.database.util import title_to_desc


def enum_desc(desc_dict: Dict[str, str]) -> str:
    """
    Given a dictionary mapping enum value to description, generates a markdown
    table for displaying that enum description in documentation.
    """
    table = "|Value|Description|\n"
    table += "|-----" * 2 + "|\n"
    table += "\n".join([f"|{k}|{v}|" for k, v in desc_dict.items()])
    return table


tags_metadata = [
    {
        "name": "rating",
        "description": "Routes involving analysis of user ratings.",
    },
    {
        "name": "profile",
        "description": (
            "Routes involving analysis of user profile attributes.\n"
            f"A description of player title enum values:\n{enum_desc(title_to_desc)}"
        ),
    },
    {
        "name": "graph",
        "description": "Routes involving analysis of the graph of wins.",
    },
]
