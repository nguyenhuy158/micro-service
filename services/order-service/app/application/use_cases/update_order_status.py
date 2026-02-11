from typing import Any
from uuid import UUID

from app.domain.ports.inventory_client import InventoryClient
from app.domain.repositories.order_repository import OrderRepository
from shared.enums.status import OrderStatus


class UpdateOrderStatusUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        inventory_client: InventoryClient,
    ) -> None:
        self._repository = repository
        self._inventory_client = inventory_client

    async def execute(self, order_id: UUID, status: OrderStatus) -> Any | None:
        db_order = await self._repository.get_by_id(order_id)
        if db_order:
            db_order.api_keys = await self._inventory_client.get_api_keys(order_id)
            db_order.status = status
            await self._repository.commit()
            await self._repository.refresh(db_order)
        return db_order
