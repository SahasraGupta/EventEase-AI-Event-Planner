
from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    user_query: str


class Venue(BaseModel):
    name: str = Field(description="Verified venue name")

    image_url: str | None = Field(
        default=None,
        description="Image URL of this venue, if available"
    )

    rating: str | None = Field(
        default=None,
        description="Verified venue rating, if available"
    )

    address: str | None = Field(
        default=None,
        description="Verified venue address or locality"
    )

    capacity: str | None = Field(
        default=None,
        description="Verified guest capacity"
    )

    facilities: list[str] = Field(
        default_factory=list,
        description="Verified facilities available at the venue"
    )

    price: str | None = Field(
        default=None,
        description="Verified venue pricing or estimated price"
    )

    source_url: str = Field(
        description="Direct source URL supporting this venue's details"
    )


class EventRecommendations(BaseModel):
    event_overview: str = Field(
        description="Overview of the event"
    )

    venue_recommendations: list[Venue] = Field(
        description="List of individually structured venue recommendations"
    )

    food_recommendations: str = Field(
        description="Food and catering suggestions"
    )

    decoration_recommendations: str = Field(
        description="Decoration ideas"
    )

    additional_recommendations: str = Field(
        description="Additional useful suggestions"
    )

    budget_breakdown: str = Field(
        description="Estimated budget breakdown"
    )

    information_sources: str = Field(
        description="Other sources used for recommendations"
    )
