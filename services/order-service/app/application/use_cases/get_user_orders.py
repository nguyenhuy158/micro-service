from typing import Any
from uuid import UUID

from app.domain.ports.inventory_client import InventoryClient
from app.domain.repositories.order_repository import OrderRepository


class GetUserOrdersUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        inventory_client: InventoryClient,
    ) -> None:
        self._repository = repository
        self._inventory_client = inventory_client

    async def execute(self, user_id: UUID) -> list[Any]:
        orders = await self._repository.get_by_user_id(user_id)
        for order in orders:
            order.api_keys = await self._inventory_client.get_api_keys(order.id)
        return orders
