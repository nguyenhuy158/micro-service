from uuid import UUID

from pydantic import BaseModel, Field


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
