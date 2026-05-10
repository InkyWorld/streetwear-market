"""Composition helpers for order application use cases."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.orders.create_order import CreateOrderCommandHandler
from app.application.orders.event_handlers import OrderCreatedEventHandler
from app.domain.events import OrderCreatedEvent
from app.infrastructure.domain_event_dispatcher import InMemoryDomainEventDispatcher


def build_create_order_handler(session: AsyncSession) -> CreateOrderCommandHandler:
    """Build create-order handler with in-memory event dispatcher."""
    dispatcher = InMemoryDomainEventDispatcher()
    dispatcher.register(OrderCreatedEvent, OrderCreatedEventHandler(session))
    return CreateOrderCommandHandler(session=session, dispatcher=dispatcher)
