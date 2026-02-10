from typing import Any

from app.domain.repositories.user_repository import UserRepositoryInterface


class UploadAvatarUseCase:
    def __init__(self, user_repo: UserRepositoryInterface) -> None:
        self._user_repo = user_repo

    async def execute(self, user: Any, avatar_url: str) -> Any:
        return await self._user_repo.update(user, avatar_url=avatar_url)
