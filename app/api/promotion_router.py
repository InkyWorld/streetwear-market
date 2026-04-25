"""Promotion API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import PromotionCreateDTO, PromotionReadDTO
from app.services.promotion import PromotionService

router = APIRouter(prefix="/api/promotion", tags=["promotions"])


@router.post("", response_model=PromotionReadDTO, status_code=status.HTTP_201_CREATED)
async def create_promotion(
    promotion_data: PromotionCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    service = PromotionService(session)
    return await service.create_promotion(promotion_data)


@router.get("/active", response_model=list[PromotionReadDTO], status_code=status.HTTP_200_OK)
async def list_active_promotions(session: AsyncSession = Depends(get_db_session)):
    service = PromotionService(session)
    return await service.list_active_promotions()
