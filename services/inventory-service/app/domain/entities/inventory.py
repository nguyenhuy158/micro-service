from uuid import UUID

from pydantic import BaseModel, Field


class InventoryEntity(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int = Field(ge=0, default=0)
    reserved_quantity: int = Field(ge=0, default=0)
    location: str | None = None

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity

    def can_reserve(self, quantity: int) -> bool:
        return self.available_quantity >= quantity


class ApiKeyEntity(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    order_id: UUID
    key: str
    quota_limit: int = 1000
    quota_used: int = 0
    rate_limit: int = 60
    is_active: bool = True
