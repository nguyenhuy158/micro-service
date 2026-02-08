from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Product Service"
    API_V1_STR: str = "/api/v1"

    # DATABASE
    DATABASE_URL: str

    # RABBITMQ
    RABBITMQ_URL: str

    # MEILISEARCH
    MEILISEARCH_URL: str
    MEILISEARCH_KEY: str

    class Config:
        case_sensitive = True


settings = Settings()
