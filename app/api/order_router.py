"""Order API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import OrderCreateDTO, OrderListItemDTO, OrderReadDTO
from app.services import OrderService

router = APIRouter(prefix="/api/order", tags=["orders"])


@router.get("", response_model=List[OrderListItemDTO], status_code=status.HTTP_200_OK)
async def list_orders(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List all orders."""
    service = OrderService(session)
    return await service.list_orders(skip, limit)


@router.get("/{order_id}", response_model=OrderReadDTO, status_code=status.HTTP_200_OK)
async def get_order(order_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get order by id."""
    service = OrderService(session)
    return await service.get_order(order_id)


@router.post("", response_model=OrderReadDTO, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    """Create a new order."""
    service = OrderService(session)
    return await service.create_order(order_data)


@router.get(
    "/customer/{customer_id}", response_model=List[OrderListItemDTO], status_code=status.HTTP_200_OK
)
async def list_customer_orders(
    customer_id: int, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List orders for a specific customer."""
    service = OrderService(session)
    return await service.list_customer_orders(customer_id, skip, limit)
