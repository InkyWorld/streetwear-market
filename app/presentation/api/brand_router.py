"""Brand API router."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.application.dto import BrandCreateDTO, BrandReadDTO, BrandUpdateDTO
from app.presentation.dependencies import get_brand_service

router = APIRouter(prefix="/api/brand", tags=["brands"])


@router.get("", response_model=List[BrandReadDTO], status_code=status.HTTP_200_OK)
async def list_brands(
    skip: int = 0,
    limit: int = 100,
    service=Depends(get_brand_service),
):
    return await service.list_brands(skip, limit)


@router.get("/{brand_id}", response_model=BrandReadDTO, status_code=status.HTTP_200_OK)
async def get_brand(brand_id: int, service=Depends(get_brand_service)):
    return await service.get_brand(brand_id)


@router.post("", response_model=BrandReadDTO, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_data: BrandCreateDTO,
    service=Depends(get_brand_service),
):
    return await service.create_brand(brand_data)


@router.put("/{brand_id}", response_model=BrandReadDTO, status_code=status.HTTP_200_OK)
async def update_brand(
    brand_id: int,
    brand_data: BrandUpdateDTO,
    service=Depends(get_brand_service),
):
    return await service.update_brand(brand_id, brand_data)


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(brand_id: int, service=Depends(get_brand_service)):
    await service.delete_brand(brand_id)
