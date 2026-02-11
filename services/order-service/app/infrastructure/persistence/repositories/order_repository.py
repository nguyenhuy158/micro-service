import uuid
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.persistence.models.order import Order, OrderItem
from shared.enums.status import OrderStatus


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, order_id: UUID) -> Any | None:
        result = await self._db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> list[Any]:
        result = await self._db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        return list(result.scalars().all())

    async def create(
        self,
        order_id: UUID,
        user_id: UUID,
        total_amount: float,
        shipping_address: str | None,
        status: OrderStatus,
        items: list[dict],
    ) -> Any:
        db_order = Order(
            id=order_id,
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            status=status,
        )
        self._db.add(db_order)
        await self._db.flush()

        for item_data in items:
            db_item = OrderItem(
                id=uuid.uuid4(),
                order_id=db_order.id,
                **item_data,
            )
            self._db.add(db_item)
            db_order.items.append(db_item)

        return db_order

    async def update_status(self, order_id: UUID, status: OrderStatus) -> Any | None:
        result = await self._db.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )
        db_order = result.scalar_one_or_none()
        if db_order:
            db_order.status = status
        return db_order

    async def commit(self) -> None:
        await self._db.commit()

    async def refresh(self, obj: Any) -> None:
        await self._db.refresh(obj)
