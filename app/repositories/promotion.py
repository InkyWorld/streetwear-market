"""Promotion repository."""

from datetime import datetime

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Promotion
from app.repositories.base import BaseRepository


class PromotionRepository(BaseRepository[Promotion]):
    """Repository for promotion model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Promotion)

    async def get_active(self, now: datetime) -> list[Promotion]:
        """Return active promotions for a point in time."""
        stmt = (
            select(Promotion)
            .where(Promotion.is_active.is_(True))
            .where(or_(Promotion.active_from.is_(None), Promotion.active_from <= now))
            .where(or_(Promotion.active_to.is_(None), Promotion.active_to >= now))
            .where(and_(Promotion.discount_percentage > 0, Promotion.discount_percentage <= 1))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
