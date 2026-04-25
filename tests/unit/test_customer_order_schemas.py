"""Unit tests for Customer and Order DTO schemas."""

import pytest
from pydantic import ValidationError

from app.schemas import (
    CustomerCreateDTO,
    CustomerReadDTO,
    OrderCreateDTO,
    OrderItemCreateDTO,
    OrderReadDTO,
)


def test_customer_create_dto_valid():
    """Test valid CustomerCreateDTO."""
    dto = CustomerCreateDTO(
        full_name="John Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    assert dto.full_name == "John Doe"
    assert dto.email == "john@example.com"
    assert dto.phone == "+1234567890"


def test_customer_create_dto_invalid_email():
    """Test CustomerCreateDTO with invalid email."""
    with pytest.raises(ValidationError):
        CustomerCreateDTO(
            full_name="John Doe",
            email="invalid-email"  # Invalid email format
        )


def test_customer_create_dto_optional_phone():
    """Test CustomerCreateDTO with optional phone."""
    dto = CustomerCreateDTO(
        full_name="Jane Doe",
        email="jane@example.com"
        # phone not provided
    )
    assert dto.phone is None


def test_order_item_create_dto_valid():
    """Test valid OrderItemCreateDTO."""
    dto = OrderItemCreateDTO(
        product_id=1,
        quantity=2
    )
    assert dto.product_id == 1
    assert dto.quantity == 2


def test_order_item_create_dto_invalid_quantity():
    """Test OrderItemCreateDTO with invalid quantity."""
    with pytest.raises(ValidationError):
        OrderItemCreateDTO(
            product_id=1,
            quantity=0  # Must be > 0
        )


def test_order_create_dto_valid():
    """Test valid OrderCreateDTO."""
    dto = OrderCreateDTO(
        customer_id=1,
        items=[
            OrderItemCreateDTO(product_id=1, quantity=2),
            OrderItemCreateDTO(product_id=2, quantity=1)
        ]
    )
    assert dto.customer_id == 1
    assert len(dto.items) == 2


def test_order_create_dto_empty_items():
    """Test OrderCreateDTO with empty items."""
    with pytest.raises(ValidationError):
        OrderCreateDTO(
            customer_id=1,
            items=[]  # Must have at least one item
        )


def test_order_read_dto_from_attributes():
    """Test OrderReadDTO model_validate from attributes."""
    data = {
        "id": 1,
        "customer_id": 1,
        "status": "pending",
        "total_amount": 100.0,
        "items": [],
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    from datetime import datetime
    data["created_at"] = datetime(2024, 1, 1)
    data["updated_at"] = datetime(2024, 1, 1)

    dto = OrderReadDTO.model_validate(data)
    assert dto.id == 1
    assert dto.customer_id == 1
    assert dto.status == "pending"
