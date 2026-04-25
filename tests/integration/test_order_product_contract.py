"""Contract-style integration tests for Order and Product interaction."""

import pytest

from app.domain.exceptions import NotFoundError, ValidationError
from app.schemas import OrderCreateDTO, OrderItemCreateDTO, ProductUpdateDTO


@pytest.mark.asyncio
async def test_order_creation_requires_existing_product(order_service, sample_customer):
    """OrderService must return NotFoundError for unknown product ids."""
    with pytest.raises(NotFoundError):
        await order_service.create_order(
            OrderCreateDTO(
                customer_id=sample_customer.id,
                items=[OrderItemCreateDTO(product_id=999_999, quantity=1)],
            )
        )


@pytest.mark.asyncio
async def test_order_creation_respects_product_stock_flag(
    order_service, product_service, sample_customer, sample_product
):
    """OrderService must reject products marked as out of stock."""
    await product_service.update_product(sample_product.id, ProductUpdateDTO(in_stock=False))

    with pytest.raises(ValidationError) as exc_info:
        await order_service.create_order(
            OrderCreateDTO(
                customer_id=sample_customer.id,
                items=[OrderItemCreateDTO(product_id=sample_product.id, quantity=1)],
            )
        )

    assert "not in stock" in exc_info.value.message
