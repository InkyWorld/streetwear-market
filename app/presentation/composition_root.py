"""Composition root for wiring application services and use cases."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.orders.create_order import CreateOrderCommandHandler
from app.application.orders.event_handlers import OrderCreatedEventHandler
from app.application.services.brand import BrandService
from app.application.services.catalog import CatalogService
from app.application.services.customer import CustomerService
from app.application.services.inventory import InventoryService
from app.application.services.order import OrderService
from app.application.services.product import ProductService
from app.application.services.promotion import PromotionService
from app.domain.events import OrderCreatedEvent
from app.infrastructure.domain_event_dispatcher import InMemoryDomainEventDispatcher
from app.infrastructure.persistence.repositories import (
    BrandRepository,
    CatalogRepository,
    CustomerRepository,
    InventoryReservationRepository,
    OrderItemRepository,
    OrderRepository,
    ProductRepository,
    PromotionRepository,
)


class CompositionRoot:
    """Build application services and handlers with concrete infrastructure adapters."""

    @staticmethod
    def brand_service(session: AsyncSession) -> BrandService:
        return BrandService(session=session, brand_repo=BrandRepository(session))

    @staticmethod
    def catalog_service(session: AsyncSession) -> CatalogService:
        return CatalogService(session=session, catalog_repo=CatalogRepository(session))

    @staticmethod
    def customer_service(session: AsyncSession) -> CustomerService:
        return CustomerService(session=session, customer_repo=CustomerRepository(session))

    @staticmethod
    def product_service(session: AsyncSession) -> ProductService:
        return ProductService(
            session=session,
            product_repo=ProductRepository(session),
            brand_repo=BrandRepository(session),
            catalog_repo=CatalogRepository(session),
        )

    @staticmethod
    def promotion_service(session: AsyncSession) -> PromotionService:
        return PromotionService(session=session, repo=PromotionRepository(session))

    @staticmethod
    def inventory_service(session: AsyncSession) -> InventoryService:
        return InventoryService(
            session=session,
            reservation_repo=InventoryReservationRepository(session),
            product_repo=ProductRepository(session),
        )

    @staticmethod
    def order_command_handler(session: AsyncSession) -> CreateOrderCommandHandler:
        dispatcher = InMemoryDomainEventDispatcher()
        dispatcher.register(
            OrderCreatedEvent,
            OrderCreatedEventHandler(CompositionRoot.inventory_service(session)),
        )
        return CreateOrderCommandHandler(
            session=session,
            dispatcher=dispatcher,
            order_repo=OrderRepository(session),
            customer_repo=CustomerRepository(session),
            product_repo=ProductRepository(session),
            promotion_repo=PromotionRepository(session),
        )

    @staticmethod
    def order_service(session: AsyncSession) -> OrderService:
        return OrderService(
            session=session,
            order_repo=OrderRepository(session),
            order_item_repo=OrderItemRepository(session),
            customer_repo=CustomerRepository(session),
            product_repo=ProductRepository(session),
            inventory_service=CompositionRoot.inventory_service(session),
            create_order_handler_factory=CompositionRoot.order_command_handler,
        )
