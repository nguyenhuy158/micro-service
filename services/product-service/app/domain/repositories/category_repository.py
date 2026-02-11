from abc import ABC, abstractmethod
from typing import Any


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> Any: ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[Any]: ...
