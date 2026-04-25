"""Inventory reservation repository."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InventoryReservation
from app.repositories.base import BaseRepository


class InventoryReservationRepository(BaseRepository[InventoryReservation]):
    """Repository for inventory reservations."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, InventoryReservation)

    async def get_held_by_order(self, order_id: int) -> list[InventoryReservation]:
        stmt = select(InventoryReservation).where(
            InventoryReservation.order_id == order_id, InventoryReservation.status == "held"
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_expired_holds(self) -> list[InventoryReservation]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        stmt = select(InventoryReservation).where(
            InventoryReservation.status == "held", InventoryReservation.expires_at < now
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
