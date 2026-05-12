"""Catalog service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto import CatalogCreateDTO, CatalogListDTO, CatalogReadDTO, CatalogUpdateDTO
from app.application.ports.persistence import CatalogRepositoryPort
from app.domain.exceptions import NotFoundError


class CatalogService:
    """Service for catalog operations."""

    def __init__(self, session: AsyncSession, catalog_repo: CatalogRepositoryPort):
        self.session = session
        self.catalog_repo = catalog_repo

    async def get_catalog(self, catalog_id: int) -> CatalogReadDTO:
        catalog = await self.catalog_repo.get_by_id(catalog_id)
        if not catalog:
            raise NotFoundError(f"Catalog with id {catalog_id} not found")
        return CatalogReadDTO.model_validate(catalog)

    async def list_catalogs(self, skip: int = 0, limit: int = 100) -> List[CatalogListDTO]:
        catalogs = await self.catalog_repo.get_all(skip, limit)
        return [CatalogListDTO.model_validate(c) for c in catalogs]

    async def create_catalog(self, catalog_data: CatalogCreateDTO) -> CatalogReadDTO:
        catalog = await self.catalog_repo.create(name=catalog_data.name, description=catalog_data.description)
        await self.session.commit()
        return CatalogReadDTO.model_validate(catalog)

    async def update_catalog(self, catalog_id: int, catalog_data: CatalogUpdateDTO) -> CatalogReadDTO:
        catalog = await self.catalog_repo.update(
            catalog_id, name=catalog_data.name, description=catalog_data.description
        )
        if not catalog:
            raise NotFoundError(f"Catalog with id {catalog_id} not found")
        await self.session.commit()
        return CatalogReadDTO.model_validate(catalog)

    async def delete_catalog(self, catalog_id: int) -> None:
        deleted = await self.catalog_repo.delete(catalog_id)
        if not deleted:
            raise NotFoundError(f"Catalog with id {catalog_id} not found")
        await self.session.commit()
