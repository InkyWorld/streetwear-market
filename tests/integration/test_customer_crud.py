"""Integration tests for Customer CRUD operations."""

import pytest

from app.domain.exceptions import ConflictError, NotFoundError, ValidationError
from app.schemas import CustomerCreateDTO


@pytest.mark.asyncio
async def test_create_customer_success(customer_service):
    """Test successful customer creation."""
    customer_data = CustomerCreateDTO(
        full_name="Alice Johnson",
        email="alice@example.com",
        phone="+9876543210",
    )

    customer = await customer_service.create_customer(customer_data)

    assert customer.id is not None
    assert customer.full_name == "Alice Johnson"
    assert customer.email == "alice@example.com"
    assert customer.phone == "+9876543210"


@pytest.mark.asyncio
async def test_create_customer_duplicate_email(customer_service):
    """Test creating customer with duplicate email."""
    customer_data1 = CustomerCreateDTO(
        full_name="Bob Smith",
        email="bob@example.com",
    )
    customer_data2 = CustomerCreateDTO(
        full_name="Bob Smith Jr",
        email="bob@example.com",  # Same email
    )

    await customer_service.create_customer(customer_data1)

    with pytest.raises(ConflictError) as exc_info:
        await customer_service.create_customer(customer_data2)

    assert "already exists" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_customer_empty_name(customer_service):
    """Test creating customer with empty name."""
    customer_data = CustomerCreateDTO(
        full_name="   ",  # Empty after strip
        email="empty@example.com",
    )

    with pytest.raises(ValidationError) as exc_info:
        await customer_service.create_customer(customer_data)

    assert "Full name cannot be empty" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_customer_success(customer_service, sample_customer):
    """Test getting customer by id."""
    customer = await customer_service.get_customer(sample_customer.id)

    assert customer.id == sample_customer.id
    assert customer.full_name == sample_customer.full_name
    assert customer.email == sample_customer.email


@pytest.mark.asyncio
async def test_get_customer_not_found(customer_service):
    """Test getting non-existent customer."""
    with pytest.raises(NotFoundError) as exc_info:
        await customer_service.get_customer(9999)

    assert "not found" in exc_info.value.message


@pytest.mark.asyncio
async def test_list_customers(customer_service, sample_customer):
    """Test listing customers."""
    customers = await customer_service.list_customers()

    assert len(customers) >= 1
    assert any(c.id == sample_customer.id for c in customers)


@pytest.mark.asyncio
async def test_list_customers_pagination(customer_service):
    """Test listing customers with pagination."""
    # Create multiple customers
    for i in range(5):
        customer_data = CustomerCreateDTO(
            full_name=f"Customer {i}",
            email=f"customer{i}@example.com",
        )
        await customer_service.create_customer(customer_data)

    # Test pagination
    customers_page1 = await customer_service.list_customers(skip=0, limit=2)
    assert len(customers_page1) == 2

    customers_page2 = await customer_service.list_customers(skip=2, limit=2)
    assert len(customers_page2) == 2


@pytest.mark.asyncio
async def test_customer_email_case_insensitive(customer_service):
    """Test that email is stored in lowercase."""
    customer_data = CustomerCreateDTO(
        full_name="Email Case Test",
        email="TestEmail@EXAMPLE.COM",
    )

    customer = await customer_service.create_customer(customer_data)

    assert customer.email == "testemail@example.com"
