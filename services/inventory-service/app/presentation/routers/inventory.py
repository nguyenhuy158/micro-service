from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.create_inventory import CreateInventoryUseCase
from app.application.use_cases.generate_api_key import GenerateApiKeyUseCase
from app.application.use_cases.get_api_keys import GetApiKeysUseCase
from app.application.use_cases.get_inventory import GetInventoryUseCase
from app.application.use_cases.release_stock import ReleaseStockUseCase
from app.application.use_cases.reserve_stock import ReserveStockUseCase
from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.repositories.api_key_repository import (
    SqlAlchemyApiKeyRepository,
)
from app.infrastructure.persistence.repositories.inventory_repository import (
    SqlAlchemyInventoryRepository,
)
from app.presentation.schemas.inventory import (
    ApiKeyCreate,
    InventoryCreate,
    InventoryResponse,
    StockReservation,
)
from shared.schemas.api_key import ApiKeyResponse

router = APIRouter()

_inventory_repo = SqlAlchemyInventoryRepository()
_api_key_repo = SqlAlchemyApiKeyRepository()


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    *, db: AsyncSession = Depends(get_db), inventory_in: InventoryCreate
) -> Any:
    use_case = CreateInventoryUseCase(_inventory_repo)
    try:
        return await use_case.execute(db, inventory_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{product_id}", response_model=InventoryResponse)
async def get_inventory(product_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    use_case = GetInventoryUseCase(_inventory_repo)
    inventory = await use_case.execute(db, product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.post("/reserve", status_code=status.HTTP_200_OK)
async def reserve_stock(
    *, db: AsyncSession = Depends(get_db), reservation: StockReservation
) -> Any:
    use_case = ReserveStockUseCase(_inventory_repo)
    success = await use_case.execute(db, reservation.product_id, reservation.quantity)
    if not success:
        raise HTTPException(
            status_code=400, detail="Insufficient stock or product not found"
        )
    return {"status": "success", "message": "Stock reserved"}


@router.post("/release", status_code=status.HTTP_200_OK)
async def release_stock(
    *, db: AsyncSession = Depends(get_db), reservation: StockReservation
) -> Any:
    use_case = ReleaseStockUseCase(_inventory_repo)
    success = await use_case.execute(db, reservation.product_id, reservation.quantity)
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
    use_case = GenerateApiKeyUseCase(_api_key_repo)
    return await use_case.execute(
        db,
        key_in.user_id,
        key_in.product_id,
        key_in.order_id,
        key_in.quota_limit,
        key_in.rate_limit,
    )


@router.get("/keys/order/{order_id}", response_model=list[ApiKeyResponse])
async def get_order_keys(order_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    use_case = GetApiKeysUseCase(_api_key_repo)
    return await use_case.get_by_order(db, order_id)


@router.get("/keys/user/{user_id}", response_model=list[ApiKeyResponse])
async def get_user_keys(user_id: UUID, db: AsyncSession = Depends(get_db)) -> Any:
    use_case = GetApiKeysUseCase(_api_key_repo)
    return await use_case.get_by_user(db, user_id)
