"""Unit tests for tactical DDD order domain model."""

import pytest

from app.domain.enums import OrderStatus
from app.domain.events import OrderCreatedEvent
from app.domain.exceptions import ValidationError
from app.domain.ordering import Order, OrderLine
from app.domain.value_objects import Money, Quantity, Sku


class TestValueObjects:
    def test_money_is_normalized_and_immutable(self):
        money = Money.create(100, "usd")

        assert money.amount == 100.0
        assert money.currency == "USD"

    def test_money_rejects_negative_amount(self):
        with pytest.raises(ValidationError):
            Money.create(-1, "USD")

    def test_quantity_rejects_zero(self):
        with pytest.raises(ValidationError):
            Quantity.create(0)

    def test_sku_is_normalized(self):
        sku = Sku.create("nike-air-001")
        assert sku.value == "NIKE-AIR-001"


class TestOrderAggregate:
    def test_order_requires_at_least_one_line(self):
        with pytest.raises(ValidationError):
            Order.create(
                customer_id=1,
                lines=[],
                total_price=Money.create(100, "USD"),
            )

    def test_order_raises_created_event(self):
        order = Order.create(
            customer_id=1,
            lines=[
                OrderLine.create(
                    product_id=10,
                    sku="NIKE-AIR-001",
                    quantity=2,
                    unit_price=50,
                    currency="USD",
                )
            ],
            total_price=Money.create(100, "USD"),
            pricing_breakdown={"subtotal": 100.0, "final_total": 100.0},
        )

        events = order.domain_events

        assert len(events) == 1
        assert isinstance(events[0], OrderCreatedEvent)
        assert events[0].customer_id == 1
        assert events[0].item_count == 2

    def test_order_validates_pricing_breakdown_against_lines(self):
        with pytest.raises(ValidationError):
            Order.create(
                customer_id=1,
                lines=[
                    OrderLine.create(
                        product_id=10,
                        sku="NIKE-AIR-001",
                        quantity=2,
                        unit_price=50,
                        currency="USD",
                    )
                ],
                total_price=Money.create(100, "USD"),
                pricing_breakdown={"subtotal": 90.0, "final_total": 100.0},
            )

    def test_order_status_changes_use_domain_methods(self):
        order = Order.create(
            customer_id=1,
            lines=[
                OrderLine.create(
                    product_id=10,
                    sku="NIKE-AIR-001",
                    quantity=1,
                    unit_price=100,
                    currency="USD",
                )
            ],
            total_price=Money.create(100, "USD"),
            pricing_breakdown={"subtotal": 100.0, "final_total": 100.0},
        )

        order.confirm()
        order.mark_shipped()
        order.mark_delivered()

        assert order.status == OrderStatus.DELIVERED.value

    def test_order_rejects_invalid_status_transition(self):
        order = Order.create(
            customer_id=1,
            lines=[
                OrderLine.create(
                    product_id=10,
                    sku="NIKE-AIR-001",
                    quantity=1,
                    unit_price=100,
                    currency="USD",
                )
            ],
            total_price=Money.create(100, "USD"),
            pricing_breakdown={"subtotal": 100.0, "final_total": 100.0},
        )

        with pytest.raises(ValidationError):
            order.mark_shipped()
