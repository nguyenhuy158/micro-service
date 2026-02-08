from uuid import UUID

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
    transaction_id: str | None = None

    class Config:
        from_attributes = True
