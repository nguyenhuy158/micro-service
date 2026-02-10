from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any


class TokenServicePort(ABC):
    @abstractmethod
    def create_access_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]: ...
