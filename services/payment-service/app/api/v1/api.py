from app.api.v1.endpoints import payment
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
