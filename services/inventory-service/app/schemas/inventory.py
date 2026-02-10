from uuid import UUID

from pydantic import BaseModel, Field
from shared.schemas.api_key import ApiKeyResponse

__all__ = [
    "InventoryBase",
    "InventoryCreate",
    "InventoryUpdate",
    "InventoryResponse",
    "StockReservation",
    "ApiKeyCreate",
    "ApiKeyResponse",
]


class InventoryBase(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=0)
    location: str | None = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: int | None = Field(None, ge=0)
    reserved_quantity: int | None = Field(None, ge=0)
    location: str | None = None


class InventoryResponse(InventoryBase):
    id: UUID
    reserved_quantity: int

    class Config:
        from_attributes = True


class StockReservation(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class ApiKeyCreate(BaseModel):
    user_id: UUID
    product_id: UUID
    order_id: UUID
    quota_limit: int = 1000
    rate_limit: int = 60
