"""Order service."""

from typing import List
from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto import OrderCreateDTO, OrderListItemDTO, OrderReadDTO
from app.application.orders import CreateOrderCommand, CreateOrderItemCommand
from app.application.orders.create_order import CreateOrderCommandHandler
from app.application.services.inventory import InventoryService
from app.application.ports.persistence import (
    CustomerRepositoryPort,
    OrderItemRepositoryPort,
    OrderRepositoryPort,
    ProductRepositoryPort,
)
from app.domain.enums import LoyaltyTier
from app.domain.exceptions import NotFoundError
from app.domain.workflow import OrderWorkflowValidator


class OrderService:
    def __init__(
        self,
        session: AsyncSession,
        order_repo: OrderRepositoryPort,
        order_item_repo: OrderItemRepositoryPort,
        customer_repo: CustomerRepositoryPort,
        product_repo: ProductRepositoryPort,
        inventory_service: InventoryService,
        create_order_handler_factory: Callable[[AsyncSession], CreateOrderCommandHandler],
    ):
        self.session = session
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.customer_repo = customer_repo
        self.product_repo = product_repo
        self.inventory_service = inventory_service
        self.create_order_handler_factory = create_order_handler_factory

    async def get_order(self, order_id: int) -> OrderReadDTO:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError(f"Order with id {order_id} not found")
        return OrderReadDTO.model_validate(order)

    async def list_orders(self, skip: int = 0, limit: int = 100) -> List[OrderListItemDTO]:
        orders = await self.order_repo.get_all(skip, limit)
        return [OrderListItemDTO.model_validate(o) for o in orders]

    async def list_customer_orders(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderListItemDTO]:
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {customer_id} not found")
        orders = await self.order_repo.get_by_customer_id(customer_id, skip, limit)
        return [OrderListItemDTO.model_validate(o) for o in orders]

    def _calculate_loyalty_discount(self, loyalty_tier: str) -> float:
        try:
            tier = LoyaltyTier(loyalty_tier)
            return tier.get_discount_percentage()
        except ValueError:
            return 0.0

    async def create_order(self, order_data: OrderCreateDTO) -> OrderReadDTO:
        command = CreateOrderCommand(
            customer_id=order_data.customer_id,
            items=tuple(
                CreateOrderItemCommand(product_id=item.product_id, quantity=item.quantity)
                for item in order_data.items
            ),
        )
        handler = self.create_order_handler_factory(self.session)
        return await handler.handle(command)

    async def change_order_status(self, order_id: int, new_status: str) -> OrderReadDTO:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundError(f"Order with id {order_id} not found")
        OrderWorkflowValidator.validate_transition(order.status, new_status)
        await self.order_repo.update(order_id, status=new_status)
        if new_status == "confirmed":
            await self.inventory_service.commit_holds_for_order(order_id)
        if new_status == "cancelled":
            await self.inventory_service.release_holds_for_order(order_id, reason="order_cancelled")
        await self.session.commit()
        updated_order = await self.order_repo.get_by_id(order_id)
        return OrderReadDTO.model_validate(updated_order)
