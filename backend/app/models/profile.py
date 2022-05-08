from typing import List, Optional

from pydantic import BaseModel, Field

from app.database.util import Title, TerminationType


# Titles


class TitleEntry(BaseModel):
    title: Optional[Title] = Field(description=f"The player title (or null if untitled)")


class TitleDescriptionEntry(TitleEntry):
    description: str = Field(description="A description of this title.")


class TitleDescription(BaseModel):
    titles: List[TitleDescriptionEntry] = Field(description="An array of title entries.")


class TitleDistributionEntry(TitleEntry):
    count: int = Field(ge=0, description="The number of players with this title.")


class TitleDistribution(BaseModel):
    titles: List[TitleDistributionEntry] = Field(description="An array of title entries.")


class CompletionRateByTitleEntry(TitleEntry):
    avg_completion_rate: Optional[float] = Field(
        ge=0, le=100, description="The average completion rate (0-100) of players with this title."
    )
    stddev_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The standard deviation of completion rates of players with this title.",
    )


class CompletionRateByTitle(BaseModel):
    titles: List[CompletionRateByTitleEntry] = Field(description="An array of title entries.")


class ResultPercentagesByTitleEntry(TitleEntry):
    win_percentage: Optional[float] = Field(
        ge=0, le=100, description="The average win percentage (0-100) of players with this title."
    )
    draw_percentage: Optional[float] = Field(
        ge=0, le=100, description="The average draw percentage (0-100) of players with this title."
    )
    loss_percentage: Optional[float] = Field(
        ge=0, le=100, description="The average loss percentage (0-100) of players with this title."
    )


class ResultPercentagesByTitle(BaseModel):
    titles: List[ResultPercentagesByTitleEntry] = Field(description="An array of title entries.")


class GameTerminationTypeByTitleEntryTerminationType(BaseModel):
    termination_type: TerminationType = Field(description="The termination type.")
    percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games with this termination type, played by players with this title.",  # noqa: E501
    )


class GameTerminationTypeByTitleEntryTitle(TitleEntry):
    termination_types: List[GameTerminationTypeByTitleEntryTerminationType] = Field(
        description="An array of termination type entries."
    )


class GameTerminationTypeByTitle(BaseModel):
    titles: List[GameTerminationTypeByTitleEntryTitle] = Field(
        description="An array of title entries."
    )


class GameLengthByTitleEntry(TitleEntry):
    avg_game_length: Optional[float] = Field(
        ge=1,
        description="The average game length (number of moves) played by players with this title.",
    )
    stddev_game_length: Optional[float] = Field(
        ge=0,
        description="The standard deviation of game lengths (number of moves) played by players with this title.",  # noqa: E501
    )


class GameLengthByTitle(BaseModel):
    titles: List[GameLengthByTitleEntry] = Field(description="An array of title entries.")


# Countries


class CountryEntry(BaseModel):
    country: str = Field(description="The player's country.")


class CountryDistributionEntry(CountryEntry):
    count: int = Field(ge=0, description="The number of players from this country.")


class CountryDistribution(BaseModel):
    countries: List[CountryDistributionEntry] = Field(description="An array of country entries.")


class CompletionRateByCountryEntry(BaseModel):
    country: str = Field(description="The player's country.")
    avg_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The average completion rate (0-100) of players from this country.",
    )
    stddev_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The standard deviation of completion rates of players from this country.",
    )


class CompletionRateByCountry(BaseModel):
    countries: List[CompletionRateByCountryEntry] = Field(
        description="An array of country entries."
    )


class ResultPercentagesByCountryEntry(CountryEntry):
    win_percentage: Optional[float] = Field(
        ge=0, le=100, description="The average win percentage (0-100) of players from this country."
    )
    draw_percentage: Optional[float] = Field(
        ge=0,
        le=100,
        description="The average draw percentage (0-100) of players from this country.",
    )
    loss_percentage: Optional[float] = Field(
        ge=0,
        le=100,
        description="The average loss percentage (0-100) of players from this country.",
    )


class ResultPercentagesByCountry(BaseModel):
    countries: List[ResultPercentagesByCountryEntry] = Field(
        description="An array of country entries."
    )


class GameTerminationTypeByCountryEntryTerminationType(BaseModel):
    termination_type: TerminationType = Field(description="The termination type.")
    percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games with this termination type, played by players from this country.",  # noqa: E501
    )


class GameTerminationTypeByCountryEntryCountry(CountryEntry):
    termination_types: List[GameTerminationTypeByCountryEntryTerminationType] = Field(
        description="An array of termination type entries."
    )


class GameTerminationTypeByCountry(BaseModel):
    countries: List[GameTerminationTypeByCountryEntryCountry] = Field(
        description="An array of country entries."
    )


class GameLengthByCountryEntry(CountryEntry):
    avg_game_length: Optional[float] = Field(
        ge=1,
        description="The average game length (number of moves) played by players from this country.",  # noqa: E501
    )
    stddev_game_length: Optional[float] = Field(
        ge=0,
        description="The standard deviation of game lengths (number of moves) played by players from this country.",  # noqa: E501
    )


class GameLengthByCountry(BaseModel):
    countries: List[GameLengthByCountryEntry] = Field(description="An array of country entries.")
