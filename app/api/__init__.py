"""API module."""

from app.api import brand_router, catalog_router, customer_router, order_router, product_router

__all__ = ["product_router", "catalog_router", "brand_router", "customer_router", "order_router"]
