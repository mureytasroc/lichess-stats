from enum import Enum


class GameType(str, Enum):
    ultrabullet = "ultrabullet"
    bullet = "bullet"
    blitz = "blitz"
    rapid = "rapid"
    classsical = "classical"
    correspondence = "correspondence"


class RatingType(str, Enum):
    ultrabullet = "ultrabullet"
    bullet = "bullet"
    blitz = "blitz"
    rapid = "rapid"
    classsical = "classical"
    correspondence = "correspondence"
    fide = "fide"
    uscf = "uscf"
    ecf = "ecf"


class Title(str, Enum):
    GM = "GM"
    WGM = "WGM"
    IM = "IM"
    WIM = "WIM"
    FM = "FM"
    WFM = "WFM"
    NM = "NM"
    CM = "CM"
    WCM = "WCM"
    WNM = "WNM"
    LM = "LM"
    BOT = "BOT"


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

categories = {
    "Bullet",
    "Blitz",
    "Rapid",
    "Classical",
    "Correspondence",
    "UltraBullet",
}
