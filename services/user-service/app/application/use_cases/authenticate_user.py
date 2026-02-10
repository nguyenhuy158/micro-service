from typing import Any

from app.domain.ports.password_hasher import PasswordHasherPort
from app.domain.repositories.user_repository import UserRepositoryInterface


class AuthenticateUserUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> Any | None:
        user = await self._user_repo.get_by_email(email)
        if not user or not user.hashed_password:
            return None
        if not self._password_hasher.verify(password, user.hashed_password):
            return None
        return user
