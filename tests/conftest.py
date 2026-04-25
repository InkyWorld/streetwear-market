"""Pytest configuration and fixtures."""

import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base
from app.repositories import (
    BrandRepository,
    CatalogRepository,
    CustomerRepository,
    OrderItemRepository,
    OrderRepository,
    ProductRepository,
)
from app.services import BrandService, CatalogService, CustomerService, OrderService, ProductService

# Use test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def product_service(test_db):
    """Create product service with test database."""
    return ProductService(test_db)


@pytest.fixture
async def brand_service(test_db):
    """Create brand service with test database."""
    return BrandService(test_db)


@pytest.fixture
async def catalog_service(test_db):
    """Create catalog service with test database."""
    return CatalogService(test_db)


@pytest.fixture
async def customer_service(test_db):
    """Create customer service with test database."""
    return CustomerService(test_db)


@pytest.fixture
async def order_service(test_db):
    """Create order service with test database."""
    return OrderService(test_db)


@pytest.fixture
async def product_repository(test_db):
    """Create product repository with test database."""
    return ProductRepository(test_db)


@pytest.fixture
async def brand_repository(test_db):
    """Create brand repository with test database."""
    return BrandRepository(test_db)


@pytest.fixture
async def catalog_repository(test_db):
    """Create catalog repository with test database."""
    return CatalogRepository(test_db)


@pytest.fixture
async def customer_repository(test_db):
    """Create customer repository with test database."""
    return CustomerRepository(test_db)


@pytest.fixture
async def order_repository(test_db):
    """Create order repository with test database."""
    return OrderRepository(test_db)


@pytest.fixture
async def order_item_repository(test_db):
    """Create order item repository with test database."""
    return OrderItemRepository(test_db)


@pytest.fixture
async def sample_brand(brand_service):
    """Create sample brand."""
    from app.schemas import BrandCreateDTO

    return await brand_service.create_brand(BrandCreateDTO(name="Nike", description="Sportswear"))


@pytest.fixture
async def sample_catalog(catalog_service):
    """Create sample catalog."""
    from app.schemas import CatalogCreateDTO

    return await catalog_service.create_catalog(
        CatalogCreateDTO(name="Sneakers", description="Athletic footwear")
    )


@pytest.fixture
async def sample_product(product_service, sample_brand, sample_catalog):
    """Create sample product."""
    from app.schemas import ProductCreateDTO

    return await product_service.create_product(
        ProductCreateDTO(
            sku="NIKE-AIR-001",
            name="Nike Air Max 90",
            description="Classic sneaker",
            price=150.0,
            currency="USD",
            size="10",
            color="White",
            season="SS",
            in_stock=True,
            category_id=sample_catalog.id,
            brand_id=sample_brand.id,
        )
    )


@pytest.fixture
async def sample_customer(customer_service):
    """Create sample customer."""
    from app.schemas import CustomerCreateDTO

    return await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="John Doe",
            email="john@example.com",
            phone="+1234567890",
        )
    )


@pytest.fixture
async def sample_order(order_service, sample_customer, sample_product):
    """Create sample order."""
    from app.schemas import OrderCreateDTO, OrderItemCreateDTO

    return await order_service.create_order(
        OrderCreateDTO(
            customer_id=sample_customer.id,
            items=[
                OrderItemCreateDTO(
                    product_id=sample_product.id,
                    quantity=2,
                )
            ],
        )
    )
