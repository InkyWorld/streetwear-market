"""Integration tests for inventory hold/release lifecycle."""

import pytest

from app.schemas import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    ProductCreateDTO,
)
from app.services import (
    BrandService,
    CatalogService,
    CustomerService,
    InventoryService,
    OrderService,
    ProductService,
)


@pytest.mark.asyncio
async def test_manual_release_endpoint_flow(test_db):
    brand_service = BrandService(test_db)
    catalog_service = CatalogService(test_db)
    product_service = ProductService(test_db)
    customer_service = CustomerService(test_db)
    order_service = OrderService(test_db)
    inventory_service = InventoryService(test_db)

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
        CustomerCreateDTO(full_name="Inv User", email="inv-user@example.com")
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
