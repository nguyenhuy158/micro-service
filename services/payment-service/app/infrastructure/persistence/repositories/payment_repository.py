import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.payment_repository import PaymentRepository
from app.infrastructure.persistence.models.payment import Payment


class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_by_order_id(self, order_id: uuid.UUID) -> Payment | None:
        result = await self._db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def save(self, payment: Payment) -> Payment:
        self._db.add(payment)
        await self._db.commit()
        await self._db.refresh(payment)
        return payment
