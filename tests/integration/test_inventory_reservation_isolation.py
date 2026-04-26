"""Integration tests for reservation isolation between orders."""

import pytest

from app.schemas import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    ProductCreateDTO,
)
from app.services import BrandService, CatalogService, CustomerService, OrderService, ProductService


@pytest.mark.asyncio
async def test_cancelling_one_order_does_not_release_other_order_hold(test_db):
    brand_service = BrandService(test_db)
    catalog_service = CatalogService(test_db)
    product_service = ProductService(test_db)
    customer_service = CustomerService(test_db)
    order_service = OrderService(test_db)

    brand = await brand_service.create_brand(BrandCreateDTO(name="Iso Brand", description="Isolation"))
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Iso Catalog", description="Isolation")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="ISO-RES-001",
            name="Isolation Product",
            price=100.0,
            category_id=catalog.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer_a = await customer_service.create_customer(
        CustomerCreateDTO(full_name="Customer A", email="customer-a@example.com")
    )
    customer_b = await customer_service.create_customer(
        CustomerCreateDTO(full_name="Customer B", email="customer-b@example.com")
    )

    order_a = await order_service.create_order(
        OrderCreateDTO(customer_id=customer_a.id, items=[OrderItemCreateDTO(product_id=product.id, quantity=2)])
    )
    order_b = await order_service.create_order(
        OrderCreateDTO(customer_id=customer_b.id, items=[OrderItemCreateDTO(product_id=product.id, quantity=3)])
    )

    reduced = await product_service.get_product(product.id)
    assert reduced.stock_quantity == 5

    await order_service.change_order_status(order_a.id, "cancelled")
    after_cancel_a = await product_service.get_product(product.id)
    assert after_cancel_a.stock_quantity == 7

    # Ensure the second order still holds its quantity and can release only its own hold.
    await order_service.change_order_status(order_b.id, "cancelled")
    after_cancel_b = await product_service.get_product(product.id)
    assert after_cancel_b.stock_quantity == 10
