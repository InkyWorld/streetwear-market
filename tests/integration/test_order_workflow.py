"""Integration tests for order workflow, inventory, and loyalty tier."""

import pytest

from app.domain.exceptions import NotFoundError, ValidationError
from app.schemas import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    ProductCreateDTO,
)


@pytest.mark.asyncio
async def test_order_creation_decreases_stock(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that order creation decreases product stock."""
    # Create test data
    brand = await brand_service.create_brand(BrandCreateDTO(name="Test Brand", description="Test"))
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-001",
            name="Test Product",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer", email="test@example.com", loyalty_tier="bronze"
        )
    )

    initial_stock = product.stock_quantity

    # Create order
    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=2)],
    )
    created_order = await order_service.create_order(order_data)

    # Verify order created
    assert created_order.id is not None
    assert created_order.status == "pending"
    assert created_order.total_amount == 200.0  # 2 * 100

    # Verify stock decreased
    updated_product = await product_service.get_product(product.id)
    assert updated_product.stock_quantity == initial_stock - 2


@pytest.mark.asyncio
async def test_order_creation_insufficient_stock_fails(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that order creation fails with insufficient stock."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 2", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 2", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-002",
            name="Test Product 2",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=2,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 2", email="test2@example.com", loyalty_tier="bronze"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=5)],
    )

    with pytest.raises(ValidationError) as exc_info:
        await order_service.create_order(order_data)

    assert "Insufficient stock" in str(exc_info.value)


@pytest.mark.asyncio
async def test_loyalty_tier_silver_applies_discount(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that silver tier applies 5% discount."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 3", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 3", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-003",
            name="Test Product 3",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 3", email="test3@example.com", loyalty_tier="silver"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=1)],
    )

    created_order = await order_service.create_order(order_data)

    # Price is 100, silver gets 5% discount = 5, total = 95
    assert created_order.total_amount == 95.0


@pytest.mark.asyncio
async def test_loyalty_tier_gold_applies_discount(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that gold tier applies 10% discount."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 4", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 4", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-004",
            name="Test Product 4",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 4", email="test4@example.com", loyalty_tier="gold"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=1)],
    )

    created_order = await order_service.create_order(order_data)

    # Price is 100, gold gets 10% discount = 10, total = 90
    assert created_order.total_amount == 90.0


@pytest.mark.asyncio
async def test_order_status_change_valid_transition(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test valid order status transition."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 5", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 5", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-005",
            name="Test Product 5",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 5", email="test5@example.com", loyalty_tier="bronze"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=1)],
    )

    created_order = await order_service.create_order(order_data)

    # Change status from pending to confirmed
    updated_order = await order_service.change_order_status(created_order.id, "confirmed")
    assert updated_order.status == "confirmed"

    # Change status from confirmed to shipped
    updated_order = await order_service.change_order_status(created_order.id, "shipped")
    assert updated_order.status == "shipped"

    # Change status from shipped to delivered
    updated_order = await order_service.change_order_status(created_order.id, "delivered")
    assert updated_order.status == "delivered"


@pytest.mark.asyncio
async def test_order_status_change_invalid_transition(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that invalid status transition raises error."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 6", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 6", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-006",
            name="Test Product 6",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 6", email="test6@example.com", loyalty_tier="bronze"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=1)],
    )

    created_order = await order_service.create_order(order_data)

    # Try invalid transition: pending -> shipped (skipping confirmed)
    with pytest.raises(ValidationError) as exc_info:
        await order_service.change_order_status(created_order.id, "shipped")

    assert "Cannot transition" in str(exc_info.value)


@pytest.mark.asyncio
async def test_order_status_change_to_cancelled_releases_inventory(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that cancelling releases reserved inventory."""
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 7", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 7", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-007",
            name="Test Product 7",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 7", email="test7@example.com", loyalty_tier="bronze"
        )
    )
    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=product.id, quantity=1)],
    )
    created_order = await order_service.create_order(order_data)

    updated = await order_service.change_order_status(created_order.id, "cancelled")
    assert updated.status == "cancelled"

    refreshed = await product_service.get_product(product.id)
    assert refreshed.stock_quantity == 10


@pytest.mark.asyncio
async def test_order_rollback_on_failure(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test that order creation rolls back on failure."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 8", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 8", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-008",
            name="Test Product 8",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 8", email="test8@example.com", loyalty_tier="bronze"
        )
    )

    initial_stock = product.stock_quantity

    # Try to create order with non-existent product
    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[OrderItemCreateDTO(product_id=99999, quantity=1)],
    )

    with pytest.raises(NotFoundError):
        await order_service.create_order(order_data)

    # Verify stock was not changed (rollback worked)
    updated_product = await product_service.get_product(product.id)
    assert updated_product.stock_quantity == initial_stock


@pytest.mark.asyncio
async def test_order_multiple_items_with_loyalty(
    product_service, brand_service, catalog_service, customer_service, order_service
):
    """Test order with multiple items and loyalty discount."""
    # Create test data
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="Test Brand 9", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Test Catalog 9", description="Test")
    )
    product1 = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-009A",
            name="Test Product 9A",
            description="Test",
            price=100.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    product2 = await product_service.create_product(
        ProductCreateDTO(
            sku="TEST-009B",
            name="Test Product 9B",
            description="Test",
            price=200.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Test Customer 9", email="test9@example.com", loyalty_tier="gold"
        )
    )

    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[
            OrderItemCreateDTO(product_id=product1.id, quantity=1),
            OrderItemCreateDTO(product_id=product2.id, quantity=1),
        ],
    )

    created_order = await order_service.create_order(order_data)

    # Subtotal: 100 + 200 = 300
    # Gold discount 10% = 30
    # Total: 270
    assert created_order.total_amount == 270.0
