import uuid

from app.models.inventory import Inventory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Product IDs from product-service seeding
PROD_LAPTOP_ID = uuid.UUID("b1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
PROD_SMARTPHONE_ID = uuid.UUID("b2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")
PROD_TSHIRT_ID = uuid.UUID("b3e3b3c3-d3e3-43f3-a3b3-c3d3e3f3a3b3")

# News API Products
PROD_NEWS_STARTER_ID = uuid.UUID("c1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
PROD_NEWS_ADVANCE_ID = uuid.UUID("c2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")
PROD_NEWS_VIP_ID = uuid.UUID("c3e3b3c3-d3e3-43f3-a3b3-c3d3e3f3a3b3")


async def init_db(db: AsyncSession) -> None:
    # Check if we already have inventory
    result = await db.execute(select(Inventory).limit(1))
    inventory = result.scalar_one_or_none()

    if not inventory:
        # Create inventory items
        items = [
            Inventory(product_id=PROD_LAPTOP_ID, quantity=10, location="Warehouse A"),
            Inventory(
                product_id=PROD_SMARTPHONE_ID, quantity=20, location="Warehouse A"
            ),
            Inventory(product_id=PROD_TSHIRT_ID, quantity=50, location="Warehouse B"),
            Inventory(
                product_id=PROD_NEWS_STARTER_ID, quantity=999999, location="Digital"
            ),
            Inventory(
                product_id=PROD_NEWS_ADVANCE_ID, quantity=999999, location="Digital"
            ),
            Inventory(product_id=PROD_NEWS_VIP_ID, quantity=999999, location="Digital"),
        ]
        db.add_all(items)
        await db.commit()
