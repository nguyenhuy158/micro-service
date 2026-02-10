import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware, metrics

from app.api.api import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: Create tables (In production, use Alembic!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data
    async with SessionLocal() as db:
        await init_db(db)

    yield

    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# Ensure static directory exists
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(static_dir):
    os.makedirs(os.path.join(static_dir, "avatars"), exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check() -> Any:
    return {"status": "ok", "service": "user-service"}


@app.get("/")
def root() -> Any:
    return {"message": "Welcome to User Service"}
