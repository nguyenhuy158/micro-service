import uuid

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    image_url: str | None = None
    category_id: uuid.UUID | None = None

    api_url: str | None = None
    quota_limit: int = 1000
    rate_limit: int = 60


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: uuid.UUID
    category: Category | None = None
    model_config = ConfigDict(from_attributes=True)
