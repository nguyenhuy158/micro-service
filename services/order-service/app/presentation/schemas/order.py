from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from shared.enums.status import OrderStatus
from shared.schemas.api_key import ApiKeyResponse


class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class OrderBase(BaseModel):
    user_id: UUID
    shipping_address: str | None = None


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    total_amount: float
    status: OrderStatus
    items: list[OrderItemResponse]
    api_keys: list[ApiKeyResponse] = []
