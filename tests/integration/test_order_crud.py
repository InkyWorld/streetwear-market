"""Integration tests for Order CRUD operations."""

import pytest
from pydantic import ValidationError as PydanticValidationError

from app.domain.exceptions import NotFoundError, ValidationError
from app.schemas import CustomerCreateDTO, OrderCreateDTO, OrderItemCreateDTO


@pytest.mark.asyncio
async def test_create_order_success(order_service, sample_customer, sample_product):
    """Test successful order creation."""
    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(
                product_id=sample_product.id,
                quantity=3,
            )
        ],
    )

    order = await order_service.create_order(order_data)

    assert order.id is not None
    assert order.customer_id == sample_customer.id
    assert order.status == "pending"
    assert len(order.items) == 1
    assert order.items[0].product_id == sample_product.id
    assert order.items[0].quantity == 3
    assert order.total_amount == sample_product.price * 3


@pytest.mark.asyncio
async def test_create_order_multiple_items(order_service, sample_customer, product_service, sample_brand, sample_catalog):
    """Test creating order with multiple items."""
    # Create another product
    from app.schemas import ProductCreateDTO

    product2_data = ProductCreateDTO(
        sku="ADIDAS-BOOST-001",
        name="Adidas Boost",
        price=120.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
        in_stock=True,
    )
    product2 = await product_service.create_product(product2_data)

    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(product_id=product2.id, quantity=2),
            OrderItemCreateDTO(product_id=product2.id, quantity=1),
        ],
    )

    order = await order_service.create_order(order_data)

    assert len(order.items) == 2
    expected_total = (product2.price * 2) + (product2.price * 1)
    assert order.total_amount == expected_total


@pytest.mark.asyncio
async def test_create_order_invalid_customer(order_service, sample_product):
    """Test creating order with non-existent customer."""
    order_data = OrderCreateDTO(
        customer_id=9999,  # Non-existent
        items=[
            OrderItemCreateDTO(
                product_id=sample_product.id,
                quantity=1,
            )
        ],
    )

    with pytest.raises(NotFoundError) as exc_info:
        await order_service.create_order(order_data)

    assert "Customer" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_order_invalid_product(order_service, sample_customer):
    """Test creating order with non-existent product."""
    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(
                product_id=9999,  # Non-existent
                quantity=1,
            )
        ],
    )

    with pytest.raises(NotFoundError) as exc_info:
        await order_service.create_order(order_data)

    assert "Product" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_order_product_out_of_stock(order_service, sample_customer, product_service, sample_brand, sample_catalog):
    """Test creating order with out-of-stock product."""
    from app.schemas import ProductCreateDTO, ProductUpdateDTO

    # Create out-of-stock product
    product_data = ProductCreateDTO(
        sku="OUT-OF-STOCK-001",
        name="Out of Stock Product",
        price=100.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
        in_stock=True,
    )
    product = await product_service.create_product(product_data)

    # Update to out of stock
    await product_service.update_product(product.id, ProductUpdateDTO(in_stock=False))

    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(
                product_id=product.id,
                quantity=1,
            )
        ],
    )

    with pytest.raises(ValidationError) as exc_info:
        await order_service.create_order(order_data)

    assert "not in stock" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_order_invalid_quantity(order_service, sample_customer):
    """Test creating order with invalid quantity."""
    with pytest.raises(PydanticValidationError):
        OrderCreateDTO(
            customer_id=sample_customer.id,
            items=[
                OrderItemCreateDTO(
                    product_id=1,
                    quantity=0,  # Invalid
                )
            ],
        )


@pytest.mark.asyncio
async def test_create_order_empty_items(order_service, sample_customer):
    """Test creating order with empty items list."""
    with pytest.raises(PydanticValidationError):
        OrderCreateDTO(
            customer_id=sample_customer.id,
            items=[],  # Empty items
        )


