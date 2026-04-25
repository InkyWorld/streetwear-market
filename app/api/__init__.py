"""API module."""

from app.api import (
    brand_router,
    catalog_router,
    customer_router,
    inventory_router,
    order_router,
    product_router,
    promotion_router,
)

__all__ = [
    "product_router",
    "catalog_router",
    "brand_router",
    "customer_router",
    "order_router",
    "promotion_router",
    "inventory_router",
]
