from fastapi import APIRouter, Depends, HTTPException, status

from assembly import get_create_user_use_case, get_list_users_use_case
from domain.schemas.user import UserCreate, UserPublic
from domain.use_cases.create_user import CreateUserUseCase
from domain.use_cases.list_users import ListUsersUseCase
from errors import UserConflictError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserPublic:
    try:
        user = use_case.execute(payload)
    except UserConflictError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo_electronico ya existe",
        )
    return UserPublic.model_validate(user)


@router.get("", response_model=list[UserPublic], status_code=status.HTTP_200_OK)
def get_users(
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
) -> list[UserPublic]:
    users = use_case.execute()
    return [UserPublic.model_validate(user) for user in users]
