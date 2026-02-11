import uuid
from typing import Any

from app.domain.ports.inventory_client import InventoryClient
from app.domain.ports.payment_client import PaymentClient
from app.domain.ports.product_client import ProductClient
from app.domain.repositories.order_repository import OrderRepository
from app.presentation.schemas.order import OrderCreate
from shared.enums.status import OrderStatus


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        inventory_client: InventoryClient,
        payment_client: PaymentClient,
        product_client: ProductClient,
    ) -> None:
        self._repository = repository
        self._inventory_client = inventory_client
        self._payment_client = payment_client
        self._product_client = product_client

    async def execute(self, order_in: OrderCreate) -> Any:
        total_amount = sum(item.price * item.quantity for item in order_in.items)

        items_data = [item.model_dump() for item in order_in.items]

        db_order = await self._repository.create(
            order_id=uuid.uuid4(),
            user_id=order_in.user_id,
            total_amount=total_amount,
            shipping_address=order_in.shipping_address,
            status=OrderStatus.PENDING,
            items=items_data,
        )

        reserved_items = []
        stock_success = True
        for item in order_in.items:
            success = await self._inventory_client.reserve_stock(
                item.product_id, item.quantity
            )
            if not success:
                stock_success = False
                break
            reserved_items.append(item)

        if not stock_success:
            for item in reserved_items:
                await self._inventory_client.release_stock(
                    item.product_id, item.quantity
                )
            db_order.status = OrderStatus.FAILED
            await self._repository.commit()
            await self._repository.refresh(db_order)
            return db_order

        payment_success = await self._payment_client.process_payment(
            db_order.id, total_amount
        )
        if not payment_success:
            for item in reserved_items:
                await self._inventory_client.release_stock(
                    item.product_id, item.quantity
                )
            db_order.status = OrderStatus.FAILED
            await self._repository.commit()
            await self._repository.refresh(db_order)
            return db_order

        db_order.status = OrderStatus.PAID
        await self._repository.commit()
        await self._repository.refresh(db_order)

        for item in db_order.items:
            product = await self._product_client.get_product(item.product_id)
            quota_limit = product.get("quota_limit", 1000) if product else 1000
            rate_limit = product.get("rate_limit", 60) if product else 60
            await self._inventory_client.generate_api_key(
                user_id=db_order.user_id,
                product_id=item.product_id,
                order_id=db_order.id,
                quota_limit=quota_limit,
                rate_limit=rate_limit,
            )

        return db_order
