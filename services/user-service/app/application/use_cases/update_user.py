from typing import Any

from app.domain.ports.password_hasher import PasswordHasherPort
from app.domain.repositories.user_repository import UserRepositoryInterface


class UpdateUserUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, user: Any, update_data: dict[str, Any]) -> Any:
        if update_data.get("password"):
            hashed_password = self._password_hasher.hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            del update_data["password"]

        return await self._user_repo.update(user, **update_data)
