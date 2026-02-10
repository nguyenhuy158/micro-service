from typing import Any

from app.domain.ports.google_auth_port import GoogleAuthPort
from app.domain.repositories.user_repository import UserRepositoryInterface


class LoginGoogleUseCase:
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        google_auth: GoogleAuthPort,
    ) -> None:
        self._user_repo = user_repo
        self._google_auth = google_auth

    async def execute(self, id_token: str) -> tuple[Any, dict]:
        google_data = await self._google_auth.verify_token(id_token)
        google_id = google_data["sub"]
        email = google_data["email"]
        name = google_data.get("name")

        user = await self._user_repo.get_by_google_id(google_id)
        if not user:
            user = await self._user_repo.get_by_email(email)
            if user:
                user = await self._user_repo.update(user, google_id=google_id)
            else:
                user = await self._user_repo.create(
                    email=email,
                    google_id=google_id,
                    full_name=name,
                    hashed_password=None,
                    role=None,
                    is_active=True,
                )

        return user, google_data
