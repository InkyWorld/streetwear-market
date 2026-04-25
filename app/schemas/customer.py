"""Customer DTO schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreateDTO(BaseModel):
    """Schema for creating a customer."""

    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)


class CustomerReadDTO(BaseModel):
    """Schema for reading a customer."""

    id: int
    full_name: str
    email: str
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerListItemDTO(BaseModel):
    """Schema for listing customers."""

    id: int
    full_name: str
    email: str
    phone: Optional[str]

    model_config = ConfigDict(from_attributes=True)
