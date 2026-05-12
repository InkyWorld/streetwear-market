"""Order API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from app.application.dto import OrderCreateDTO, OrderListItemDTO, OrderReadDTO
from app.application.orders import CreateOrderCommand, CreateOrderItemCommand
from app.presentation.dependencies import get_order_command_handler, get_order_service

router = APIRouter(prefix="/api/order", tags=["orders"])


class OrderStatusUpdateDTO(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|shipped|delivered|cancelled)$")


@router.get("", response_model=List[OrderListItemDTO], status_code=status.HTTP_200_OK)
async def list_orders(skip: int = 0, limit: int = 100, service=Depends(get_order_service)):
    return await service.list_orders(skip, limit)


@router.get("/{order_id}", response_model=OrderReadDTO, status_code=status.HTTP_200_OK)
async def get_order(order_id: int, service=Depends(get_order_service)):
    return await service.get_order(order_id)


@router.post("", response_model=OrderReadDTO, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreateDTO, handler=Depends(get_order_command_handler)):
    command = CreateOrderCommand(
        customer_id=order_data.customer_id,
        items=tuple(
            CreateOrderItemCommand(product_id=item.product_id, quantity=item.quantity)
            for item in order_data.items
        ),
    )
    return await handler.handle(command)


@router.patch("/{order_id}/status", response_model=OrderReadDTO, status_code=status.HTTP_200_OK)
async def change_order_status(
    order_id: int,
    status_data: OrderStatusUpdateDTO,
    service=Depends(get_order_service),
):
    return await service.change_order_status(order_id, status_data.status)


@router.get(
    "/customer/{customer_id}", response_model=List[OrderListItemDTO], status_code=status.HTTP_200_OK
)
async def list_customer_orders(
    customer_id: int,
    skip: int = 0,
    limit: int = 100,
    service=Depends(get_order_service),
):
    return await service.list_customer_orders(customer_id, skip, limit)
