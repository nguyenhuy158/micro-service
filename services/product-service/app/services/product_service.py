import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.create_category import CreateCategoryUseCase
from app.application.use_cases.create_product import CreateProductUseCase
from app.application.use_cases.get_product import GetProductUseCase
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.application.use_cases.list_products import ListProductsUseCase
from app.infrastructure.persistence.models.product import Category, Product
from app.infrastructure.persistence.repositories.category_repository import (
    SqlAlchemyCategoryRepository,
)
from app.infrastructure.persistence.repositories.product_repository import (
    SqlAlchemyProductRepository,
)
from app.presentation.schemas.product import CategoryCreate, ProductCreate


class ProductService:
    async def create_product(
        self, db: AsyncSession, product_in: ProductCreate
    ) -> Product:
        repo = SqlAlchemyProductRepository(db)
        use_case = CreateProductUseCase(repo)
        return await use_case.execute(product_in.model_dump())

    async def get_products(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        repo = SqlAlchemyProductRepository(db)
        use_case = ListProductsUseCase(repo)
        return await use_case.execute(skip, limit)

    async def get_product(
        self, db: AsyncSession, product_id: uuid.UUID
    ) -> Product | None:
        repo = SqlAlchemyProductRepository(db)
        use_case = GetProductUseCase(repo)
        return await use_case.execute(product_id)

    async def create_category(
        self, db: AsyncSession, category_in: CategoryCreate
    ) -> Category:
        repo = SqlAlchemyCategoryRepository(db)
        use_case = CreateCategoryUseCase(repo)
        return await use_case.execute(category_in.model_dump())

    async def get_categories(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Category]:
        repo = SqlAlchemyCategoryRepository(db)
        use_case = ListCategoriesUseCase(repo)
        return await use_case.execute(skip, limit)


product_service = ProductService()
