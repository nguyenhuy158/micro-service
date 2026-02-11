import uuid
from dataclasses import dataclass, field

from shared.enums.status import PaymentStatus


@dataclass
class PaymentEntity:
    order_id: uuid.UUID
    amount: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: str | None = None
    provider: str = "mock"
