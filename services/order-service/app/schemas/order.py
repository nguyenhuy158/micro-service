from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field
from shared.enums.status import OrderStatus


class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: UUID

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: UUID
    shipping_address: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderResponse(OrderBase):
    id: UUID
    total_amount: float
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
