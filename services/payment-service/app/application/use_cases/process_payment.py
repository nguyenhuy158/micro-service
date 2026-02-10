import uuid

from app.domain.repositories.payment_repository import PaymentRepository
from app.infrastructure.persistence.models.payment import Payment
from shared.enums.status import PaymentStatus


class ProcessPaymentUseCase:
    def __init__(self, repository: PaymentRepository) -> None:
        self._repository = repository

    async def execute(self, order_id: uuid.UUID, amount: float) -> Payment:
        existing = await self._repository.find_by_order_id(order_id)
        if existing:
            return existing

        status = PaymentStatus.SUCCESS
        if amount > 10000:
            status = PaymentStatus.FAILED

        payment = Payment(
            id=uuid.uuid4(),
            order_id=order_id,
            amount=amount,
            status=status,
            transaction_id=str(uuid.uuid4())
            if status == PaymentStatus.SUCCESS
            else None,
        )

        return await self._repository.save(payment)
