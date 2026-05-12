"""Integration tests for API-level domain event flow."""

import pytest

from app.application.dto import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    ProductCreateDTO,
)


@pytest.mark.asyncio
async def test_create_order_api_dispatches_order_created_event_and_runs_handler(
    api_client,
    brand_service,
    catalog_service,
    customer_service,
    product_service,
):
    """POST /api/order triggers OrderCreatedEvent and applies inventory hold side effect."""
    brand = await brand_service.create_brand(
        BrandCreateDTO(name="API Event Brand", description="Test")
    )
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="API Event Catalog", description="Test")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="API-EVENT-001",
            name="API Event Product",
            description="Test",
            price=120.0,
            currency="USD",
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
            in_stock=True,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="API Event Customer",
            email="api.event.customer@example.com",
            loyalty_tier="bronze",
        )
    )

    response = await api_client.post(
        "/api/order",
        json={
            "customer_id": customer.id,
            "items": [{"product_id": product.id, "quantity": 2}],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["customer_id"] == customer.id
    assert payload["status"] == "pending"
    assert payload["total_amount"] == 240.0

    refreshed_product = await product_service.get_product(product.id)
    assert refreshed_product.stock_quantity == 8
