"""Customer API router."""

from typing import List

from fastapi import APIRouter, Depends, status

from app.application.dto import (
    CustomerCreateDTO,
    CustomerListItemDTO,
    CustomerReadDTO,
    CustomerUpdateDTO,
)
from app.presentation.dependencies import get_customer_service

router = APIRouter(prefix="/api/customer", tags=["customers"])


@router.get("", response_model=List[CustomerListItemDTO], status_code=status.HTTP_200_OK)
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    service=Depends(get_customer_service),
):
    return await service.list_customers(skip, limit)


@router.get("/{customer_id}", response_model=CustomerReadDTO, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, service=Depends(get_customer_service)):
    return await service.get_customer(customer_id)


@router.post("", response_model=CustomerReadDTO, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreateDTO,
    service=Depends(get_customer_service),
):
    return await service.create_customer(customer_data)


@router.put("/{customer_id}", response_model=CustomerReadDTO, status_code=status.HTTP_200_OK)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdateDTO,
    service=Depends(get_customer_service),
):
    return await service.update_customer(customer_id, customer_data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, service=Depends(get_customer_service)):
    await service.delete_customer(customer_id)
