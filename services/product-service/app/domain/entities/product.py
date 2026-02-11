import uuid

from pydantic import BaseModel, ConfigDict


class CategoryEntity(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductEntity(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    image_url: str | None = None
    api_url: str | None = None
    quota_limit: int = 1000
    rate_limit: int = 60
    category_id: uuid.UUID | None = None
    category: CategoryEntity | None = None

    model_config = ConfigDict(from_attributes=True)
