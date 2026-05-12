"""Customer repository."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models import Customer
from app.infrastructure.persistence.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Repository for Customer model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Customer)

    async def get_by_email(self, email: str) -> Optional[Customer]:
        stmt = select(Customer).where(Customer.email == email.lower())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        stmt = select(func.count()).select_from(Customer).where(Customer.email == email.lower())
        if exclude_id is not None:
            stmt = stmt.where(Customer.id != exclude_id)
        result = await self.session.execute(stmt)
        return result.scalar_one() > 0
