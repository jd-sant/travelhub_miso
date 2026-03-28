from abc import ABC, abstractmethod
from typing import Optional

from domain.schemas.user import UserCreateRequest, UserResponse


class UserRepository(ABC):
    @abstractmethod
    def add(self, payload: UserCreateRequest) -> UserResponse:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserResponse]:
        pass

    @abstractmethod
    def list_all(self) -> list[UserResponse]:
        pass
