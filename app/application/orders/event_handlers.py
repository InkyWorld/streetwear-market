"""Domain event handlers related to order use cases."""

from __future__ import annotations

import logging
from typing import Any

from app.application.services.inventory import InventoryService
from app.domain.events import DomainEvent, OrderCreatedEvent

logger = logging.getLogger(__name__)


class OrderCreatedEventHandler:
    """Handle order-created side effects in application layer."""

    def __init__(self, inventory_service: InventoryService):
        self.inventory_service = inventory_service

    async def handle(self, event: DomainEvent, context: dict[str, Any] | None = None) -> None:
        """Reserve inventory and provide integration extension point."""
        if not isinstance(event, OrderCreatedEvent):
            return

        logger.info(
            "OrderCreatedEvent: customer_id=%s total_amount=%s currency=%s item_count=%s",
            event.customer_id,
            event.total_amount,
            event.currency,
            event.item_count,
        )

        order_id = (context or {}).get("order_id")
        items_to_reserve = (context or {}).get("items_to_reserve", [])
        if order_id is not None and items_to_reserve:
            await self.inventory_service.hold_items(order_id=order_id, items=items_to_reserve)


