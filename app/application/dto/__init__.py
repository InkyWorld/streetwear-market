"""Application DTO contracts."""

from app.application.dto.brand import BrandCreateDTO, BrandReadDTO, BrandUpdateDTO
from app.application.dto.catalog import CatalogCreateDTO, CatalogListDTO, CatalogReadDTO, CatalogUpdateDTO
from app.application.dto.customer import (
    CustomerCreateDTO,
    CustomerListItemDTO,
    CustomerReadDTO,
    CustomerUpdateDTO,
)
from app.application.dto.inventory import InventoryReleaseOrderDTO, InventoryReleaseResultDTO
from app.application.dto.order import (
    OrderCreateDTO,
    OrderItemCreateDTO,
    OrderItemReadDTO,
    OrderListItemDTO,
    OrderReadDTO,
)
from app.application.dto.product import (
    ProductCreateDTO,
    ProductListItemDTO,
    ProductReadDTO,
    ProductUpdateDTO,
    SeasonEnum,
)
from app.application.dto.promotion import PromotionCreateDTO, PromotionReadDTO, PromotionUpdateDTO

__all__ = [
    "BrandCreateDTO",
    "BrandReadDTO",
    "BrandUpdateDTO",
    "CatalogCreateDTO",
    "CatalogReadDTO",
    "CatalogListDTO",
    "CatalogUpdateDTO",
    "CustomerCreateDTO",
    "CustomerReadDTO",
    "CustomerUpdateDTO",
    "CustomerListItemDTO",
    "InventoryReleaseOrderDTO",
    "InventoryReleaseResultDTO",
    "OrderCreateDTO",
    "OrderReadDTO",
    "OrderListItemDTO",
    "OrderItemCreateDTO",
    "OrderItemReadDTO",
    "ProductCreateDTO",
    "ProductUpdateDTO",
    "ProductReadDTO",
    "ProductListItemDTO",
    "PromotionCreateDTO",
    "PromotionReadDTO",
    "PromotionUpdateDTO",
    "SeasonEnum",
]
