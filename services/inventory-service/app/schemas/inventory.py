from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=0)
    location: Optional[str] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)
    reserved_quantity: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None


class InventoryResponse(InventoryBase):
    id: UUID
    reserved_quantity: int

    class Config:
        from_attributes = True


class StockReservation(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
