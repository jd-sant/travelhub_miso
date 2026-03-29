from fastapi import Depends
from sqlmodel import Session

from adapters.repositories.accommodation_repository import (
    SQLModelAccommodationRepository,
)
from db.session import get_session
from domain.ports.accommodation_repository import AccommodationRepository
from domain.use_cases.get_accommodation_detail import (
    GetAccommodationDetailUseCase,
)


def get_accommodation_repository(
    session: Session = Depends(get_session),
) -> AccommodationRepository:
    return SQLModelAccommodationRepository(session)


def get_accommodation_detail_use_case(
    repository: AccommodationRepository = Depends(get_accommodation_repository),
) -> GetAccommodationDetailUseCase:
    return GetAccommodationDetailUseCase(repository)
