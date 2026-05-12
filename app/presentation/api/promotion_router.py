"""Promotion API router."""

from fastapi import APIRouter, Depends, status

from app.application.dto import PromotionCreateDTO, PromotionReadDTO, PromotionUpdateDTO
from app.presentation.dependencies import PromotionService, get_promotion_service

router = APIRouter(prefix="/api/promotion", tags=["promotions"])


@router.post("", response_model=PromotionReadDTO, status_code=status.HTTP_201_CREATED)
async def create_promotion(
    promotion_data: PromotionCreateDTO,
    service: PromotionService = Depends(get_promotion_service),
):
    return await service.create_promotion(promotion_data)


@router.get("", response_model=list[PromotionReadDTO], status_code=status.HTTP_200_OK)
async def list_promotions(service: PromotionService = Depends(get_promotion_service)):
    return await service.list_promotions()


@router.get("/{promotion_id}", response_model=PromotionReadDTO, status_code=status.HTTP_200_OK)
async def get_promotion(promotion_id: int, service: PromotionService = Depends(get_promotion_service)):
    return await service.get_promotion(promotion_id)


@router.put("/{promotion_id}", response_model=PromotionReadDTO, status_code=status.HTTP_200_OK)
async def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdateDTO,
    service: PromotionService = Depends(get_promotion_service),
):
    return await service.update_promotion(promotion_id, promotion_data)


@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_promotion(
    promotion_id: int,
    service: PromotionService = Depends(get_promotion_service),
):
    await service.delete_promotion(promotion_id)


@router.get("/active", response_model=list[PromotionReadDTO], status_code=status.HTTP_200_OK)
async def list_active_promotions(service: PromotionService = Depends(get_promotion_service)):
    return await service.list_active_promotions()
