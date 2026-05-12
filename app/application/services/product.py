"""Product service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto import (
    ProductCreateDTO,
    ProductListItemDTO,
    ProductReadDTO,
    ProductUpdateDTO,
)
from app.application.ports.persistence import (
    BrandRepositoryPort,
    CatalogRepositoryPort,
    ProductRepositoryPort,
)
from app.domain.exceptions import ConflictError, NotFoundError, ValidationError


class ProductService:
    """Service for product operations."""

    def __init__(
        self,
        session: AsyncSession,
        product_repo: ProductRepositoryPort,
        brand_repo: BrandRepositoryPort,
        catalog_repo: CatalogRepositoryPort,
    ):
        self.session = session
        self.product_repo = product_repo
        self.brand_repo = brand_repo
        self.catalog_repo = catalog_repo

    async def get_product(self, product_id: int) -> ProductReadDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        return ProductReadDTO.model_validate(product)

    async def list_products(self, skip: int = 0, limit: int = 100) -> List[ProductListItemDTO]:
        products = await self.product_repo.get_all(skip, limit)
        return [ProductListItemDTO.model_validate(p) for p in products]

    async def create_product(self, product_data: ProductCreateDTO) -> ProductReadDTO:
        category = await self.catalog_repo.get_by_id(product_data.category_id)
        if not category:
            raise NotFoundError(f"Category with id {product_data.category_id} not found")
        brand = await self.brand_repo.get_by_id(product_data.brand_id)
        if not brand:
            raise NotFoundError(f"Brand with id {product_data.brand_id} not found")
        if await self.product_repo.sku_exists(product_data.sku):
            raise ConflictError(f"Product with SKU '{product_data.sku}' already exists")
        if product_data.price <= 0:
            raise ValidationError("Price must be greater than 0")

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
            stock_quantity=product_data.stock_quantity,
            category_id=product_data.category_id,
            brand_id=product_data.brand_id,
        )
        await self.session.commit()
        return ProductReadDTO.model_validate(product)

    async def update_product(self, product_id: int, product_data: ProductUpdateDTO) -> ProductReadDTO:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        if product_data.category_id:
            category = await self.catalog_repo.get_by_id(product_data.category_id)
            if not category:
                raise NotFoundError(f"Category with id {product_data.category_id} not found")
        if product_data.brand_id:
            brand = await self.brand_repo.get_by_id(product_data.brand_id)
            if not brand:
                raise NotFoundError(f"Brand with id {product_data.brand_id} not found")
        if product_data.price is not None and product_data.price <= 0:
            raise ValidationError("Price must be greater than 0")

        update_data = product_data.model_dump(exclude_unset=True)
        if "sku" in update_data:
            update_data["sku"] = update_data["sku"].upper()
        product = await self.product_repo.update(product_id, **update_data)
        await self.session.commit()
        return ProductReadDTO.model_validate(product)

    async def delete_product(self, product_id: int) -> None:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        await self.product_repo.delete(product_id)
        await self.session.commit()
