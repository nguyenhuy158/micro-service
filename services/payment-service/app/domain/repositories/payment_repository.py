import uuid
from abc import ABC, abstractmethod

from app.infrastructure.persistence.models.payment import Payment


class PaymentRepository(ABC):
    @abstractmethod
    async def find_by_order_id(self, order_id: uuid.UUID) -> Payment | None: ...

    @abstractmethod
    async def save(self, payment: Payment) -> Payment: ...
