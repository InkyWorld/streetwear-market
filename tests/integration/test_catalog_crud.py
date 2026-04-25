"""Integration tests for Catalog CRUD operations."""

import pytest

from app.domain.exceptions import NotFoundError
from app.schemas import CatalogCreateDTO


@pytest.mark.asyncio
async def test_create_catalog_success(catalog_service):
    """Test successful catalog creation."""
    catalog = await catalog_service.create_catalog(
        CatalogCreateDTO(name="Outerwear", description="Jackets and coats")
    )

    assert catalog.id is not None
    assert catalog.name == "Outerwear"
    assert catalog.description == "Jackets and coats"


@pytest.mark.asyncio
async def test_get_catalog_success(catalog_service, sample_catalog):
    """Test getting catalog by id."""
    catalog = await catalog_service.get_catalog(sample_catalog.id)

    assert catalog.id == sample_catalog.id
    assert catalog.name == sample_catalog.name
    assert catalog.description == sample_catalog.description


@pytest.mark.asyncio
async def test_get_catalog_not_found(catalog_service):
    """Test getting non-existent catalog."""
    with pytest.raises(NotFoundError) as exc_info:
        await catalog_service.get_catalog(9999)

    assert "not found" in exc_info.value.message


@pytest.mark.asyncio
async def test_list_catalogs(catalog_service, sample_catalog):
    """Test listing catalogs."""
    catalogs = await catalog_service.list_catalogs()

    assert len(catalogs) >= 1
    assert any(c.id == sample_catalog.id for c in catalogs)


@pytest.mark.asyncio
async def test_list_catalogs_pagination(catalog_service):
    """Test listing catalogs with pagination."""
    for i in range(5):
        await catalog_service.create_catalog(
            CatalogCreateDTO(name=f"Catalog {i}", description=f"Description {i}")
        )

    first_page = await catalog_service.list_catalogs(skip=0, limit=2)
    second_page = await catalog_service.list_catalogs(skip=2, limit=2)

    assert len(first_page) == 2
    assert len(second_page) == 2
