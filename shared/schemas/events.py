from typing import Any
from uuid import UUID

from pydantic import BaseModel

from .base import DomainEvent


# Payload Models
class OrderItem(BaseModel):
    product_id: UUID
    quantity: int
    price: float


class ApiKeyPayload(BaseModel):
    order_id: UUID
    user_id: UUID
    product_id: UUID
    api_key: str
    quota: int
    rate_limit: int


class OrderPayload(BaseModel):
    order_id: UUID
    user_id: UUID
    items: list[OrderItem]
    total_amount: float
    status: str


# Events
class OrderCreatedEvent(DomainEvent):
    event_type: str = "OrderCreated"
    payload: OrderPayload


class StockReservedEvent(DomainEvent):
    event_type: str = "StockReserved"
    payload: dict[str, Any]  # { "order_id": ..., "status": "reserved" }


class StockReservationFailedEvent(DomainEvent):
    event_type: str = "StockReservationFailed"
    payload: dict[str, Any]  # { "order_id": ..., "reason": "out_of_stock" }


class PaymentProcessedEvent(DomainEvent):
    event_type: str = "PaymentProcessed"
    payload: dict[str, Any]  # { "order_id": ..., "payment_id": ... }


class PaymentFailedEvent(DomainEvent):
    event_type: str = "PaymentFailed"
    payload: dict[str, Any]  # { "order_id": ..., "reason": "insufficient_funds" }


class OrderCompletedEvent(DomainEvent):
    event_type: str = "OrderCompleted"
    payload: dict[str, Any]  # { "order_id": ... }


class OrderCancelledEvent(DomainEvent):
    event_type: str = "OrderCancelled"
    payload: dict[str, Any]  # { "order_id": ..., "reason": ... }


class ApiKeyGeneratedEvent(DomainEvent):
    event_type: str = "ApiKeyGenerated"
    payload: ApiKeyPayload
