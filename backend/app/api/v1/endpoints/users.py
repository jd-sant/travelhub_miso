from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.user import UserCreate, UserPublic
from app.services.user_service import create_user_service, list_users_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)) -> UserPublic:
    user = create_user_service(session, payload)
    return UserPublic.model_validate(user)


@router.get("", response_model=list[UserPublic], status_code=status.HTTP_200_OK)
def get_users(session: Session = Depends(get_session)) -> list[UserPublic]:
    users = list_users_service(session)
    return [UserPublic.model_validate(user) for user in users]
