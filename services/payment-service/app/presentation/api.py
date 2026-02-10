from fastapi import APIRouter

from app.presentation.routers import payment

api_router = APIRouter()
api_router.include_router(payment.router, prefix="/payments", tags=["payments"])
