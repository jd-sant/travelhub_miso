from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.schemas.accommodation import AccommodationResponse


class AccommodationRepository(ABC):
    @abstractmethod
    def get_by_id(self, accommodation_id: UUID) -> Optional[AccommodationResponse]:
        pass

    @abstractmethod
    def list_all(self) -> list[AccommodationResponse]:
        pass
