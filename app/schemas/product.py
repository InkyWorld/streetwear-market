"""Product DTO schemas."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SeasonEnum(str, Enum):
    """Season enumeration."""

    SPRING_SUMMER = "SS"
    AUTUMN_WINTER = "AW"


class ProductCreateDTO(BaseModel):
    """Schema for creating a product."""

    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    price: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    size: Optional[str] = Field(default=None, max_length=20)
    color: Optional[str] = Field(default=None, max_length=50)
    season: SeasonEnum = Field(default=SeasonEnum.SPRING_SUMMER)
    in_stock: bool = Field(default=True)
    category_id: int = Field(...)
    brand_id: int = Field(...)

    @field_validator("sku")
    @classmethod
    def sku_must_be_alphanumeric(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("SKU must be alphanumeric with optional hyphens or underscores")
        return v.upper()


class ProductUpdateDTO(BaseModel):
    """Schema for updating a product."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    size: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=50)
    season: Optional[SeasonEnum] = None
    in_stock: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None


class ProductReadDTO(BaseModel):
    """Schema for reading a product."""

    id: int
    sku: str
    name: str
    description: str
    price: float
    currency: str
    size: Optional[str]
    color: Optional[str]
    season: SeasonEnum
    in_stock: bool
    category_id: int
    brand_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListItemDTO(BaseModel):
    """Schema for listing products."""

    id: int
    sku: str
    name: str
    price: float
    currency: str
    size: Optional[str]
    color: Optional[str]
    season: SeasonEnum
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)
