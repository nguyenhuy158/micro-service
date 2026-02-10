from __future__ import annotations

import abc
from uuid import UUID


class ProductClient(abc.ABC):
    @abc.abstractmethod
    async def get_product(self, product_id: UUID) -> dict | None: ...
