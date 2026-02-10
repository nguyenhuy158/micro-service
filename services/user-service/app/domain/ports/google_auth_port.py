from abc import ABC, abstractmethod


class GoogleAuthPort(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> dict: ...
