from typing import List, Optional

from pydantic import BaseModel, Field

from app.database.util import Title


# Titles


class TitleEntry(BaseModel):
    title: Optional[Title] = Field(description="The player title (or null if untitled).")


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


class GameTerminationTypeByTitleEntry(TitleEntry):
    normal_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated normally (e.g. checkmate or draw) played by players with this title.",  # noqa: E501
    )
    resignation_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by resignation played by players with this title.",  # noqa: E501
    )
    time_forfeit_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by time forfeit played by players with this title.",  # noqa: E501
    )
    abandoned_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by abandonment played by players with this title.",  # noqa: E501
    )


class GameTerminationTypeByTitle(BaseModel):
    titles: List[GameTerminationTypeByTitleEntry] = Field(description="An array of title entries.")


class GameLengthByTitleEntry(TitleEntry):
    avg_game_length: Optional[float] = Field(
        ge=1,
        description="The average game length (number of moves) played by players with this title.",
    )
    stddev_game_length: Optional[float] = Field(
        ge=1,
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


class GameTerminationTypeByCountryEntry(CountryEntry):
    normal_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated normally (e.g. checkmate or draw) played by players from this country.",  # noqa: E501
    )
    resignation_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by resignation played by players from this country.",  # noqa: E501
    )
    time_forfeit_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by time forfeit played by players from this country.",  # noqa: E501
    )
    abandoned_percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games that terminated by abandonment played by players from this country.",  # noqa: E501
    )


class GameTerminationTypeByCountry(BaseModel):
    countries: List[GameTerminationTypeByCountryEntry] = Field(
        description="An array of country entries."
    )


class GameLengthByCountryEntry(CountryEntry):
    avg_game_length: Optional[float] = Field(
        ge=1,
        description="The average game length (number of moves) played by players from this country.",  # noqa: E501
    )
    stddev_game_length: Optional[float] = Field(
        ge=1,
        description="The standard deviation of game lengths (number of moves) played by players from this country.",  # noqa: E501
    )


class GameLengthByCountry(BaseModel):
    countries: List[GameLengthByCountryEntry] = Field(description="An array of country entries.")
