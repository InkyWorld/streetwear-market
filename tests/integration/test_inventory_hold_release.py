"""Integration tests for inventory hold/release lifecycle."""

import pytest

from app.application.dto import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    ProductCreateDTO,
)
from app.presentation.composition_root import CompositionRoot


@pytest.mark.asyncio
async def test_manual_release_endpoint_flow(test_db):
    brand_service = CompositionRoot.brand_service(test_db)
    catalog_service = CompositionRoot.catalog_service(test_db)
    product_service = CompositionRoot.product_service(test_db)
    customer_service = CompositionRoot.customer_service(test_db)
    order_service = CompositionRoot.order_service(test_db)
    inventory_service = CompositionRoot.inventory_service(test_db)

    brand = await brand_service.create_brand(BrandCreateDTO(name="Inv Brand", description="Inv"))
    category = await catalog_service.create_catalog(CatalogCreateDTO(name="Inv Cat", description="Inv"))
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="INV-REL-001",
            name="Inv Product",
            price=80.0,
            category_id=category.id,
            brand_id=brand.id,
            stock_quantity=5,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(
            full_name="Inv User",
            email="inv-user@example.com",
            phone="+10000000001",
        )
    )

    order = await order_service.create_order(
        OrderCreateDTO(customer_id=customer.id, items=[OrderItemCreateDTO(product_id=product.id, quantity=2)])
    )
    reduced = await product_service.get_product(product.id)
    assert reduced.stock_quantity == 3

    released = await inventory_service.release_holds_for_order(order.id, reason="manual_release")
    await test_db.commit()
    assert released >= 1

    replenished = await product_service.get_product(product.id)
    assert replenished.stock_quantity == 5
