from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


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
    Classical = auto()
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


def get_rating_col(rating_type):
    return rating_type.lower() + "_rating"


country_codes = {
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua & Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AN": "Netherlands Antilles",
    "AO": "Angola",
    "AQ": "Antarctica",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BN": "Brunei Darussalam",
    "BO": "Bolivia",
    "BR": "Brazil",
    "BS": "Bahama",
    "BT": "Bhutan",
    "BU": "Burma (no longer exists)",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CF": "Central African Republic",
    "CG": "Congo",
    "CH": "Switzerland",
    "CI": "Côte D'ivoire (Ivory Coast)",
    "CK": "Cook Iislands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CS": "Czechoslovakia (no longer exists)",
    "CU": "Cuba",
    "CV": "Cape Verde",
    "CX": "Christmas Island",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DD": "German Democratic Republic (no longer exists)",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "EU": "European Union",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands (Malvinas)",
    "FM": "Micronesia",
    "FO": "Faroe Islands",
    "FR": "France",
    "FX": "France, Metropolitan",
    "GA": "Gabon",
    "GB": "United Kingdom (Great Britain)",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard & McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Islamic Republic of Iran",
    "IS": "Iceland",
    "IT": "Italy",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "St. Kitts and Nevis",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Lao People's Democratic Republic",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libyan Arab Jamahiriya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova, Republic of",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "ML": "Mali",
    "MN": "Mongolia",
    "MM": "Myanmar",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Monserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NT": "Neutral Zone (no longer exists)",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "St. Pierre & Miquelon",
    "PN": "Pitcairn",
    "PR": "Puerto Rico",
    "PS": "Palestine",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "St. Helena",
    "SI": "Slovenia",
    "SJ": "Svalbard & Jan Mayen Islands",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "ST": "Sao Tome & Principe",
    "SU": "Union of Soviet Socialist Republics (no longer exists)",
    "SV": "El Salvador",
    "SY": "Syrian Arab Republic",
    "SZ": "Swaziland",
    "TC": "Turks & Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TP": "East Timor",
    "TR": "Turkey",
    "TT": "Trinidad & Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan, Province of China",
    "TZ": "Tanzania, United Republic of",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UM": "United States Minor Outlying Islands",
    "US": "United States of America",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Vatican City State (Holy See)",
    "VC": "St. Vincent & the Grenadines",
    "VE": "Venezuela",
    "VG": "British Virgin Islands",
    "VI": "United States Virgin Islands",
    "VN": "Viet Nam",
    "VU": "Vanuatu",
    "WF": "Wallis & Futuna Islands",
    "WS": "Samoa",
    "XK": "Kosovo",
    "YD": "Democratic Yemen (no longer exists)",
    "YE": "Yemen",
    "YT": "Mayotte",
    "YU": "Yugoslavia",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZR": "Zaire",
    "ZW": "Zimbabwe",
    "_united-nations": "United Nations",
    "_earth": "Earth",
    "_lichess": "Lichess",
    "_belarus-wrw": "Belarus WRW",
    "GB-SCT": "Scotland",
    "GB-ENG": "England",
    "_russia-wbw": "Russia WBW",
    "TL": "East Timor",
    "_adygea": "Adygea",
    "MK": "North Macedonia",
    "AX": "Åland Islands",
    "ME": "Montenegro",
    "ES-EU": "Basque Country",
    "IM": "Isle of Man",
    "CW": "Curaçao",
    "GB-WLS": "Wales",
    "CD": "Democratic Republic of the Congo",
    "_east-turkestan": "East Turkestan",
    "SS": "South Sudan",
    "MF": "Saint Martin",
    "_rainbow": "Rainbow",
    "_pirate": "Pirate",
    "BQ": "Caribbean Netherlands",
    "ES-CT": "Catalonia",
    "JE": "Jersey",
    "CA-QC": "Quebec",
}


def convert_country_codes(results: List):
    return [{**r, "country": country_codes.get(r["country"], r["country"])} for r in results]
