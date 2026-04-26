"""Catalog DTO schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CatalogCreateDTO(BaseModel):
    """Schema for creating a catalog/category."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class CatalogUpdateDTO(BaseModel):
    """Schema for updating a catalog/category."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CatalogReadDTO(BaseModel):
    """Schema for reading a catalog."""

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CatalogListDTO(BaseModel):
    """Schema for listing catalogs."""

    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
