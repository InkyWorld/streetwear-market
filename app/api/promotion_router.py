"""Promotion API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import PromotionCreateDTO, PromotionReadDTO, PromotionUpdateDTO
from app.services.promotion import PromotionService

router = APIRouter(prefix="/api/promotion", tags=["promotions"])


@router.post("", response_model=PromotionReadDTO, status_code=status.HTTP_201_CREATED)
async def create_promotion(
    promotion_data: PromotionCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    service = PromotionService(session)
    return await service.create_promotion(promotion_data)


@router.get("", response_model=list[PromotionReadDTO], status_code=status.HTTP_200_OK)
async def list_promotions(session: AsyncSession = Depends(get_db_session)):
    service = PromotionService(session)
    return await service.list_promotions()


@router.get("/{promotion_id}", response_model=PromotionReadDTO, status_code=status.HTTP_200_OK)
async def get_promotion(promotion_id: int, session: AsyncSession = Depends(get_db_session)):
    service = PromotionService(session)
    return await service.get_promotion(promotion_id)


@router.put("/{promotion_id}", response_model=PromotionReadDTO, status_code=status.HTTP_200_OK)
async def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdateDTO,
    session: AsyncSession = Depends(get_db_session),
):
    service = PromotionService(session)
    return await service.update_promotion(promotion_id, promotion_data)


@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_promotion(promotion_id: int, session: AsyncSession = Depends(get_db_session)):
    service = PromotionService(session)
    await service.delete_promotion(promotion_id)


@router.get("/active", response_model=list[PromotionReadDTO], status_code=status.HTTP_200_OK)
async def list_active_promotions(session: AsyncSession = Depends(get_db_session)):
    service = PromotionService(session)
    return await service.list_active_promotions()
