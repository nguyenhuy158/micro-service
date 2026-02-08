from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.product import Category, Product
from app.schemas.product import CategoryCreate, ProductCreate


class ProductService:
    async def create_product(
        self, db: AsyncSession, product_in: ProductCreate
    ) -> Product:
        db_product = Product(**product_in.model_dump())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    async def get_products(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_product(self, db: AsyncSession, product_id: int) -> Product | None:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create_category(
        self, db: AsyncSession, category_in: CategoryCreate
    ) -> Category:
        db_category = Category(**category_in.model_dump())
        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)
        return db_category

    async def get_categories(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Category]:
        query = select(Category).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())


product_service = ProductService()
