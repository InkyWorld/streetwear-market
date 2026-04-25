"""Product repository."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    """Repository for Product model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        stmt = select(Product).where(Product.sku == sku.upper())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def sku_exists(self, sku: str, exclude_id: Optional[int] = None) -> bool:
        """Check if SKU exists."""
        stmt = select(func.count()).select_from(Product).where(Product.sku == sku.upper())
        if exclude_id:
            stmt = stmt.where(Product.id != exclude_id)
        result = await self.session.execute(stmt)
        return result.scalar() > 0

    async def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100):
        """Get products by category."""
        stmt = select(Product).where(Product.category_id == category_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_brand(self, brand_id: int, skip: int = 0, limit: int = 100):
        """Get products by brand."""
        stmt = select(Product).where(Product.brand_id == brand_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_in_stock(self, skip: int = 0, limit: int = 100):
        """Get products in stock."""
        stmt = select(Product).where(Product.in_stock).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
