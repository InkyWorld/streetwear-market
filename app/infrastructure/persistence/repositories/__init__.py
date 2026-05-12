"""Repositories exposed via infrastructure.persistence namespace."""

from app.infrastructure.persistence.repositories.base import BaseRepository
from app.infrastructure.persistence.repositories.brand import BrandRepository
from app.infrastructure.persistence.repositories.catalog import CatalogRepository
from app.infrastructure.persistence.repositories.customer import CustomerRepository
from app.infrastructure.persistence.repositories.inventory import InventoryReservationRepository
from app.infrastructure.persistence.repositories.order import OrderItemRepository, OrderRepository
from app.infrastructure.persistence.repositories.product import ProductRepository
from app.infrastructure.persistence.repositories.promotion import PromotionRepository

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
