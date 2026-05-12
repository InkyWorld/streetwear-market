"""Inventory schemas."""

from pydantic import BaseModel, Field


class InventoryReleaseOrderDTO(BaseModel):
    order_id: int = Field(..., gt=0)


class InventoryReleaseResultDTO(BaseModel):
    released_count: int
