"""Catalog service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import NotFoundError
from app.repositories import CatalogRepository
from app.schemas import CatalogCreateDTO, CatalogListDTO, CatalogReadDTO


class CatalogService:
    """Service for catalog operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.catalog_repo = CatalogRepository(session)

    async def get_catalog(self, catalog_id: int) -> CatalogReadDTO:
        """Get catalog by id."""
        catalog = await self.catalog_repo.get_by_id(catalog_id)
        if not catalog:
            raise NotFoundError(f"Catalog with id {catalog_id} not found")
        return CatalogReadDTO.model_validate(catalog)

    async def list_catalogs(self, skip: int = 0, limit: int = 100) -> List[CatalogListDTO]:
        """List all catalogs."""
        catalogs = await self.catalog_repo.get_all(skip, limit)
        return [CatalogListDTO.model_validate(c) for c in catalogs]

    async def create_catalog(self, catalog_data: CatalogCreateDTO) -> CatalogReadDTO:
        """Create a new catalog."""
        catalog = await self.catalog_repo.create(
            name=catalog_data.name, description=catalog_data.description
        )
        await self.session.commit()
        return CatalogReadDTO.model_validate(catalog)
