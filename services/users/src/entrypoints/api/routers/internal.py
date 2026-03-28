from fastapi import APIRouter, Depends, Header, HTTPException, status

from assembly import get_verify_credentials_use_case
from core.config import settings
from domain.schemas.user import VerifyCredentialsRequest, VerifyCredentialsResponse
from domain.use_cases.verify_credentials import VerifyCredentialsUseCase
from errors import InvalidCredentialsError

router = APIRouter(prefix="/internal", tags=["internal"])


def _verify_api_key(
    x_internal_api_key: str = Header(default=None),
) -> None:
    if x_internal_api_key != settings.internal_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )


@router.post(
    "/verify-credentials",
    response_model=VerifyCredentialsResponse,
    status_code=status.HTTP_200_OK,
)
def verify_credentials(
    payload: VerifyCredentialsRequest,
    _: None = Depends(_verify_api_key),
    use_case: VerifyCredentialsUseCase = Depends(
        get_verify_credentials_use_case
    ),
) -> VerifyCredentialsResponse:
    try:
        return use_case.execute(payload)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )
