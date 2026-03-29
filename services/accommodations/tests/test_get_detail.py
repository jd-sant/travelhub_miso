from uuid import uuid4

import pytest
from sqlmodel import Session

from adapters.models.accommodation import Accommodation
from adapters.repositories.accommodation_repository import (
    SQLModelAccommodationRepository,
)
from domain.use_cases.get_accommodation_detail import (
    GetAccommodationDetailUseCase,
)
from errors import AccommodationNotFoundError


@pytest.fixture
def accommodation_sample():
    """Create a sample accommodation for testing"""
    return Accommodation(
        id=uuid4(),
        name="Hotel Paradise",
        description="A beautiful hotel with ocean view",
        location="Miami, USA",
        price_per_night=150.00,
        rating=4.5,
        available_rooms=10,
        status=1,
    )


def test_get_accommodation_detail_success(
    session: Session, accommodation_sample: Accommodation
):
    """Test getting accommodation detail successfully"""
    session.add(accommodation_sample)
    session.commit()

    repository = SQLModelAccommodationRepository(session)
    use_case = GetAccommodationDetailUseCase(repository)

    result = use_case.execute(accommodation_sample.id)

    assert result.id == accommodation_sample.id
    assert result.name == accommodation_sample.name
    assert result.description == accommodation_sample.description
    assert result.location == accommodation_sample.location
    assert result.price_per_night == accommodation_sample.price_per_night
    assert result.rating == accommodation_sample.rating
    assert result.available_rooms == accommodation_sample.available_rooms
    assert result.status == accommodation_sample.status


def test_get_accommodation_detail_not_found(session: Session):
    """Test getting accommodation detail when not found"""
    repository = SQLModelAccommodationRepository(session)
    use_case = GetAccommodationDetailUseCase(repository)

    non_existent_id = uuid4()

    with pytest.raises(AccommodationNotFoundError):
        use_case.execute(non_existent_id)
