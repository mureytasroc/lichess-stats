from typing import List, Optional

from pydantic import BaseModel, Field

from app.database.util import TerminationType, Title


# Titles


class TitleEntry(BaseModel):
    title: Optional[Title] = Field(description="The player title (or null if untitled)")


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
        ge=0,
        le=100,
        description="The average game completion rate (0-100) of players with this title. A player is considered to have completed the game if they did not resign or abandon the game.",  # noqa: E501
    )
    stddev_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The standard deviation of game completion rates of players with this title.",
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


class ResultCountsByTitleEntry(TitleEntry):
    win_count: Optional[int] = Field(
        ge=0, description="The total number of wins by players with this title."
    )
    draw_count: Optional[int] = Field(
        ge=0,
        description="The total number of draws by players with this title.",
    )
    loss_count: Optional[int] = Field(
        ge=0,
        description="The total number of losses by players with this title.",
    )


class ResultCountsByTitle(BaseModel):
    titles: List[ResultCountsByTitleEntry] = Field(description="An array of title entries.")


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
    country: Optional[str] = Field(description="The player's country.")


class CountryDistributionEntry(CountryEntry):
    count: int = Field(ge=0, description="The number of players from this country.")


class CountryDistribution(BaseModel):
    countries: List[CountryDistributionEntry] = Field(description="An array of country entries.")


class CompletionRateByCountryEntry(CountryEntry):
    avg_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The average completion rate (0-100) of players from this country. A player is considered to have completed the game if they did not resign or abandon the game.",  # noqa: E501
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


class ResultCountsByCountryEntry(CountryEntry):
    win_count: Optional[int] = Field(
        ge=0, description="The total number of wins by players from this country."
    )
    draw_count: Optional[int] = Field(
        ge=0,
        description="The total number of draws by players from this country.",
    )
    loss_count: Optional[int] = Field(
        ge=0,
        description="The total number of losses by players from this country.",
    )


class ResultCountsByCountry(BaseModel):
    countries: List[ResultCountsByCountryEntry] = Field(description="An array of country entries.")


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
