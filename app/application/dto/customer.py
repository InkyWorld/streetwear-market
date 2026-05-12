"""Customer DTO schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreateDTO(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    loyalty_tier: str = Field(default="bronze", pattern="^(bronze|silver|gold)$")


class CustomerUpdateDTO(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: Optional[str] = Field(None, max_length=20)
    loyalty_tier: str | None = Field(default=None, pattern="^(bronze|silver|gold)$")


class CustomerReadDTO(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    loyalty_tier: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerListItemDTO(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    loyalty_tier: str

    model_config = ConfigDict(from_attributes=True)
