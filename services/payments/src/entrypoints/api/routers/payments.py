from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from assembly import (
    get_create_payment_charge_use_case,
    get_get_payment_use_case,
    get_list_payment_events_use_case,
)
from core.config import settings
from domain.schemas.payment import PaymentChargeRequest, PaymentEventResponse, PaymentPublicResponse
from domain.use_cases.create_payment_charge import CreatePaymentChargeUseCase
from domain.use_cases.get_payment import GetPaymentUseCase
from domain.use_cases.list_payment_events import ListPaymentEventsUseCase
from errors import (
    DuplicatePaymentError,
    InsecureTransportError,
    InvalidChecksumError,
    PaymentNotFoundError,
)

router = APIRouter(prefix="/payments", tags=["payments"])


def _assert_secure_transport(x_forwarded_proto: str | None) -> None:
    if settings.enforce_tls_header and x_forwarded_proto != "https":
        raise InsecureTransportError("TLS 1.2+ is required for payment requests")


@router.post("/charges", response_model=PaymentPublicResponse, status_code=status.HTTP_201_CREATED)
def create_charge(
    payload: PaymentChargeRequest,
    x_forwarded_proto: str | None = Header(default=None),
    use_case: CreatePaymentChargeUseCase = Depends(get_create_payment_charge_use_case),
) -> PaymentPublicResponse:
    try:
        _assert_secure_transport(x_forwarded_proto)
        return use_case.execute(payload)
    except DuplicatePaymentError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Se detecto una transaccion duplicada en menos de 2 segundos.",
                "duplicate_payment_id": str(exc.duplicate_payment_id),
            },
        )
    except InvalidChecksumError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Checksum de integridad invalido.",
        )
    except InsecureTransportError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/{payment_id}", response_model=PaymentPublicResponse, status_code=status.HTTP_200_OK)
def get_payment(
    payment_id: UUID,
    use_case: GetPaymentUseCase = Depends(get_get_payment_use_case),
) -> PaymentPublicResponse:
    try:
        return use_case.execute(payment_id)
    except PaymentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado.",
        )


@router.get("/{payment_id}/events", response_model=list[PaymentEventResponse], status_code=status.HTTP_200_OK)
def list_payment_events(
    payment_id: UUID,
    use_case: ListPaymentEventsUseCase = Depends(get_list_payment_events_use_case),
) -> list[PaymentEventResponse]:
    return use_case.execute(payment_id)
