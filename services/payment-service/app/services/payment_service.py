import uuid

from app.application.use_cases.get_payment import GetPaymentUseCase
from app.application.use_cases.process_payment import ProcessPaymentUseCase
from app.infrastructure.persistence.models.payment import Payment
from app.infrastructure.persistence.repositories.payment_repository import (
    SqlAlchemyPaymentRepository,
)
from app.presentation.schemas.payment import PaymentRequest
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentService:
    @staticmethod
    async def process_payment(db: AsyncSession, payment_in: PaymentRequest) -> Payment:
        repository = SqlAlchemyPaymentRepository(db)
        use_case = ProcessPaymentUseCase(repository)
        return await use_case.execute(payment_in.order_id, payment_in.amount)

    @staticmethod
    async def get_payment_by_order(
        db: AsyncSession, order_id: uuid.UUID
    ) -> Payment | None:
        repository = SqlAlchemyPaymentRepository(db)
        use_case = GetPaymentUseCase(repository)
        return await use_case.execute(order_id)
