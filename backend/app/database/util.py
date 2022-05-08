from typing import Optional
from fastapi_utils.enums import StrEnum
from enum import auto


class GameType(StrEnum):
    UltraBullet = auto()
    Bullet = auto()
    Blitz = auto()
    Rapid = auto()
    Classical = auto()
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
    ThreefoldRepetition = auto()
    RulesInfraction = auto()


class TerminationParity(StrEnum):
    Win = auto()
    Draw = auto()
    Loss = auto()
