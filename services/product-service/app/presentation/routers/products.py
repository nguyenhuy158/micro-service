from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.create_category import CreateCategoryUseCase
from app.application.use_cases.create_product import CreateProductUseCase
from app.application.use_cases.get_product import GetProductUseCase
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.application.use_cases.list_products import ListProductsUseCase
from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.repositories.category_repository import (
    SqlAlchemyCategoryRepository,
)
from app.infrastructure.persistence.repositories.product_repository import (
    SqlAlchemyProductRepository,
)
from app.infrastructure.search.meili_client import MeiliSearchClient, get_meili_client
from app.presentation.schemas.product import (
    Category,
    CategoryCreate,
    Product,
    ProductCreate,
)

router = APIRouter()


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    meili: MeiliSearchClient = Depends(get_meili_client),
) -> Any:
    repo = SqlAlchemyProductRepository(db)
    use_case = CreateProductUseCase(repo)
    product = await use_case.execute(product_in.model_dump())
    meili.index_product(product)
    return product


@router.get("/products/search")
async def search_products(
    q: str = Query(default="", description="Search query"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    meili: MeiliSearchClient = Depends(get_meili_client),
) -> Any:
    return meili.search(query=q, limit=limit, offset=offset)


@router.get("/products", response_model=list[Product])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    category_id: uuid.UUID | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
    sort_by: str | None = Query(
        default=None,
        pattern="^(price_asc|price_desc|name_asc|name_desc|newest)$",
    ),
    db: AsyncSession = Depends(get_db),
) -> Any:
    repo = SqlAlchemyProductRepository(db)
    use_case = ListProductsUseCase(repo)
    return await use_case.execute(
        skip=skip,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by,
    )


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Any:
    repo = SqlAlchemyProductRepository(db)
    use_case = GetProductUseCase(repo)
    product = await use_case.execute(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/categories", response_model=Category, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_in: CategoryCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    repo = SqlAlchemyCategoryRepository(db)
    use_case = CreateCategoryUseCase(repo)
    return await use_case.execute(category_in.model_dump())


@router.get("/categories", response_model=list[Category])
async def list_categories(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> Any:
    repo = SqlAlchemyCategoryRepository(db)
    use_case = ListCategoriesUseCase(repo)
    return await use_case.execute(skip, limit)
