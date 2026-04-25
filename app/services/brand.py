"""Brand service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import NotFoundError
from app.repositories import BrandRepository
from app.schemas import BrandCreateDTO, BrandReadDTO


class BrandService:
    """Service for brand operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.brand_repo = BrandRepository(session)

    async def get_brand(self, brand_id: int) -> BrandReadDTO:
        """Get brand by id."""
        brand = await self.brand_repo.get_by_id(brand_id)
        if not brand:
            raise NotFoundError(f"Brand with id {brand_id} not found")
        return BrandReadDTO.model_validate(brand)

    async def list_brands(self, skip: int = 0, limit: int = 100) -> List[BrandReadDTO]:
        """List all brands."""
        brands = await self.brand_repo.get_all(skip, limit)
        return [BrandReadDTO.model_validate(b) for b in brands]

    async def create_brand(self, brand_data: BrandCreateDTO) -> BrandReadDTO:
        """Create a new brand."""
        brand = await self.brand_repo.create(
            name=brand_data.name, description=brand_data.description
        )
        await self.session.commit()
        return BrandReadDTO.model_validate(brand)
