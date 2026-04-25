"""Order service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import NotFoundError, ValidationError
from app.repositories import CustomerRepository, OrderItemRepository, OrderRepository, ProductRepository
from app.schemas import OrderCreateDTO, OrderListItemDTO, OrderReadDTO


class OrderService:
    """Service for order operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.order_item_repo = OrderItemRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.product_repo = ProductRepository(session)

    async def get_order(self, order_id: int) -> OrderReadDTO:
        """Get order by id."""
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError(f"Order with id {order_id} not found")
        return OrderReadDTO.model_validate(order)

    async def list_orders(self, skip: int = 0, limit: int = 100) -> List[OrderListItemDTO]:
        """List all orders."""
        orders = await self.order_repo.get_all(skip, limit)
        return [OrderListItemDTO.model_validate(o) for o in orders]

    async def list_customer_orders(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderListItemDTO]:
        """List orders for a specific customer."""
        # Verify customer exists
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {customer_id} not found")

        orders = await self.order_repo.get_by_customer_id(customer_id, skip, limit)
        return [OrderListItemDTO.model_validate(o) for o in orders]

    async def create_order(self, order_data: OrderCreateDTO) -> OrderReadDTO:
        """Create a new order with validation."""
        # Validate customer exists
        customer = await self.customer_repo.get_by_id(order_data.customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {order_data.customer_id} not found")

        # Validate and collect items
        total_amount = 0.0
        items_to_create = []

        for item in order_data.items:
            # Validate product exists and is in stock
            product = await self.product_repo.get_by_id(item.product_id)
            if not product:
                raise NotFoundError(f"Product with id {item.product_id} not found")

            if not product.in_stock:
                raise ValidationError(f"Product with id {item.product_id} is not in stock")

            # Calculate total for this item
            item_total = product.price * item.quantity
            total_amount += item_total

            items_to_create.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": product.price,
                }
            )

        # Create order with items in transaction
        order = await self.order_repo.create_with_items(
            customer_id=order_data.customer_id,
            status="pending",
            total_amount=total_amount,
            items_data=items_to_create,
        )

        await self.session.commit()
        # Re-fetch order with eager-loaded items to avoid async lazy-loading
        # when serializing response DTO in FastAPI.
        created_order = await self.order_repo.get_by_id(order.id)
        return OrderReadDTO.model_validate(created_order)
