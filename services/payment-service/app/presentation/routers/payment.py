from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.get_payment import GetPaymentUseCase
from app.application.use_cases.process_payment import ProcessPaymentUseCase
from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.repositories.payment_repository import (
    SqlAlchemyPaymentRepository,
)
from app.presentation.schemas.payment import PaymentRequest, PaymentResponse
from shared.enums.status import PaymentStatus

router = APIRouter()


@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    *, db: AsyncSession = Depends(get_db), payment_in: PaymentRequest
) -> Any:
    repository = SqlAlchemyPaymentRepository(db)
    use_case = ProcessPaymentUseCase(repository)
    payment = await use_case.execute(payment_in.order_id, payment_in.amount)
    if payment.status == PaymentStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment failed",
        )
    return payment


@router.get("/order/{order_id}", response_model=PaymentResponse)
async def get_payment_by_order(
    order_id: UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    repository = SqlAlchemyPaymentRepository(db)
    use_case = GetPaymentUseCase(repository)
    payment = await use_case.execute(order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
