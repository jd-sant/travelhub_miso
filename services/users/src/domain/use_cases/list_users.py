from adapters.models.user import User
from domain.ports.user_repository import UserRepository
from domain.use_cases.base import BaseUseCase


class ListUsersUseCase(BaseUseCase[None, list[User]]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self) -> list[User]:
        return self.repository.list_all()
