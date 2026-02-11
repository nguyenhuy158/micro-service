from __future__ import annotations

import abc
from uuid import UUID


class InventoryClient(abc.ABC):
    @abc.abstractmethod
    async def reserve_stock(self, product_id: UUID, quantity: int) -> bool: ...

    @abc.abstractmethod
    async def release_stock(self, product_id: UUID, quantity: int) -> bool: ...

    @abc.abstractmethod
    async def get_api_keys(self, order_id: UUID) -> list[dict]: ...

    @abc.abstractmethod
    async def generate_api_key(
        self,
        user_id: UUID,
        product_id: UUID,
        order_id: UUID,
        quota_limit: int = 1000,
        rate_limit: int = 60,
    ) -> bool: ...
