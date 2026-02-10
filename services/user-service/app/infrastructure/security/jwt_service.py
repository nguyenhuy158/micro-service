from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.domain.ports.token_service import TokenServicePort
from app.infrastructure.config import settings


class JoseJwtService(TokenServicePort):
    def __init__(
        self,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
        default_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._default_expire_minutes = default_expire_minutes

    def create_access_token(
        self, subject: str | Any, expires_delta: timedelta | None = None
    ) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta  # noqa: UP017
        else:
            delta = timedelta(minutes=self._default_expire_minutes)
            expire = datetime.now(timezone.utc) + delta  # noqa: UP017
        to_encode = {"exp": expire, "sub": str(subject)}
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
