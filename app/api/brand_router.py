"""Brand API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import BrandCreateDTO, BrandReadDTO
from app.services import BrandService

router = APIRouter(prefix="/api/brand", tags=["brands"])


@router.get("", response_model=List[BrandReadDTO], status_code=status.HTTP_200_OK)
async def list_brands(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List all brands."""
    service = BrandService(session)
    return await service.list_brands(skip, limit)


@router.get("/{brand_id}", response_model=BrandReadDTO, status_code=status.HTTP_200_OK)
async def get_brand(brand_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get brand by id."""
    service = BrandService(session)
    return await service.get_brand(brand_id)


@router.post("", response_model=BrandReadDTO, status_code=status.HTTP_201_CREATED)
async def create_brand(brand_data: BrandCreateDTO, session: AsyncSession = Depends(get_db_session)):
    """Create a new brand."""
    service = BrandService(session)
    return await service.create_brand(brand_data)
