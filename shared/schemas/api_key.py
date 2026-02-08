from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ApiKeyResponse(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    order_id: UUID
    key: str
    quota_limit: int
    quota_used: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
