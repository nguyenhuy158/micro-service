from typing import Any

from app.domain.repositories.user_repository import UserRepositoryInterface


class DisableTotpUseCase:
    def __init__(self, user_repo: UserRepositoryInterface) -> None:
        self._user_repo = user_repo

    async def execute(self, user: Any) -> Any:
        return await self._user_repo.update(
            user, totp_secret=None, is_totp_enabled=False
        )
