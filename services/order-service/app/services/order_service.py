import uuid
from uuid import UUID
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.internal_client import InternalServiceClient
from shared.enums.status import OrderStatus


class OrderService:
    @staticmethod
    async def get_order(db: AsyncSession, order_id: UUID) -> Optional[Order]:
        result = await db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_orders(db: AsyncSession, user_id: UUID) -> List[Order]:
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        return list(result.scalars().all())

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

        # TODO: Publish Order.Placed event to RabbitMQ

        return db_order

    @staticmethod
    async def update_order_status(
        db: AsyncSession, order_id: UUID, status: OrderStatus
    ) -> Optional[Order]:
        db_order = await OrderService.get_order(db, order_id)
        if db_order:
            db_order.status = status
            await db.commit()
            await db.refresh(db_order)
        return db_order
