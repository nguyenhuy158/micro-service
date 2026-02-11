import uuid

from app.domain.repositories.payment_repository import PaymentRepository
from app.infrastructure.persistence.models.payment import Payment


class GetPaymentUseCase:
    def __init__(self, repository: PaymentRepository) -> None:
        self._repository = repository

    async def execute(self, order_id: uuid.UUID) -> Payment | None:
        return await self._repository.find_by_order_id(order_id)
