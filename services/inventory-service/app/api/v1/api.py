from app.api.v1.endpoints import inventory
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
