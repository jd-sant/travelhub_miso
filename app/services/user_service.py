from fastapi import HTTPException
from sqlmodel import Session

from app.models.user import User
from app.repositories.user_repository import create_user_record, get_user_by_email, list_users
from app.schemas.user import UserCreate


def create_user_service(session: Session, payload: UserCreate) -> User:
    existing_user = get_user_by_email(session, str(payload.correo_electronico))
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="El correo_electronico ya existe")

    return create_user_record(session, payload)


def list_users_service(session: Session) -> list[User]:
    return list_users(session)
