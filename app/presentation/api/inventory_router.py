"""Inventory API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto import InventoryReleaseOrderDTO, InventoryReleaseResultDTO
from app.core.database import get_db_session
from app.presentation.dependencies import get_inventory_service

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/release", response_model=InventoryReleaseResultDTO, status_code=status.HTTP_200_OK)
async def release_order_holds(
    payload: InventoryReleaseOrderDTO,
    service=Depends(get_inventory_service),
    session: AsyncSession = Depends(get_db_session),
):
    released = await service.release_holds_for_order(payload.order_id, reason="manual_release")
    await session.commit()
    return InventoryReleaseResultDTO(released_count=released)


@router.post(
    "/release-expired",
    response_model=InventoryReleaseResultDTO,
    status_code=status.HTTP_200_OK,
)
async def release_expired_holds(service=Depends(get_inventory_service)):
    released = await service.release_expired_holds()
    return InventoryReleaseResultDTO(released_count=released)
