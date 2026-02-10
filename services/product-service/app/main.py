from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.infrastructure.config import settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.init_db import init_db
from app.infrastructure.db.session import SessionLocal, engine
from app.presentation.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        await init_db(db)

    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


app.include_router(api_router, prefix=settings.API_V1_STR, tags=["products"])


@app.get("/health")
def health_check() -> Any:
    return {"status": "ok"}
