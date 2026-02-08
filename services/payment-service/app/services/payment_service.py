import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payment import Payment
from app.schemas.payment import PaymentRequest
from shared.enums.status import PaymentStatus


class PaymentService:
    @staticmethod
    async def process_payment(db: AsyncSession, payment_in: PaymentRequest) -> Payment:
        # Check if payment already exists
        result = await db.execute(
            select(Payment).where(Payment.order_id == payment_in.order_id)
        )
        db_payment = result.scalar_one_or_none()

        if db_payment:
            return db_payment

        # Mock payment processing logic
        status = PaymentStatus.SUCCESS
        if payment_in.amount > 10000:  # Mock failure for large amounts
            status = PaymentStatus.FAILED

        db_payment = Payment(
            id=uuid.uuid4(),
            order_id=payment_in.order_id,
            amount=payment_in.amount,
            status=status,
            transaction_id=str(uuid.uuid4())
            if status == PaymentStatus.SUCCESS
            else None,
        )

        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        return db_payment

    @staticmethod
    async def get_payment_by_order(
        db: AsyncSession, order_id: uuid.UUID
    ) -> Optional[Payment]:
        result = await db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalar_one_or_none()
