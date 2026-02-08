from typing import Any
from uuid import UUID

from app.db.session import get_db
from app.schemas.inventory import (
    ApiKeyCreate,
    ApiKeyResponse,
    InventoryCreate,
    InventoryResponse,
    StockReservation,
)
from app.services.inventory_service import InventoryService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    *, db: AsyncSession = Depends(get_db), inventory_in: InventoryCreate
) -> Any:
    inventory = await InventoryService.get_inventory_by_product(
        db, inventory_in.product_id
    )
    if inventory:
        raise HTTPException(
            status_code=400,
            detail="Inventory for this product already exists",
        )
    return await InventoryService.create_inventory(db, inventory_in)


@router.get("/{product_id}", response_model=InventoryResponse)
async def get_inventory(product_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    inventory = await InventoryService.get_inventory_by_product(db, product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.post("/reserve", status_code=status.HTTP_200_OK)
async def reserve_stock(
    *, db: AsyncSession = Depends(get_db), reservation: StockReservation
) -> Any:
    success = await InventoryService.reserve_stock(
        db, reservation.product_id, reservation.quantity
    )
    if not success:
        raise HTTPException(
            status_code=400, detail="Insufficient stock or product not found"
        )
    return {"status": "success", "message": "Stock reserved"}


@router.post("/release", status_code=status.HTTP_200_OK)
async def release_stock(
    *, db: AsyncSession = Depends(get_db), reservation: StockReservation
) -> Any:
    success = await InventoryService.release_stock(
        db, reservation.product_id, reservation.quantity
    )
    if not success:
        raise HTTPException(status_code=400, detail="Inventory not found")
    return {"status": "success", "message": "Stock released"}


@router.post(
    "/generate-key",
    response_model=ApiKeyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_api_key(
    *, db: AsyncSession = Depends(get_db), key_in: ApiKeyCreate
) -> Any:
    return await InventoryService.generate_api_key(
        db, key_in.user_id, key_in.product_id, key_in.order_id, key_in.quota_limit
    )


@router.get("/keys/order/{order_id}", response_model=list[ApiKeyResponse])
async def get_order_keys(order_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    return await InventoryService.get_api_keys_by_order(db, order_id)


@router.get("/keys/user/{user_id}", response_model=list[ApiKeyResponse])
async def get_user_keys(user_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    return await InventoryService.get_api_keys_by_user(db, user_id)
