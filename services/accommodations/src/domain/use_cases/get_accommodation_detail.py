from uuid import UUID

from domain.ports.accommodation_repository import AccommodationRepository
from domain.schemas.accommodation import AccommodationResponse
from domain.use_cases.base import BaseUseCase
from errors import AccommodationNotFoundError


class GetAccommodationDetailUseCase(
    BaseUseCase[UUID, AccommodationResponse]
):
    def __init__(self, repository: AccommodationRepository):
        self.repository = repository

    def execute(self, accommodation_id: UUID) -> AccommodationResponse:
        accommodation = self.repository.get_by_id(accommodation_id)
        if accommodation is None:
            raise AccommodationNotFoundError(
                f"Accommodation with id {accommodation_id} not found"
            )
        return accommodation
