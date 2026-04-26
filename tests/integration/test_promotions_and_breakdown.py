"""Integration tests for promotions and transparent pricing breakdown."""

from datetime import datetime, timedelta, timezone

import pytest

from app.schemas import (
    BrandCreateDTO,
    CatalogCreateDTO,
    CustomerCreateDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    ProductCreateDTO,
    PromotionCreateDTO,
)
from app.services import (
    BrandService,
    CatalogService,
    CustomerService,
    OrderService,
    ProductService,
    PromotionService,
)


@pytest.mark.asyncio
async def test_time_and_category_promotion_in_breakdown(test_db):
    brand_service = BrandService(test_db)
    catalog_service = CatalogService(test_db)
    product_service = ProductService(test_db)
    customer_service = CustomerService(test_db)
    order_service = OrderService(test_db)
    promo_service = PromotionService(test_db)

    brand = await brand_service.create_brand(BrandCreateDTO(name="Promo Brand", description="Promo"))
    sneakers = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Sneakers Promo", description="Promo cat")
    )
    product = await product_service.create_product(
        ProductCreateDTO(
            sku="PROMO-001",
            name="Promo Sneaker",
            price=100.0,
            category_id=sneakers.id,
            brand_id=brand.id,
            stock_quantity=10,
        )
    )
    customer = await customer_service.create_customer(
        CustomerCreateDTO(full_name="Promo User", email="promo-user@example.com", loyalty_tier="silver")
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    await promo_service.create_promotion(
        PromotionCreateDTO(
            name="Time Promo",
            promotion_type="time",
            discount_percentage=0.1,
            active_from=now - timedelta(hours=1),
            active_to=now + timedelta(hours=1),
        )
    )
    await promo_service.create_promotion(
        PromotionCreateDTO(
            name="Category Promo",
            promotion_type="category",
            discount_percentage=0.1,
            category_id=sneakers.id,
        )
    )

    order = await order_service.create_order(
        OrderCreateDTO(customer_id=customer.id, items=[OrderItemCreateDTO(product_id=product.id, quantity=5)])
    )

    assert order.pricing_breakdown is not None
    assert order.pricing_breakdown["subtotal"] == 500.0
    applied_rule_names = [x["rule"] for x in order.pricing_breakdown["applied_rules"]]
    assert "loyalty_tier_discount" in applied_rule_names
    assert "bulk_quantity_discount" in applied_rule_names
    assert "time_promotion_discount" in applied_rule_names
    assert "category_promotion_discount" in applied_rule_names
