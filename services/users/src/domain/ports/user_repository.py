from abc import ABC, abstractmethod
from typing import Optional

from adapters.models.user import User
from domain.schemas.user import UserCreate


class UserRepository(ABC):
    @abstractmethod
    def add(self, payload: UserCreate) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass
