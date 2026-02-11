from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from shared.version import VERSION


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "User Service"
    API_V1_STR: str = "/api/v1"
    VERSION: str = VERSION

    # SECURITY
    SECRET_KEY: str = "your-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # DATABASE
    DATABASE_URL: str

    # RABBITMQ
    RABBITMQ_URL: str

    # GOOGLE OAUTH
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None


settings = Settings()
