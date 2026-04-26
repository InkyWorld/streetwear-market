"""Inventory schemas."""

from pydantic import BaseModel, Field


class InventoryReleaseOrderDTO(BaseModel):
    """Manual release request."""

    order_id: int = Field(..., gt=0)


class InventoryReleaseResultDTO(BaseModel):
    """Release result."""

    released_count: int
