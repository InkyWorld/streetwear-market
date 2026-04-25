"""Brand DTO schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BrandCreateDTO(BaseModel):
    """Schema for creating a brand."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class BrandReadDTO(BaseModel):
    """Schema for reading a brand."""

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
