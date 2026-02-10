import uuid
from abc import ABC, abstractmethod
from typing import Any


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> Any: ...

    @abstractmethod
    async def get_by_id(self, product_id: uuid.UUID) -> Any | None: ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[Any]: ...
