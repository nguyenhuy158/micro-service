from typing import Any

from app.domain.ports.password_hasher import PasswordHasherPort
from app.domain.repositories.user_repository import UserRepositoryInterface
from shared.enums.status import UserRole


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(
        self,
        email: str,
        password: str,
        full_name: str | None = None,
        role: UserRole | None = UserRole.CUSTOMER,
    ) -> Any:
        hashed_password = self._password_hasher.hash(password)
        return await self._user_repo.create(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            is_active=True,
        )