@pytest.mark.asyncio
async def test_get_order_success(order_service, sample_order):
    """Test getting order by id."""
    order = await order_service.get_order(sample_order.id)

    assert order.id == sample_order.id
    assert order.customer_id == sample_order.customer_id
    assert order.status == "pending"


@pytest.mark.asyncio
async def test_get_order_not_found(order_service):
    """Test getting non-existent order."""
    with pytest.raises(NotFoundError) as exc_info:
        await order_service.get_order(9999)

    assert "not found" in exc_info.value.message


@pytest.mark.asyncio
async def test_list_orders(order_service, sample_order):
    """Test listing orders."""
    orders = await order_service.list_orders()

    assert len(orders) >= 1
    assert any(o.id == sample_order.id for o in orders)


@pytest.mark.asyncio
async def test_list_customer_orders(order_service, sample_customer, sample_order):
    """Test listing orders for a specific customer."""
    orders = await order_service.list_customer_orders(sample_customer.id)

    assert len(orders) >= 1
    assert any(o.id == sample_order.id for o in orders)


@pytest.mark.asyncio
async def test_list_customer_orders_not_found(order_service):
    """Test listing orders for non-existent customer."""
    with pytest.raises(NotFoundError):
        await order_service.list_customer_orders(9999)


@pytest.mark.asyncio
async def test_order_total_calculation(order_service, sample_customer, sample_product):
    """Test that order total is calculated correctly."""
    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(
                product_id=sample_product.id,
                quantity=5,
            )
        ],
    )

    order = await order_service.create_order(order_data)

    expected_total = sample_product.price * 5 * 0.95
    assert order.total_amount == expected_total


@pytest.mark.asyncio
async def test_create_order_with_duplicate_product_items(
    order_service, sample_customer, sample_product
):
    """Duplicate product rows are stored as separate order items."""
    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[
            OrderItemCreateDTO(product_id=sample_product.id, quantity=1),
            OrderItemCreateDTO(product_id=sample_product.id, quantity=3),
        ],
    )

    order = await order_service.create_order(order_data)

    assert len(order.items) == 2
    assert order.items[0].product_id == sample_product.id
    assert order.items[1].product_id == sample_product.id
    assert order.total_amount == sample_product.price * 4


@pytest.mark.asyncio
async def test_order_item_uses_product_price_snapshot(
    order_service, product_service, sample_customer, sample_product
):
    """Order item unit_price keeps creation-time product price."""
    order_data = OrderCreateDTO(
        customer_id=sample_customer.id,
        items=[OrderItemCreateDTO(product_id=sample_product.id, quantity=2)],
    )
    order = await order_service.create_order(order_data)
    initial_unit_price = order.items[0].unit_price

    from app.schemas import ProductUpdateDTO

    await product_service.update_product(sample_product.id, ProductUpdateDTO(price=999.0))
    updated_order = await order_service.get_order(order.id)

    assert updated_order.items[0].unit_price == initial_unit_price
    assert updated_order.total_amount == initial_unit_price * 2


@pytest.mark.asyncio
async def test_business_flow_customer_order(customer_service, order_service, product_service, sample_brand, sample_catalog):
    """Test full business flow: create customer, product, and order."""
    # Create customer
    customer_data = CustomerCreateDTO(
        full_name="New Customer",
        email="newcustomer@example.com",
        phone="+1111111111",
    )
    customer = await customer_service.create_customer(customer_data)

    # Create product
    from app.schemas import ProductCreateDTO

    product_data = ProductCreateDTO(
        sku="BUSINESS-FLOW-001",
        name="Business Flow Product",
        price=200.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
        in_stock=True,
    )
    product = await product_service.create_product(product_data)

    # Create order
    order_data = OrderCreateDTO(
        customer_id=customer.id,
        items=[
            OrderItemCreateDTO(
                product_id=product.id,
                quantity=2,
            )
        ],
    )
    order = await order_service.create_order(order_data)

    # Verify
    assert order.customer_id == customer.id
    assert len(order.items) == 1
    assert order.items[0].product_id == product.id
    assert order.total_amount == product.price * 2
