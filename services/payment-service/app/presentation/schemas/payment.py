from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from shared.enums.status import PaymentStatus


class PaymentRequest(BaseModel):
    order_id: UUID
    amount: float = Field(gt=0)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    order_id: UUID
    amount: float
    status: PaymentStatus
    transaction_id: str | None = None
