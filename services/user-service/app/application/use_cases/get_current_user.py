from typing import Any

from app.domain.ports.token_service import TokenServicePort
from app.domain.repositories.user_repository import UserRepositoryInterface


class GetCurrentUserUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        token_service: TokenServicePort,
    ) -> None:
        self._user_repo = user_repo
        self._token_service = token_service

    async def execute(self, token: str) -> Any | None:
        payload = self._token_service.decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            return None
        return await self._user_repo.get_by_email(sub)
