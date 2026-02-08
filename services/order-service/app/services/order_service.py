import uuid
from typing import Any
from uuid import UUID

from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate
from app.services.internal_client import InternalServiceClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.enums.status import OrderStatus


class OrderService:
    @staticmethod
    async def get_order(db: AsyncSession, order_id: UUID) -> Any:
        result = await db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        if order:
            # Attach API keys from inventory service
            order.api_keys = await InternalServiceClient.get_api_keys(order_id)
        return order

    @staticmethod
    async def get_user_orders(db: AsyncSession, user_id: UUID) -> list[Any]:
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        orders = list(result.scalars().all())
        for order in orders:
            order.api_keys = await InternalServiceClient.get_api_keys(order.id)
        return orders

    @staticmethod
    async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
        # 1. Calculate total amount
        total_amount = sum(item.price * item.quantity for item in order_in.items)

        # 2. Create Order
        db_order = Order(
            id=uuid.uuid4(),
            user_id=order_in.user_id,
            total_amount=total_amount,
            shipping_address=order_in.shipping_address,
            status=OrderStatus.PENDING,
        )
        db.add(db_order)
        await db.flush()  # Get order ID

        # 3. Create OrderItems
        items_to_reserve = []
        for item_in in order_in.items:
            db_item = OrderItem(
                id=uuid.uuid4(), order_id=db_order.id, **item_in.model_dump()
            )
            db.add(db_item)
            db_order.items.append(db_item)  # Ensure items are available in memory
            items_to_reserve.append(item_in)

        # 4. Reserve Stock (Synchronous)
        reserved_items = []
        stock_success = True
        for item in items_to_reserve:
            success = await InternalServiceClient.reserve_stock(
                item.product_id, item.quantity
            )
            if not success:
                stock_success = False
                break
            reserved_items.append(item)

        if not stock_success:
            # Rollback stock reservations
            for item in reserved_items:
                await InternalServiceClient.release_stock(
                    item.product_id, item.quantity
                )

            db_order.status = OrderStatus.FAILED
            await db.commit()
            await db.refresh(db_order)
            return db_order

        # 5. Process Payment (Synchronous)
        payment_success = await InternalServiceClient.process_payment(
            db_order.id, total_amount
        )
        if not payment_success:
            # Rollback stock reservations
            for item in reserved_items:
                await InternalServiceClient.release_stock(
                    item.product_id, item.quantity
                )

            db_order.status = OrderStatus.FAILED
            await db.commit()
            await db.refresh(db_order)
            return db_order

        # 6. Finalize Order
        db_order.status = OrderStatus.PAID
        await db.commit()
        await db.refresh(db_order)

        # 7. Generate API Keys for purchased items
        for item in db_order.items:
            product = await InternalServiceClient.get_product(item.product_id)
            quota_limit = product.get("quota_limit", 1000) if product else 1000
            await InternalServiceClient.generate_api_key(
                user_id=db_order.user_id,
                product_id=item.product_id,
                order_id=db_order.id,
                quota_limit=quota_limit,
            )

        # TODO: Publish Order.Placed event to RabbitMQ

        return db_order

    @staticmethod
    async def update_order_status(
        db: AsyncSession, order_id: UUID, status: OrderStatus
    ) -> Order | None:
        db_order = await OrderService.get_order(db, order_id)
        if db_order:
            db_order.status = status
            await db.commit()
            await db.refresh(db_order)
        return db_order
