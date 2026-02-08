import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.product import Category, Product

# Fixed UUIDs for seeding
CAT_ELECTRONICS_ID = uuid.UUID("a1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
CAT_CLOTHING_ID = uuid.UUID("a2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")

PROD_LAPTOP_ID = uuid.UUID("b1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
PROD_SMARTPHONE_ID = uuid.UUID("b2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")
PROD_TSHIRT_ID = uuid.UUID("b3e3b3c3-d3e3-43f3-a3b3-c3d3e3f3a3b3")


async def init_db(db: AsyncSession) -> None:
    # Check if we already have categories
    result = await db.execute(select(Category).limit(1))
    category = result.scalar_one_or_none()

    if not category:
        # Create categories
        electronics = Category(
            id=CAT_ELECTRONICS_ID, name="Electronics", description="Gadgets and devices"
        )
        clothing = Category(
            id=CAT_CLOTHING_ID, name="Clothing", description="Apparel and accessories"
        )
        db.add_all([electronics, clothing])

        # Create products
        laptop = Product(
            id=PROD_LAPTOP_ID,
            name="Gaming Laptop",
            description="High performance gaming laptop",
            price=1200.0,
            stock=10,
            category_id=CAT_ELECTRONICS_ID,
        )
        smartphone = Product(
            id=PROD_SMARTPHONE_ID,
            name="Smartphone",
            description="Latest flagship smartphone",
            price=800.0,
            stock=20,
            category_id=CAT_ELECTRONICS_ID,
        )
        tshirt = Product(
            id=PROD_TSHIRT_ID,
            name="Cotton T-Shirt",
            description="Comfortable 100% cotton t-shirt",
            price=20.0,
            stock=50,
            category_id=CAT_CLOTHING_ID,
        )
        db.add_all([laptop, smartphone, tshirt])

        await db.commit()
