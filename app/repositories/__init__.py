"""Repository layer for database access."""

from app.repositories.base import BaseRepository
from app.repositories.brand import BrandRepository
from app.repositories.catalog import CatalogRepository
from app.repositories.customer import CustomerRepository
from app.repositories.inventory import InventoryReservationRepository
from app.repositories.order import OrderItemRepository, OrderRepository
from app.repositories.promotion import PromotionRepository
from app.repositories.product import ProductRepository

__all__ = [
    "BaseRepository",
    "ProductRepository",
    "BrandRepository",
    "CatalogRepository",
    "CustomerRepository",
    "InventoryReservationRepository",
    "OrderRepository",
    "OrderItemRepository",
    "PromotionRepository",
]
