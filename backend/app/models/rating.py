from typing import List, Optional

from pydantic import BaseModel, Field

from app.database.util import Title, TerminationType


class RatingBin(BaseModel):
    rating_min: int = Field(ge=0, description="The minimum rating of this bin.")
    rating_max: int = Field(ge=0, description="The maximum rating of this bin.")


class RatingDistributionEntry(RatingBin):
    count: int = Field(ge=1, description="The number of players in this rating bin.")


class RatingDistribution(BaseModel):
    bins: List[RatingDistributionEntry] = Field(description="An array of rating bins.")


class RatingByRatingEntry(RatingBin):
    ultrabullet_rating: Optional[float] = Field(
        ge=0, description="The average ultrabullet rating of players in this rating bin."
    )
    bullet_rating: Optional[float] = Field(
        ge=0, description="The average bullet rating of players in this rating bin."
    )
    blitz_rating: Optional[float] = Field(
        ge=0, description="The average blitz rating of players in this rating bin."
    )
    rapid_rating: Optional[float] = Field(
        ge=0, description="The average rapid rating of players in this rating bin."
    )
    classical_rating: Optional[float] = Field(
        ge=0, description="The average classical rating of players in this rating bin."
    )
    correspondence_rating: Optional[float] = Field(
        ge=0, description="The average correspondence rating of players in this rating bin."
    )
    fide_rating: Optional[float] = Field(
        ge=0, description="The average fide rating of players in this rating bin."
    )
    uscf_rating: Optional[float] = Field(
        ge=0, description="The average uscf rating of players in this rating bin."
    )
    ecf_rating: Optional[float] = Field(
        ge=0, description="The average ecf rating of players in this rating bin."
    )


class RatingByRating(BaseModel):
    bins: List[RatingByRatingEntry] = Field(description="An array of rating bins.")


class RatingByTitleEntry(BaseModel):
    title: Optional[Title] = Field(description="The player title (or null if untitled).")
    avg_rating: Optional[float] = Field(
        ge=0, description="The average rating of players with this title."
    )
    stddev_rating: Optional[float] = Field(
        ge=0, description="The standard deviation of ratings of players with this title."
    )


class RatingByTitle(BaseModel):
    titles: List[RatingByTitleEntry] = Field(description="An array of title entries.")


class RatingByCountryEntry(BaseModel):
    country: str = Field(description="The player's country.")
    avg_rating: Optional[float] = Field(
        ge=0, description="The average rating of players from this country."
    )
    stddev_rating: Optional[float] = Field(
        ge=0, description="The standard deviation of ratings of players from this country."
    )


class RatingByCountry(BaseModel):
    countries: List[RatingByCountryEntry] = Field(description="An array of country entries.")


class PlayTimeByRatingEntry(RatingBin):
    play_time: float = Field(
        ge=0, description="The average total play time (in seconds) for players in this rating bin."
    )


class PlayTimeByRating(BaseModel):
    bins: List[PlayTimeByRatingEntry] = Field(description="An array of rating bins.")


class CompletionRateByRatingEntry(RatingBin):
    avg_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The average completion rate (0-100) of players in this rating bin. A player is considered to have completed a game if they did not resign or abandon the game.",  # noqa: E501
    )
    stddev_completion_rate: Optional[float] = Field(
        ge=0,
        le=100,
        description="The standard deviation of completion rates of players in this rating bin.",
    )


class CompletionRateByRating(BaseModel):
    bins: List[CompletionRateByRatingEntry] = Field(description="An array of rating bins.")


class PercentPatronByRatingEntry(RatingBin):
    percent_patron: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of players in this rating bin who are Lichess patrons.",
    )


class PercentPatronByRating(BaseModel):
    bins: List[PercentPatronByRatingEntry] = Field(description="An array of rating bins.")


class PercentTOSViolatorsByRatingEntry(RatingBin):
    percent_tos_violators: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of players in this rating bin who have violated TOS.",
    )


class PercentTOSViolatorsByRating(BaseModel):
    bins: List[PercentTOSViolatorsByRatingEntry] = Field(description="An array of rating bins.")


class CumulativeResultPercentagesByRatingEntry(RatingBin):
    win_percentage: float = Field(
        ge=0, le=100, description="The average cumulative win percentage (0-100) of this bin."
    )
    draw_percentage: float = Field(
        ge=0, le=100, description="The average cumulative draw percentage (0-100) of this bin."
    )
    loss_percentage: float = Field(
        ge=0, le=100, description="The average cumulative loss percentage (0-100) of this bin."
    )


