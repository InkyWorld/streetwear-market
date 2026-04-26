"""Catalog API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import CatalogCreateDTO, CatalogListDTO, CatalogReadDTO, CatalogUpdateDTO
from app.services import CatalogService

router = APIRouter(prefix="/api/catalog", tags=["catalogs"])


@router.get("", response_model=List[CatalogListDTO], status_code=status.HTTP_200_OK)
async def list_catalogs(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List all catalogs."""
    service = CatalogService(session)
    return await service.list_catalogs(skip, limit)


@router.get("/{catalog_id}", response_model=CatalogReadDTO, status_code=status.HTTP_200_OK)
async def get_catalog(catalog_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get catalog by id."""
    service = CatalogService(session)
    return await service.get_catalog(catalog_id)


@router.post("", response_model=CatalogReadDTO, status_code=status.HTTP_201_CREATED)
async def create_catalog(
    catalog_data: CatalogCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    """Create a new catalog."""
    service = CatalogService(session)
    return await service.create_catalog(catalog_data)


@router.put("/{catalog_id}", response_model=CatalogReadDTO, status_code=status.HTTP_200_OK)
async def update_catalog(
    catalog_id: int,
    catalog_data: CatalogUpdateDTO,
    session: AsyncSession = Depends(get_db_session),
):
    service = CatalogService(session)
    return await service.update_catalog(catalog_id, catalog_data)


@router.delete("/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog(catalog_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CatalogService(session)
    await service.delete_catalog(catalog_id)
