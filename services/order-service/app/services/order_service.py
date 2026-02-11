import uuid
from typing import Any
from uuid import UUID

from app.infrastructure.persistence.models.order import Order, OrderItem
from app.presentation.schemas.order import OrderCreate
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
        total_amount = sum(item.price * item.quantity for item in order_in.items)

        db_order = Order(
            id=uuid.uuid4(),
            user_id=order_in.user_id,
            total_amount=total_amount,
            shipping_address=order_in.shipping_address,
            status=OrderStatus.PENDING,
        )
        db.add(db_order)
        await db.flush()

        items_to_reserve = []
        for item_in in order_in.items:
            db_item = OrderItem(
                id=uuid.uuid4(), order_id=db_order.id, **item_in.model_dump()
            )
            db.add(db_item)
            db_order.items.append(db_item)
            items_to_reserve.append(item_in)

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
            for item in reserved_items:
                await InternalServiceClient.release_stock(
                    item.product_id, item.quantity
                )

            db_order.status = OrderStatus.FAILED
            await db.commit()
            await db.refresh(db_order)
            return db_order

        payment_success = await InternalServiceClient.process_payment(
            db_order.id, total_amount
        )
        if not payment_success:
            for item in reserved_items:
                await InternalServiceClient.release_stock(
                    item.product_id, item.quantity
                )

            db_order.status = OrderStatus.FAILED
            await db.commit()
            await db.refresh(db_order)
            return db_order

        db_order.status = OrderStatus.PAID
        await db.commit()
        await db.refresh(db_order)

        for item in db_order.items:
            product = await InternalServiceClient.get_product(item.product_id)
            quota_limit = product.get("quota_limit", 1000) if product else 1000
            rate_limit = product.get("rate_limit", 60) if product else 60
            await InternalServiceClient.generate_api_key(
                user_id=db_order.user_id,
                product_id=item.product_id,
                order_id=db_order.id,
                quota_limit=quota_limit,
                rate_limit=rate_limit,
            )

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
