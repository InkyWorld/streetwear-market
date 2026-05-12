"""Catalog API router."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.application.dto import CatalogCreateDTO, CatalogListDTO, CatalogReadDTO, CatalogUpdateDTO
from app.presentation.dependencies import get_catalog_service

router = APIRouter(prefix="/api/catalog", tags=["catalogs"])


@router.get("", response_model=List[CatalogListDTO], status_code=status.HTTP_200_OK)
async def list_catalogs(
    skip: int = 0,
    limit: int = 100,
    service=Depends(get_catalog_service),
):
    return await service.list_catalogs(skip, limit)


@router.get("/{catalog_id}", response_model=CatalogReadDTO, status_code=status.HTTP_200_OK)
async def get_catalog(catalog_id: int, service=Depends(get_catalog_service)):
    return await service.get_catalog(catalog_id)


@router.post("", response_model=CatalogReadDTO, status_code=status.HTTP_201_CREATED)
async def create_catalog(
    catalog_data: CatalogCreateDTO,
    service=Depends(get_catalog_service),
):
    return await service.create_catalog(catalog_data)


@router.put("/{catalog_id}", response_model=CatalogReadDTO, status_code=status.HTTP_200_OK)
async def update_catalog(
    catalog_id: int,
    catalog_data: CatalogUpdateDTO,
    service=Depends(get_catalog_service),
):
    return await service.update_catalog(catalog_id, catalog_data)


@router.delete("/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog(catalog_id: int, service=Depends(get_catalog_service)):
    await service.delete_catalog(catalog_id)
