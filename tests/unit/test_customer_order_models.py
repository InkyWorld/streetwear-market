"""Unit tests for Customer and Order models."""

import pytest
from datetime import datetime

from app.models import Customer, Order, OrderItem


def test_customer_model_creation():
    """Test Customer model instantiation."""
    customer = Customer(
        full_name="Test Customer",
        email="test@example.com",
        phone="+1234567890"
    )
    assert customer.full_name == "Test Customer"
    assert customer.email == "test@example.com"
    assert customer.phone == "+1234567890"


def test_order_model_creation():
    """Test Order model instantiation."""
    order = Order(
        customer_id=1,
        status="pending",
        total_amount=100.0
    )
    assert order.customer_id == 1
    assert order.status == "pending"
    assert order.total_amount == 100.0


def test_order_item_model_creation():
    """Test OrderItem model instantiation."""
    order_item = OrderItem(
        order_id=1,
        product_id=1,
        quantity=2,
        unit_price=50.0
    )
    assert order_item.order_id == 1
    assert order_item.product_id == 1
    assert order_item.quantity == 2
    assert order_item.unit_price == 50.0
