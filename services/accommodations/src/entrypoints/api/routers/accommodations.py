from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from assembly import get_accommodation_detail_use_case
from domain.schemas.accommodation import AccommodationResponse
from domain.use_cases.get_accommodation_detail import (
    GetAccommodationDetailUseCase,
)
from errors import AccommodationNotFoundError

router = APIRouter(prefix="/accommodations", tags=["accommodations"])


@router.get(
    "/{accommodation_id}",
    response_model=AccommodationResponse,
    status_code=status.HTTP_200_OK,
)
def get_accommodation_detail(
    accommodation_id: UUID,
    use_case: GetAccommodationDetailUseCase = Depends(
        get_accommodation_detail_use_case
    ),
) -> AccommodationResponse:
    try:
        return use_case.execute(accommodation_id)
    except AccommodationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accommodation with id {accommodation_id} not found",
        )
