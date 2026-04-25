"""Catalog repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Catalog
from app.repositories.base import BaseRepository


class CatalogRepository(BaseRepository):
    """Repository for Catalog model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Catalog)

    async def get_by_name(self, name: str) -> Optional[Catalog]:
        """Get catalog by name."""
        stmt = select(Catalog).where(Catalog.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
