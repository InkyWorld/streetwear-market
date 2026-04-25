"""Order and OrderItem DTO schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreateDTO(BaseModel):
    """Schema for creating an order item."""

    product_id: int = Field(...)
    quantity: int = Field(..., gt=0)


class OrderItemReadDTO(BaseModel):
    """Schema for reading an order item."""

    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderCreateDTO(BaseModel):
    """Schema for creating an order."""

    customer_id: int = Field(...)
    items: List[OrderItemCreateDTO] = Field(..., min_length=1)


class OrderReadDTO(BaseModel):
    """Schema for reading an order."""

    id: int
    customer_id: int
    status: str
    total_amount: float
    items: List[OrderItemReadDTO]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderListItemDTO(BaseModel):
    """Schema for listing orders."""

    id: int
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
