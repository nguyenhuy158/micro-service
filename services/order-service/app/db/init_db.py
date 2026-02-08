import uuid

from app.models.order import Order, OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from shared.enums.status import OrderStatus

# User ID from user-service seeding
TEST_USER_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")

# Product IDs from product-service seeding
PROD_LAPTOP_ID = uuid.UUID("b1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
PROD_SMARTPHONE_ID = uuid.UUID("b2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")


async def init_db(db: AsyncSession) -> None:
    # Check if we already have orders
    result = await db.execute(select(Order).limit(1))
    order = result.scalar_one_or_none()

    if not order:
        # Create a test order
        test_order = Order(
            user_id=TEST_USER_ID,
            total_amount=2000.0,
            status=OrderStatus.COMPLETED,
            shipping_address="123 Test St, Seed City",
        )
        db.add(test_order)
        await db.flush()  # Get order ID

        # Add items to order
        item1 = OrderItem(
            order_id=test_order.id, product_id=PROD_LAPTOP_ID, quantity=1, price=1200.0
        )
        item2 = OrderItem(
            order_id=test_order.id,
            product_id=PROD_SMARTPHONE_ID,
            quantity=1,
            price=800.0,
        )
        db.add_all([item1, item2])

        await db.commit()
