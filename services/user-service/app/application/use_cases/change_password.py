from typing import Any

from app.domain.ports.password_hasher import PasswordHasherPort
from app.domain.repositories.user_repository import UserRepositoryInterface


class ChangePasswordUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, user: Any, new_password: str) -> Any:
        hashed = self._password_hasher.hash(new_password)
        return await self._user_repo.update(user, hashed_password=hashed)
