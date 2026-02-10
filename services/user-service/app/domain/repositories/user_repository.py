from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Any | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None: ...

    @abstractmethod
    async def get_by_google_id(self, google_id: str) -> Any | None: ...

    @abstractmethod
    async def create(
        self,
        email: str,
        hashed_password: str | None,
        full_name: str | None,
        role: Any,
        is_active: bool,
        google_id: str | None = None,
    ) -> Any: ...

    @abstractmethod
    async def update(self, user: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    async def has_any_user(self) -> bool: ...
