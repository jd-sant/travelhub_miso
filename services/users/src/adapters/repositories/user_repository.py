from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from adapters.models.user import User
from core.security import hash_password
from domain.ports.user_repository import UserRepository
from domain.schemas.user import UserCreate
from errors import UserConflictError


class SQLModelUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, payload: UserCreate) -> User:
        user = User(
            correo_electronico=str(payload.correo_electronico),
            telefono=payload.telefono,
            contrasena=hash_password(payload.contrasena),
            estado=payload.estado,
        )
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise UserConflictError("Conflict while creating user") from exc
        self.session.refresh(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.exec(
            select(User).where(User.correo_electronico == email)
        ).first()

    def list_all(self) -> list[User]:
        return list(self.session.exec(select(User)).all())
