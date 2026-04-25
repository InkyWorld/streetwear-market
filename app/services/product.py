"""Product service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import ConflictError, NotFoundError, ValidationError
from app.repositories import BrandRepository, CatalogRepository, ProductRepository
from app.schemas import (
    ProductCreateDTO,
    ProductListItemDTO,
    ProductReadDTO,
    ProductUpdateDTO,
)


class ProductService:
    """Service for product operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)
        self.brand_repo = BrandRepository(session)
        self.catalog_repo = CatalogRepository(session)

    async def get_product(self, product_id: int) -> ProductReadDTO:
        """Get product by id."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        return ProductReadDTO.model_validate(product)

    async def list_products(self, skip: int = 0, limit: int = 100) -> List[ProductListItemDTO]:
        """List all products."""
        products = await self.product_repo.get_all(skip, limit)
        return [ProductListItemDTO.model_validate(p) for p in products]

    async def create_product(self, product_data: ProductCreateDTO) -> ProductReadDTO:
        """Create a new product."""
        # Validate category exists
        category = await self.catalog_repo.get_by_id(product_data.category_id)
        if not category:
            raise NotFoundError(f"Category with id {product_data.category_id} not found")

        # Validate brand exists
        brand = await self.brand_repo.get_by_id(product_data.brand_id)
        if not brand:
            raise NotFoundError(f"Brand with id {product_data.brand_id} not found")

        # Check SKU uniqueness
        if await self.product_repo.sku_exists(product_data.sku):
            raise ConflictError(f"Product with SKU '{product_data.sku}' already exists")

        # Validate price
        if product_data.price <= 0:
            raise ValidationError("Price must be greater than 0")

        # Create product
        product = await self.product_repo.create(
            sku=product_data.sku.upper(),
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            currency=product_data.currency,
            size=product_data.size,
            color=product_data.color,
            season=product_data.season,
            in_stock=product_data.in_stock,
            category_id=product_data.category_id,
            brand_id=product_data.brand_id,
        )

        await self.session.commit()
        return ProductReadDTO.model_validate(product)

    async def update_product(
        self, product_id: int, product_data: ProductUpdateDTO
    ) -> ProductReadDTO:
        """Update an existing product."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")

        # Validate category if provided
        if product_data.category_id:
            category = await self.catalog_repo.get_by_id(product_data.category_id)
            if not category:
                raise NotFoundError(f"Category with id {product_data.category_id} not found")

        # Validate brand if provided
        if product_data.brand_id:
            brand = await self.brand_repo.get_by_id(product_data.brand_id)
            if not brand:
                raise NotFoundError(f"Brand with id {product_data.brand_id} not found")

        # Validate price if provided
        if product_data.price is not None and product_data.price <= 0:
            raise ValidationError("Price must be greater than 0")

        # Update product
        update_data = product_data.model_dump(exclude_unset=True)
        if "sku" in update_data:
            update_data["sku"] = update_data["sku"].upper()

        product = await self.product_repo.update(product_id, **update_data)
        await self.session.commit()

        return ProductReadDTO.model_validate(product)

    async def delete_product(self, product_id: int) -> None:
        """Delete a product."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")

        await self.product_repo.delete(product_id)
        await self.session.commit()
