from typing import Optional
from fastapi_utils.enums import StrEnum
from enum import auto


class GameType(StrEnum):
    UltraBullet = auto()
    Bullet = auto()
    Blitz = auto()
    Rapid = auto()
    Classsical = auto()
    Correspondence = auto()


class RatingType(StrEnum):
    UltraBullet = auto()
    Bullet = auto()
    Blitz = auto()
    Rapid = auto()
    Classsical = auto()
    Correspondence = auto()
    FIDE = auto()
    USCF = auto()
    ECF = auto()


class Title(StrEnum):
    GM = auto()
    WGM = auto()
    IM = auto()
    WIM = auto()
    FM = auto()
    WFM = auto()
    NM = auto()
    CM = auto()
    WCM = auto()
    WNM = auto()
    LM = auto()
    BOT = auto()


title_to_desc = {
    "GM": "Grandmaster",
    "WGM": "Woman Grandmaster",
    "IM": "International Master",
    "WIM": "Woman International Master",
    "FM": "FIDE Master",
    "WFM": "Woman FIDE Master",
    "NM": "National Master",
    "CM": "Candidate Master (FIDE)",
    "WCM": "Woman Candidate Master (FIDE)",
    "WNM": "Woman National Master",
    "LM": "Lichess Master",
    "BOT": "Bot Account",
}


class TerminationType(StrEnum):
    Resignation = auto()
    DrawAgreement = auto()
    TimeForfeit = auto()
    Checkmate = auto()
    Stalemate = auto()
    InsufficientMaterial = auto()
    SeventyFiveMoveRule = auto()
    FivefoldRepetition = auto()
    FiftyMoveRule = auto()
    ThreeFoldRepetition = auto()
    RulesInfraction = auto()


class TerminationParity(StrEnum):
    Win = auto()
    Draw = auto()
    Loss = auto()


def exclusive_end_date(end_date: Optional[str]):
    """
    Converts the given nullable `end_date` from an inclusive format
    to exclusive (e.g '2022-04' to '2022-05'), or returns None if None.
    Assumes the `end_date` has already been validated to have the format
    YYYY-MM if it is not None.

    :param end_date: the date to convert to exclusive, of the form YYYY-MM or None.
    """
    if end_date is None:
        return None
    end_year, end_month = map(int, end_date.split("-"))
    if end_month == 12:
        end_date = f"{end_year+1}-1"
    else:
        end_date = f"{end_year}-{end_month+1}"


def game_type_case(game_type: Optional[str]):
    """
    Converts the given nullable `game_type` to the proper casing to match
    with the `category` column in the `Game` table of the DB.

    :param game_type: the game type to convert to the proper case
    """
    if game_type is None:
        return None
    game_type = game_type.lower().title()
    if game_type == "Ultrabullet":
        return "UltraBullet"
    return game_type
