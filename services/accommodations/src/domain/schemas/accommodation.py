from uuid import UUID

from pydantic import BaseModel, Field


class AccommodationResponse(BaseModel):
    id: UUID
    name: str
    description: str
    location: str
    price_per_night: float
    rating: float = Field(ge=0.0, le=5.0)
    available_rooms: int = Field(ge=0)
    status: int = Field(default=1, ge=0, le=1)
