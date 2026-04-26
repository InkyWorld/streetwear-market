"""Promotion service."""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.validators import validate_promotion_window
from app.repositories import PromotionRepository
from app.schemas import PromotionCreateDTO, PromotionReadDTO, PromotionUpdateDTO


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

    async def list_promotions(self) -> list[PromotionReadDTO]:
        promotions = await self.repo.get_all()
        return [PromotionReadDTO.model_validate(item) for item in promotions]

    async def get_promotion(self, promotion_id: int) -> PromotionReadDTO:
        promotion = await self.repo.get_by_id(promotion_id)
        if not promotion:
            raise NotFoundError(f"Promotion with id {promotion_id} not found")
        return PromotionReadDTO.model_validate(promotion)

    async def update_promotion(self, promotion_id: int, dto: PromotionUpdateDTO) -> PromotionReadDTO:
        promotion = await self.repo.get_by_id(promotion_id)
        if not promotion:
            raise NotFoundError(f"Promotion with id {promotion_id} not found")

        active_from = dto.active_from if dto.active_from is not None else promotion.active_from
        active_to = dto.active_to if dto.active_to is not None else promotion.active_to
        validate_promotion_window(active_from, active_to)

        promotion_type = dto.promotion_type if dto.promotion_type is not None else promotion.promotion_type
        category_id = dto.category_id if dto.category_id is not None else promotion.category_id
        if promotion_type == "category" and category_id is None:
            raise ValidationError("category_id is required for category promotions")

        updated = await self.repo.update(
            promotion_id,
            name=dto.name,
            promotion_type=dto.promotion_type,
            discount_percentage=dto.discount_percentage,
            category_id=dto.category_id,
            active_from=dto.active_from,
            active_to=dto.active_to,
            is_active=dto.is_active,
        )
        await self.session.commit()
        return PromotionReadDTO.model_validate(updated)

    async def delete_promotion(self, promotion_id: int) -> None:
        deleted = await self.repo.delete(promotion_id)
        if not deleted:
            raise NotFoundError(f"Promotion with id {promotion_id} not found")
        await self.session.commit()
