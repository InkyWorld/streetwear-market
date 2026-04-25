"""Integration tests for Product CRUD operations."""

import pytest

from app.domain.exceptions import ConflictError, NotFoundError
from app.schemas import ProductCreateDTO, ProductUpdateDTO, SeasonEnum


@pytest.mark.asyncio
async def test_create_product_success(product_service, sample_brand, sample_catalog):
    """Test successful product creation."""
    product_data = ProductCreateDTO(
        sku="TEST-PROD-001",
        name="Test Product",
        description="A test product",
        price=99.99,
        currency="USD",
        size="M",
        color="Blue",
        season=SeasonEnum.AUTUMN_WINTER,
        in_stock=True,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
    )

    product = await product_service.create_product(product_data)

    assert product.id is not None
    assert product.sku == "TEST-PROD-001"
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.in_stock is True


@pytest.mark.asyncio
async def test_create_product_duplicate_sku(
    product_service, sample_product, sample_brand, sample_catalog
):
    """Test creating product with duplicate SKU."""
    product_data = ProductCreateDTO(
        sku=sample_product.sku,  # Same SKU
        name="Another Product",
        price=100.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
    )

    with pytest.raises(ConflictError) as exc_info:
        await product_service.create_product(product_data)

    assert "already exists" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_product_invalid_price(product_service, sample_brand, sample_catalog):
    """Test creating product with invalid price."""
    from pydantic import ValidationError as PydanticValidationError

    with pytest.raises(PydanticValidationError):
        ProductCreateDTO(
            sku="TEST-INVALID-PRICE",
            name="Invalid Price Product",
            price=-10.0,  # Invalid negative price
            category_id=sample_catalog.id,
            brand_id=sample_brand.id,
        )


@pytest.mark.asyncio
async def test_create_product_nonexistent_category(product_service, sample_brand):
    """Test creating product with non-existent category."""
    product_data = ProductCreateDTO(
        sku="TEST-NO-CATEGORY",
        name="No Category Product",
        price=100.0,
        category_id=9999,  # Non-existent
        brand_id=sample_brand.id,
    )

    with pytest.raises(NotFoundError) as exc_info:
        await product_service.create_product(product_data)

    assert "Category" in exc_info.value.message


@pytest.mark.asyncio
async def test_create_product_nonexistent_brand(product_service, sample_catalog):
    """Test creating product with non-existent brand."""
    product_data = ProductCreateDTO(
        sku="TEST-NO-BRAND",
        name="No Brand Product",
        price=100.0,
        category_id=sample_catalog.id,
        brand_id=9999,  # Non-existent
    )

    with pytest.raises(NotFoundError) as exc_info:
        await product_service.create_product(product_data)

    assert "Brand" in exc_info.value.message


@pytest.mark.asyncio
async def test_get_product_success(product_service, sample_product):
    """Test getting product by id."""
    product = await product_service.get_product(sample_product.id)

    assert product.id == sample_product.id
    assert product.sku == sample_product.sku
    assert product.name == sample_product.name


@pytest.mark.asyncio
async def test_get_product_not_found(product_service):
    """Test getting non-existent product."""
    with pytest.raises(NotFoundError) as exc_info:
        await product_service.get_product(9999)

    assert "not found" in exc_info.value.message


@pytest.mark.asyncio
async def test_list_products(product_service, sample_product):
    """Test listing products."""
    products = await product_service.list_products()

    assert len(products) >= 1
    assert any(p.id == sample_product.id for p in products)


@pytest.mark.asyncio
async def test_update_product_success(product_service, sample_product):
    """Test successful product update."""
    update_data = ProductUpdateDTO.model_validate({"name": "Updated Product Name", "price": 199.99})

    updated_product = await product_service.update_product(sample_product.id, update_data)

    assert updated_product.name == "Updated Product Name"
    assert updated_product.price == 199.99
    assert updated_product.sku == sample_product.sku  # SKU unchanged


@pytest.mark.asyncio
async def test_update_product_not_found(product_service):
    """Test updating non-existent product."""
    update_data = ProductUpdateDTO.model_validate({"name": "Updated"})

    with pytest.raises(NotFoundError):
        await product_service.update_product(9999, update_data)


@pytest.mark.asyncio
async def test_update_product_invalid_price(product_service, sample_product):
    """Test updating product with invalid price."""
    from pydantic import ValidationError as PydanticValidationError

    with pytest.raises(PydanticValidationError):
        ProductUpdateDTO.model_validate({"price": -50.0})


@pytest.mark.asyncio
async def test_update_product_nonexistent_category(product_service, sample_product):
    """Test updating product with non-existent category."""
    update_data = ProductUpdateDTO.model_validate({"category_id": 9999})

    with pytest.raises(NotFoundError):
        await product_service.update_product(sample_product.id, update_data)


@pytest.mark.asyncio
async def test_delete_product_success(product_service, sample_product):
    """Test successful product deletion."""
    product_id = sample_product.id

    await product_service.delete_product(product_id)

    with pytest.raises(NotFoundError):
        await product_service.get_product(product_id)


@pytest.mark.asyncio
async def test_delete_product_not_found(product_service):
    """Test deleting non-existent product."""
    with pytest.raises(NotFoundError):
        await product_service.delete_product(9999)


@pytest.mark.asyncio
async def test_product_sku_case_normalization(product_service, sample_brand, sample_catalog):
    """Test that SKU is normalized to uppercase."""
    product_data = ProductCreateDTO(
        sku="test-lowercase-sku",
        name="Case Test Product",
        price=100.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
    )

    product = await product_service.create_product(product_data)

    assert product.sku == "TEST-LOWERCASE-SKU"


@pytest.mark.asyncio
async def test_product_fields_partial_update(product_service, sample_product):
    """Test partial product update."""
    original_name = sample_product.name

    update_data = ProductUpdateDTO.model_validate({"color": "Black"})  # Only update color

    updated_product = await product_service.update_product(sample_product.id, update_data)

    assert updated_product.name == original_name
    assert updated_product.color == "Black"


@pytest.mark.asyncio
async def test_product_empty_fields_handling(product_service, sample_brand, sample_catalog):
    """Test product creation with optional empty fields."""
    product_data = ProductCreateDTO(
        sku="EMPTY-FIELDS",
        name="Empty Fields Product",
        price=50.0,
        category_id=sample_catalog.id,
        brand_id=sample_brand.id,
        # size, color not provided (should be None)
    )

    product = await product_service.create_product(product_data)

    assert product.id is not None
    assert product.size is None
    assert product.color is None
