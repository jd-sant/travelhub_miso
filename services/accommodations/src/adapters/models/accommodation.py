from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Accommodation(SQLModel, table=True):
    __tablename__ = "accommodations"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)
    description: str
    location: str = Field(index=True)
    price_per_night: float
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    available_rooms: int = Field(default=0, ge=0)
    status: int = Field(default=1, ge=0, le=1)
