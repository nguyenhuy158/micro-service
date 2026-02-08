from uuid import UUID

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
    shipping_address: str | None = None


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderResponse(OrderBase):
    id: UUID
    total_amount: float
    status: OrderStatus
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
