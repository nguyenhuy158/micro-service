from typing import Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infrastructure.config import settings
from app.presentation.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, version=settings.VERSION, openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check() -> Any:
    return {"status": "healthy", "service": settings.PROJECT_NAME}
