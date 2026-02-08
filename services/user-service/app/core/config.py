from typing import List, Union
from pydantic import AnyHttpUrl, validator
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

    class Config:
        case_sensitive = True


settings = Settings()
