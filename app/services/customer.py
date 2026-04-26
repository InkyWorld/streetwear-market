"""Customer service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import ConflictError, NotFoundError, ValidationError
from app.repositories import CustomerRepository
from app.schemas import CustomerCreateDTO, CustomerListItemDTO, CustomerReadDTO, CustomerUpdateDTO


class CustomerService:
    """Service for customer operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.customer_repo = CustomerRepository(session)

    async def get_customer(self, customer_id: int) -> CustomerReadDTO:
        """Get customer by id."""
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {customer_id} not found")
        return CustomerReadDTO.model_validate(customer)

    async def list_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerListItemDTO]:
        """List all customers."""
        customers = await self.customer_repo.get_all(skip, limit)
        return [CustomerListItemDTO.model_validate(c) for c in customers]

    async def create_customer(self, customer_data: CustomerCreateDTO) -> CustomerReadDTO:
        """Create a new customer."""
        # Validate email uniqueness
        if await self.customer_repo.email_exists(customer_data.email):
            raise ConflictError(f"Customer with email '{customer_data.email}' already exists")

        # Validate full_name
        if not customer_data.full_name.strip():
            raise ValidationError("Full name cannot be empty")

        # Create customer
        customer = await self.customer_repo.create(
            full_name=customer_data.full_name,
            email=customer_data.email.lower(),
            phone=customer_data.phone,
            loyalty_tier=customer_data.loyalty_tier,
        )

        await self.session.commit()
        return CustomerReadDTO.model_validate(customer)

    async def update_customer(self, customer_id: int, customer_data: CustomerUpdateDTO) -> CustomerReadDTO:
        """Update a customer."""
        existing = await self.customer_repo.get_by_id(customer_id)
        if not existing:
            raise NotFoundError(f"Customer with id {customer_id} not found")

        if customer_data.email and await self.customer_repo.email_exists(customer_data.email, exclude_id=customer_id):
            raise ConflictError(f"Customer with email '{customer_data.email}' already exists")

        updated = await self.customer_repo.update(
            customer_id,
            full_name=customer_data.full_name,
            email=customer_data.email.lower() if customer_data.email else None,
            phone=customer_data.phone,
            loyalty_tier=customer_data.loyalty_tier,
        )
        await self.session.commit()
        return CustomerReadDTO.model_validate(updated)

    async def delete_customer(self, customer_id: int) -> None:
        """Delete a customer."""
        deleted = await self.customer_repo.delete(customer_id)
        if not deleted:
            raise NotFoundError(f"Customer with id {customer_id} not found")
        await self.session.commit()
