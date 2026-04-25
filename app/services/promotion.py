"""Promotion service."""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.validators import validate_promotion_window
from app.repositories import PromotionRepository
from app.schemas import PromotionCreateDTO, PromotionReadDTO


class PromotionService:
    """Application service for promotion CRUD and activation logic."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PromotionRepository(session)

    async def create_promotion(self, dto: PromotionCreateDTO) -> PromotionReadDTO:
        validate_promotion_window(dto.active_from, dto.active_to)
        promotion = await self.repo.create(**dto.model_dump())
        await self.session.commit()
        return PromotionReadDTO.model_validate(promotion)

    async def list_active_promotions(self) -> list[PromotionReadDTO]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        promotions = await self.repo.get_active(now)
        return [PromotionReadDTO.model_validate(item) for item in promotions]
