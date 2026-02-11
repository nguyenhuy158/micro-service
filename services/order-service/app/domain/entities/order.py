from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from shared.enums.status import OrderStatus


@dataclass
class OrderItemEntity:
    product_id: uuid.UUID
    quantity: int
    price: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    order_id: uuid.UUID | None = None


@dataclass
class OrderEntity:
    user_id: uuid.UUID
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: str | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    items: list[OrderItemEntity] = field(default_factory=list)
    api_keys: list[dict] = field(default_factory=list)

    @staticmethod
    def calculate_total(items: list[OrderItemEntity]) -> float:
        return sum(item.price * item.quantity for item in items)
