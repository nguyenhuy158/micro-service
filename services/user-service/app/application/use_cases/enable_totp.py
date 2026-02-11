from typing import Any

from app.domain.ports.totp_service import TotpServicePort
from app.domain.repositories.user_repository import UserRepositoryInterface


class EnableTotpUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        totp_service: TotpServicePort,
    ) -> None:
        self._user_repo = user_repo
        self._totp_service = totp_service

    async def execute(self, user: Any, secret: str, code: str) -> Any:
        if not self._totp_service.verify_code(secret, code):
            return None
        return await self._user_repo.update(
            user, totp_secret=secret, is_totp_enabled=True
        )
