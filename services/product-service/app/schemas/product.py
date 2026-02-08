from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    image_url: str | None = None
    category_id: int | None = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category: Category | None = None
    model_config = ConfigDict(from_attributes=True)
