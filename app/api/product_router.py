"""API routers."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import ProductCreateDTO, ProductListItemDTO, ProductReadDTO, ProductUpdateDTO
from app.services import ProductService

router = APIRouter(prefix="/api/product", tags=["products"])


@router.get("", response_model=List[ProductListItemDTO], status_code=status.HTTP_200_OK)
async def list_products(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List all products."""
    service = ProductService(session)
    return await service.list_products(skip, limit)


@router.get("/{product_id}", response_model=ProductReadDTO, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get product by id."""
    service = ProductService(session)
    return await service.get_product(product_id)


@router.post("", response_model=ProductReadDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    """Create a new product."""
    service = ProductService(session)
    return await service.create_product(product_data)


@router.put("/{product_id}", response_model=ProductReadDTO, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_data: ProductUpdateDTO,
    session: AsyncSession = Depends(get_db_session),
):
    """Update a product."""
    service = ProductService(session)
    return await service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete a product."""
    service = ProductService(session)
    await service.delete_product(product_id)
