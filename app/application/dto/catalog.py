"""Catalog DTO schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CatalogCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)


class CatalogUpdateDTO(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CatalogReadDTO(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CatalogListDTO(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
