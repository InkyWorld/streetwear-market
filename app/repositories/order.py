"""Order and OrderItem repositories."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.ordering import Order as DomainOrder
from app.models import Order, OrderItem
from app.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    """Repository for OrderItem model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderItem)

    async def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        """Get all items for a specific order."""
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class OrderRepository(BaseRepository[Order]):
    """Repository for Order model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def get_by_id(self, id: int) -> Optional[Order]:
        """Get order by id with items."""
        stmt = select(Order).where(Order.id == id).options(selectinload(Order.items))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with items."""
        stmt = select(Order).offset(skip).limit(limit).options(selectinload(Order.items))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_customer_id(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """Get orders for a specific customer."""
        stmt = (
            select(Order)
            .where(Order.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
            .options(selectinload(Order.items))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_with_items(
        self,
        customer_id: int,
        status: str,
        total_amount: float,
        items_data: List[dict],
        pricing_breakdown: dict | None = None,
    ) -> Order:
        """Create order with items in a single transaction."""
        # Create order
        order = Order(
            customer_id=customer_id,
            status=status,
            total_amount=total_amount,
            pricing_breakdown=pricing_breakdown,
        )
        self.session.add(order)
        await self.session.flush()

        # Create order items
        for item_data in items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
            )
            self.session.add(order_item)

        await self.session.flush()
        return order

    async def create_from_aggregate(self, aggregate: DomainOrder) -> Order:
        """Persist a domain aggregate using existing ORM tables."""
        order = Order(
            customer_id=aggregate.customer_id,
            status=aggregate.status,
            total_amount=aggregate.total_price.amount,
            pricing_breakdown=aggregate.pricing_breakdown,
        )
        self.session.add(order)
        await self.session.flush()

        aggregate.assign_persistence_id(order.id)

        for line in aggregate.lines:
            self.session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=line.product_id,
                    quantity=line.quantity.value,
                    unit_price=line.unit_price.amount,
                )
            )

        await self.session.flush()
        return order
