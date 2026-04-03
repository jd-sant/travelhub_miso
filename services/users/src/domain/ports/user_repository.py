from abc import ABC, abstractmethod
from typing import Optional

from domain.schemas.user import UserCreateRequest, UserCredentialsData, UserResponse


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

    @abstractmethod
    def get_by_email_with_password_and_roles(
        self, email: str
    ) -> Optional[UserCredentialsData]:
        pass
