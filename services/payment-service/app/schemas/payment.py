from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from shared.enums.status import PaymentStatus


class PaymentRequest(BaseModel):
    order_id: UUID
    amount: float = Field(gt=0)


class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    amount: float
    status: PaymentStatus
    transaction_id: Optional[str] = None

    class Config:
        from_attributes = True
