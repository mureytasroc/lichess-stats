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
