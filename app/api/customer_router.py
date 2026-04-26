"""Customer API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import (
    CustomerCreateDTO,
    CustomerListItemDTO,
    CustomerReadDTO,
    CustomerUpdateDTO,
)
from app.services import CustomerService

router = APIRouter(prefix="/api/customer", tags=["customers"])


@router.get("", response_model=List[CustomerListItemDTO], status_code=status.HTTP_200_OK)
async def list_customers(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)
):
    """List all customers."""
    service = CustomerService(session)
    return await service.list_customers(skip, limit)


@router.get("/{customer_id}", response_model=CustomerReadDTO, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get customer by id."""
    service = CustomerService(session)
    return await service.get_customer(customer_id)


@router.post("", response_model=CustomerReadDTO, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreateDTO, session: AsyncSession = Depends(get_db_session)
):
    """Create a new customer."""
    service = CustomerService(session)
    return await service.create_customer(customer_data)


@router.put("/{customer_id}", response_model=CustomerReadDTO, status_code=status.HTTP_200_OK)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdateDTO,
    session: AsyncSession = Depends(get_db_session),
):
    service = CustomerService(session)
    return await service.update_customer(customer_id, customer_data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CustomerService(session)
    await service.delete_customer(customer_id)
