from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.presentation.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from shared.enums.status import OrderStatus

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    *, db: AsyncSession = Depends(get_db), order_in: OrderCreate
) -> Any:
    order = await OrderService.create_order(db, order_in)
    if order.status == OrderStatus.FAILED:
        raise HTTPException(
            status_code=400,
            detail="Order creation failed (insufficient stock or payment failure)",
        )
    return order


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    order = await OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/user/{user_id}", response_model=list[OrderResponse])
async def get_user_orders(user_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    return await OrderService.get_user_orders(db, user_id)


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID, order_update: OrderUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    if order_update.status is None:
        raise HTTPException(status_code=400, detail="Status is required")
    order = await OrderService.update_order_status(db, order_id, order_update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
