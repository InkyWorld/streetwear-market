"""Brand repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models import Brand
from app.infrastructure.persistence.repositories.base import BaseRepository


class BrandRepository(BaseRepository):
    """Repository for Brand model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Brand)

    async def get_by_name(self, name: str) -> Optional[Brand]:
        stmt = select(Brand).where(Brand.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
