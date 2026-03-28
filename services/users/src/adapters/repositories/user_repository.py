from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from adapters.models.user import User
from core.security import hash_password
from domain.ports.user_repository import UserRepository
from domain.schemas.user import UserCreateRequest, UserResponse
from errors import UserConflictError


def _to_response(model: User) -> UserResponse:
    return UserResponse(
        id_usuario=model.id_usuario,
        correo_electronico=model.correo_electronico,
        telefono=model.telefono,
        estado=model.estado,
    )


class SQLModelUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, payload: UserCreateRequest) -> UserResponse:
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
        return _to_response(user)

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        model = self.session.exec(
            select(User).where(User.correo_electronico == email)
        ).first()
        return _to_response(model) if model else None

    def list_all(self) -> list[UserResponse]:
        models = self.session.exec(select(User)).all()
        return [_to_response(m) for m in models]
