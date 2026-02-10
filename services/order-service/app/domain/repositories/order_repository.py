from __future__ import annotations

import abc
from typing import Any
from uuid import UUID

from shared.enums.status import OrderStatus


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, order_id: UUID) -> Any | None: ...

    @abc.abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Any]: ...

    @abc.abstractmethod
    async def create(
        self,
        order_id: UUID,
        user_id: UUID,
        total_amount: float,
        shipping_address: str | None,
        status: OrderStatus,
        items: list[dict],
    ) -> Any: ...

    @abc.abstractmethod
    async def update_status(
        self, order_id: UUID, status: OrderStatus
    ) -> Any | None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def refresh(self, obj: Any) -> None: ...