class CumulativeResultPercentagesByRating(BaseModel):
    bins: List[CumulativeResultPercentagesByRatingEntry] = Field(
        description="An array of rating bins."
    )


class ResultPercentagesByRatingEntry(RatingBin):
    win_percentage: float = Field(
        ge=0, le=100, description="The average win percentage (0-100) of this bin."
    )
    draw_percentage: float = Field(
        ge=0, le=100, description="The average draw percentage (0-100) of this bin."
    )
    loss_percentage: float = Field(
        ge=0, le=100, description="The average loss percentage (0-100) of this bin."
    )


class ResultPercentagesByRating(BaseModel):
    white_bins: List[ResultPercentagesByRatingEntry] = Field(
        description="An array of rating bins (for games played with the white pieces)."
    )
    black_bins: List[ResultPercentagesByRatingEntry] = Field(
        description="An array of rating bins (for games played with the black pieces)."
    )


class ResultPercentagesByRating2DEntry(BaseModel):
    white_rating_min: int = Field(
        description="The minimum rating of the white player for this bin."
    )
    white_rating_max: int = Field(
        description="The maximum rating of the white player for this bin."
    )
    black_rating_min: int = Field(
        description="The minimum rating of the black player for this bin."
    )
    black_rating_max: int = Field(
        description="The maximum rating of the black player for this bin."
    )
    white_win_percentage: float = Field(
        ge=0,
        le=100,
        description="The average win percentage (0-100) of the white player in this bin.",
    )
    white_draw_percentage: float = Field(
        ge=0,
        le=100,
        description="The average draw percentage (0-100) of the white player in this bin.",
    )
    white_loss_percentage: float = Field(
        ge=0,
        le=100,
        description="The average loss percentage (0-100) of the white player in this bin.",
    )
    black_win_percentage: float = Field(
        ge=0,
        le=100,
        description="The average win percentage (0-100) of the black player in this bin.",
    )
    black_draw_percentage: float = Field(
        ge=0,
        le=100,
        description="The average draw percentage (0-100) of the black player in this bin.",
    )
    black_loss_percentage: float = Field(
        ge=0,
        le=100,
        description="The average loss percentage (0-100) of the black player in this bin.",
    )


class ResultPercentagesByRating2D(BaseModel):
    bins: List[ResultPercentagesByRating2DEntry] = Field(
        description="An array of 2D (white and black) rating bins."
    )


class GameLengthByRatingEntry(RatingBin):
    game_length: float = Field(
        ge=1,
        description="The average game length (number of moves) for games in this rating bin.",
    )


class GameLengthByRating(BaseModel):
    bins: List[GameLengthByRatingEntry] = Field(description="An array of rating bins.")


class GameTerminationTypeByRatingEntryTerminationType(BaseModel):
    termination_type: TerminationType = Field(description="The termination type.")
    percentage: float = Field(
        ge=0,
        le=100,
        description="The percentage (0-100) of games with this termination type, in this rating bin.",  # noqa: E501
    )


class GameTerminationTypeByRatingEntryRating(RatingBin):
    termination_types: List[GameTerminationTypeByRatingEntryTerminationType] = Field(
        description="An array of termination type entries."
    )


class GameTerminationTypeByRating(BaseModel):
    bins: List[GameTerminationTypeByRatingEntryRating] = Field(
        description="An array of rating bins."
    )


class NumOpeningsByRatingEntry(RatingBin):
    num_openings: float = Field(
        ge=0,
        description="The average number of distinct openings (passing the optionally specified frequency threhsold) per player in this rating bin.",  # noqa: E501
    )


class NumOpeningsByRating(BaseModel):
    bins: List[NumOpeningsByRatingEntry] = Field(description="An array of rating bins.")


class AccuracyByRatingEntry(RatingBin):
    accuracy: float = Field(
        ge=0, le=100, description="The average game accuracy (0-100) by players in this rating bin."
    )


class AccuracyByRating(BaseModel):
    bins: List[AccuracyByRatingEntry] = Field(description="An array of rating bins.")


class StdDevAccuracyByRatingEntry(RatingBin):
    stddev_accuracy: float = Field(
        ge=0,
        le=100,
        description="The standard deviation of game accuracy (0-100) by players in this rating bin.",  # noqa: E501
    )


class StdDevAccuracyByRating(BaseModel):
    bins: List[StdDevAccuracyByRatingEntry] = Field(description="An array of rating bins.")
