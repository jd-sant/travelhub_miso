from adapters.models.user import User
from domain.ports.user_repository import UserRepository
from domain.schemas.user import UserCreate
from domain.use_cases.base import BaseUseCase
from errors import UserConflictError


class CreateUserUseCase(BaseUseCase[UserCreate, User]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, payload: UserCreate) -> User:
        existing = self.repository.get_by_email(str(payload.correo_electronico))
        if existing is not None:
            raise UserConflictError("El correo_electronico ya existe")

        return self.repository.add(payload)
