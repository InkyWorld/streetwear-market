"""Create order use case command and handler."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events import IDomainEventDispatcher
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.ordering import Order as DomainOrder
from app.domain.ordering import OrderLine
from app.domain.value_objects import Money
from app.repositories import CustomerRepository, OrderRepository, ProductRepository, PromotionRepository
from app.schemas import OrderReadDTO
from app.services.pricing import PricingService


@dataclass(frozen=True, slots=True)
class CreateOrderItemCommand:
    """Single order line command model."""

    product_id: int
    quantity: int


@dataclass(frozen=True, slots=True)
class CreateOrderCommand:
    """Command object for create-order use case."""

    customer_id: int
    items: tuple[CreateOrderItemCommand, ...]


class CreateOrderCommandHandler:
    """Application use case for creating orders."""

    def __init__(self, session: AsyncSession, dispatcher: IDomainEventDispatcher):
        self.session = session
        self.dispatcher = dispatcher
        self.order_repo = OrderRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.product_repo = ProductRepository(session)
        self.promotion_repo = PromotionRepository(session)
        self.pricing_service = PricingService(self.promotion_repo)

    async def handle(self, command: CreateOrderCommand) -> OrderReadDTO:
        """Execute create-order use case and dispatch domain events."""
        customer = await self.customer_repo.get_by_id(command.customer_id)
        if not customer:
            raise NotFoundError(f"Customer with id {command.customer_id} not found")

        items_to_create: list[dict] = []
        domain_lines: list[OrderLine] = []

        for item in command.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if not product:
                raise NotFoundError(f"Product with id {item.product_id} not found")

            if not product.in_stock:
                raise ValidationError(f"Product '{product.name}' (ID: {item.product_id}) is not in stock")

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
            domain_lines.append(
                OrderLine.create(
                    product_id=product.id,
                    sku=product.sku,
                    quantity=item.quantity,
                    unit_price=product.price,
                    currency=product.currency,
                )
            )

        pricing_breakdown = await self.pricing_service.build_breakdown(
            items=items_to_create,
            loyalty_tier=customer.loyalty_tier,
        )
        order_total = Money.create(
            amount=float(pricing_breakdown["final_total"]),
            currency=domain_lines[0].unit_price.currency,
        )
        aggregate = DomainOrder.create(
            customer_id=command.customer_id,
            lines=domain_lines,
            total_price=order_total,
            pricing_breakdown=pricing_breakdown,
        )

        try:
            order = await self.order_repo.create_from_aggregate(aggregate)
            raised_events = aggregate.pull_domain_events()
            await self.dispatcher.dispatch(
                raised_events,
                context={"order_id": order.id, "items_to_reserve": items_to_create},
            )
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            if isinstance(exc, (NotFoundError, ValidationError)):
                raise
            raise ValidationError(f"Failed to create order: {str(exc)}") from exc

        created_order = await self.order_repo.get_by_id(order.id)
        return OrderReadDTO.model_validate(created_order)
