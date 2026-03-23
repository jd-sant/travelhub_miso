from sqlmodel import Session, select

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(session: Session, correo_electronico: str) -> User | None:
    return session.exec(select(User).where(User.correo_electronico == correo_electronico)).first()


def create_user_record(session: Session, payload: UserCreate) -> User:
    user = User(
        correo_electronico=str(payload.correo_electronico),
        telefono=payload.telefono,
        contrasena=hash_password(payload.contrasena),
        estado=payload.estado,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def list_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()
