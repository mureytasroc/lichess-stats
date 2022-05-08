from typing import List

from pydantic import BaseModel, Field


class DateDistributionEntry(BaseModel):
    start_date: str = Field(
        regex=r"^\d{4}-\d{2}-\d{2}$",
        description="The start date of games in this bin (YYYY-MM-DD, UTC).",
    )
    count: int = Field(ge=0, description="The number of games in this bin.")


class DateDistribution(BaseModel):
    dates: List[DateDistributionEntry] = Field(description="An array of date entries.")


class CastlingPercentageEntry(BaseModel):
    username: str = Field(
        description="The username of this player.",
    )
    castling_percentage: float = Field(
        ge=0, le=100, description="The castling percentage of this player (0-100)."
    )


class CastlingPercentage(BaseModel):
    players: List[CastlingPercentageEntry] = Field(description="An array of player entries.")
