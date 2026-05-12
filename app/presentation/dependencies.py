"""FastAPI dependencies for application services and use-case handlers."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.orders.create_order import CreateOrderCommandHandler
from app.application.services.brand import BrandService
from app.application.services.catalog import CatalogService
from app.application.services.customer import CustomerService
from app.application.services.inventory import InventoryService
from app.application.services.order import OrderService
from app.application.services.product import ProductService
from app.application.services.promotion import PromotionService
from app.core.database import get_db_session
from app.presentation.composition_root import CompositionRoot


def get_brand_service(session: AsyncSession = Depends(get_db_session)) -> BrandService:
    return CompositionRoot.brand_service(session)


def get_catalog_service(session: AsyncSession = Depends(get_db_session)) -> CatalogService:
    return CompositionRoot.catalog_service(session)


def get_customer_service(session: AsyncSession = Depends(get_db_session)) -> CustomerService:
    return CompositionRoot.customer_service(session)


def get_product_service(session: AsyncSession = Depends(get_db_session)) -> ProductService:
    return CompositionRoot.product_service(session)


def get_promotion_service(session: AsyncSession = Depends(get_db_session)) -> PromotionService:
    return CompositionRoot.promotion_service(session)


def get_inventory_service(session: AsyncSession = Depends(get_db_session)) -> InventoryService:
    return CompositionRoot.inventory_service(session)


def get_order_service(session: AsyncSession = Depends(get_db_session)) -> OrderService:
    return CompositionRoot.order_service(session)


def get_order_command_handler(
    session: AsyncSession = Depends(get_db_session),
) -> CreateOrderCommandHandler:
    return CompositionRoot.order_command_handler(session)
