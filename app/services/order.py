"""Order service."""

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import LoyaltyTier
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.workflow import OrderWorkflowValidator
from app.repositories import CustomerRepository, OrderItemRepository, OrderRepository, ProductRepository
from app.schemas import OrderCreateDTO, OrderListItemDTO, OrderReadDTO
from app.services.inventory import InventoryService
from app.services.pricing import PricingService
from app.repositories import PromotionRepository


class OrderService:
    """Service for order operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.order_item_repo = OrderItemRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.product_repo = ProductRepository(session)
        self.promotion_repo = PromotionRepository(session)
        self.pricing_service = PricingService(self.promotion_repo)
        self.inventory_service = InventoryService(session)

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

    def _calculate_loyalty_discount(self, loyalty_tier: str) -> float:
        """Calculate discount percentage based on loyalty tier."""
        try:
            tier = LoyaltyTier(loyalty_tier)
            return tier.get_discount_percentage()
        except ValueError:
            return 0.0

    async def create_order(self, order_data: OrderCreateDTO) -> OrderReadDTO:
        """Create a new order with validation, inventory check, and loyalty pricing."""
        # Validate customer exists
        customer = await self.customer_repo.get_by_id(order_data.customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {order_data.customer_id} not found")

        # Validate and collect items with inventory check
        items_to_create = []

        for item in order_data.items:
            # Validate product exists
            product = await self.product_repo.get_by_id(item.product_id)
            if not product:
                raise NotFoundError(f"Product with id {item.product_id} not found")

            # Check inventory/stock availability
            if not product.in_stock:
                raise ValidationError(
                    f"Product '{product.name}' (ID: {item.product_id}) is not in stock"
                )

            if product.stock_quantity is not None and product.stock_quantity < item.quantity:
                raise ValidationError(
                    f"Insufficient stock for product '{product.name}'. "
                    f"Requested: {item.quantity}, Available: {product.stock_quantity}"
                )

            items_to_create.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": product.price,
                    "category_id": product.category_id,
                }
            )

        pricing_breakdown = await self.pricing_service.build_breakdown(
            items=items_to_create,
            loyalty_tier=customer.loyalty_tier,
        )
        total_amount = float(pricing_breakdown["final_total"])

        try:
            reservation_ids = await self.inventory_service.hold_items(
                order_id=None, items=items_to_create
            )
            order = await self.order_repo.create_with_items(
                customer_id=order_data.customer_id,
                status="pending",
                total_amount=total_amount,
                items_data=items_to_create,
                pricing_breakdown=pricing_breakdown,
            )
            await self.inventory_service.attach_holds_to_order(order.id, reservation_ids)

            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise ValidationError(f"Failed to create order: {str(e)}")

        # Re-fetch order with eager-loaded items to avoid async lazy-loading
        # when serializing response DTO in FastAPI.
        created_order = await self.order_repo.get_by_id(order.id)
        return OrderReadDTO.model_validate(created_order)

    async def change_order_status(self, order_id: int, new_status: str) -> OrderReadDTO:
        """Change order status with workflow validation."""
        # Get existing order
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError(f"Order with id {order_id} not found")

        # Validate workflow transition
        OrderWorkflowValidator.validate_transition(order.status, new_status)

        # Update status
        await self.order_repo.update(order_id, status=new_status)
        if new_status == "confirmed":
            await self.inventory_service.commit_holds_for_order(order_id)
        if new_status == "cancelled":
            await self.inventory_service.release_holds_for_order(order_id, reason="order_cancelled")
        await self.session.commit()

        # Re-fetch order
        updated_order = await self.order_repo.get_by_id(order_id)
        return OrderReadDTO.model_validate(updated_order)
