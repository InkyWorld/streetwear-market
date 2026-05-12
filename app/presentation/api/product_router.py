"""API routers."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.application.dto import ProductCreateDTO, ProductListItemDTO, ProductReadDTO, ProductUpdateDTO
from app.presentation.dependencies import get_product_service

router = APIRouter(prefix="/api/product", tags=["products"])


@router.get("", response_model=List[ProductListItemDTO], status_code=status.HTTP_200_OK)
async def list_products(
    skip: int = 0,
    limit: int = 100,
    service=Depends(get_product_service),
):
    return await service.list_products(skip, limit)


@router.get("/{product_id}", response_model=ProductReadDTO, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, service=Depends(get_product_service)):
    return await service.get_product(product_id)


@router.post("", response_model=ProductReadDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO,
    service=Depends(get_product_service),
):
    return await service.create_product(product_data)


@router.put("/{product_id}", response_model=ProductReadDTO, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_data: ProductUpdateDTO,
    service=Depends(get_product_service),
):
    return await service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service=Depends(get_product_service)):
    await service.delete_product(product_id)
