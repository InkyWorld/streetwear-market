"""Promotion schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PromotionCreateDTO(BaseModel):
    """Promotion create schema."""

    name: str = Field(..., min_length=1, max_length=120)
    promotion_type: str = Field(..., pattern="^(time|category)$")
    discount_percentage: float = Field(..., gt=0, le=1)
    category_id: int | None = None
    active_from: datetime | None = None
    active_to: datetime | None = None
    is_active: bool = True

    @model_validator(mode="after")
    def validate_category_requirement(self):
        if self.promotion_type == "category" and self.category_id is None:
            raise ValueError("category_id is required for category promotions")
        return self


class PromotionUpdateDTO(BaseModel):
    """Schema for updating a promotion."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    promotion_type: str | None = Field(default=None, pattern="^(time|category)$")
    discount_percentage: float | None = Field(default=None, gt=0, le=1)
    category_id: int | None = None
    active_from: datetime | None = None
    active_to: datetime | None = None
    is_active: bool | None = None


class PromotionReadDTO(BaseModel):
    """Promotion read schema."""

    id: int
    name: str
    promotion_type: str
    discount_percentage: float
    category_id: int | None
    active_from: datetime | None
    active_to: datetime | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
