from uuid import UUID

from core.jwt_handler import decode_token
from domain.schemas.auth import TokenValidationRequest, TokenValidationResponse
from domain.use_cases.base import BaseUseCase


class ValidateTokenUseCase(
    BaseUseCase[TokenValidationRequest, TokenValidationResponse]
):
    def execute(
        self, payload: TokenValidationRequest
    ) -> TokenValidationResponse:
        claims = decode_token(payload.token)
        return TokenValidationResponse(
            user_id=UUID(claims["sub"]),
            email=claims["email"],
            role=claims["role"],
            valid=True,
        )
