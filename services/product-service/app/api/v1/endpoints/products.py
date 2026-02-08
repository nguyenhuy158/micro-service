from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate, Category, CategoryCreate
from app.services.product_service import product_service


router = APIRouter()


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(db, product_in)


@router.get("/products", response_model=List[Product])
async def list_products(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await product_service.get_products(db, skip, limit)


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/categories", response_model=Category, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_in: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    return await product_service.create_category(db, category_in)


@router.get("/categories", response_model=List[Category])
async def list_categories(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await product_service.get_categories(db, skip, limit)
