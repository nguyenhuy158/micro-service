from __future__ import annotations

import abc
from uuid import UUID


class PaymentClient(abc.ABC):
    @abc.abstractmethod
    async def process_payment(self, order_id: UUID, amount: float) -> bool: ...
