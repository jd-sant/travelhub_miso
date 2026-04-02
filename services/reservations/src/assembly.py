from sqlmodel import Session

from adapters.repositories.reservation_repository import SQLModelReservationRepository
from db.session import get_session
from domain.use_cases.create_reservation import CreateReservationUseCase


class ReservationAssembly:
    """Dependency injection container for Reservations service."""

    @staticmethod
    def get_session():
        return get_session()

    @staticmethod
    def get_reservation_repository(session: Session = None) -> SQLModelReservationRepository:
        if session is None:
            session = next(ReservationAssembly.get_session())
        return SQLModelReservationRepository(session)

    @staticmethod
    def get_create_reservation_use_case(
        repository: SQLModelReservationRepository = None,
    ) -> CreateReservationUseCase:
        if repository is None:
            repository = ReservationAssembly.get_reservation_repository()
        return CreateReservationUseCase(repository)
