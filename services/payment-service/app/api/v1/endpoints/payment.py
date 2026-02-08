from uuid import UUID
from typing import Any

from app.db.session import get_db
from app.schemas.payment import PaymentRequest, PaymentResponse
from app.services.payment_service import PaymentService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.enums.status import PaymentStatus

router = APIRouter()


@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    *, db: AsyncSession = Depends(get_db), payment_in: PaymentRequest
) -> Any:
    payment = await PaymentService.process_payment(db, payment_in)
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
    payment = await PaymentService.get_payment_by_order(db, order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
