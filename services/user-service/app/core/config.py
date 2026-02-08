from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "User Service"
    API_V1_STR: str = "/api/v1"

    # SECURITY
    SECRET_KEY: str = "your-secret-key-change-me"  # Should be loaded from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # DATABASE
    DATABASE_URL: str

    # RABBITMQ
    RABBITMQ_URL: str

    # GOOGLE OAUTH
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None

    class Config:
        case_sensitive = True


settings = Settings()
