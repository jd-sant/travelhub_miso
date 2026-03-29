from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from adapters.models.accommodation import Accommodation
from domain.ports.accommodation_repository import AccommodationRepository
from domain.schemas.accommodation import AccommodationResponse


def _to_response(model: Accommodation) -> AccommodationResponse:
    return AccommodationResponse(
        id=model.id,
        name=model.name,
        description=model.description,
        location=model.location,
        price_per_night=model.price_per_night,
        rating=model.rating,
        available_rooms=model.available_rooms,
        status=model.status,
    )


class SQLModelAccommodationRepository(AccommodationRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, accommodation_id: UUID) -> Optional[AccommodationResponse]:
        model = self.session.exec(
            select(Accommodation).where(Accommodation.id == accommodation_id)
        ).first()
        return _to_response(model) if model else None

    def list_all(self) -> list[AccommodationResponse]:
        models = self.session.exec(select(Accommodation)).all()
        return [_to_response(m) for m in models]
