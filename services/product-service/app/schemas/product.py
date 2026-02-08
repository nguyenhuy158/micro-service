from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    model_config = ConfigDict(from_attributes=True)
