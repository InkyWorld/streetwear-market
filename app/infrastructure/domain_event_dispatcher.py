"""In-memory implementation of domain event dispatcher."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from app.application.events import DomainEventHandler, IDomainEventDispatcher
from app.domain.events import DomainEvent


class InMemoryDomainEventDispatcher(IDomainEventDispatcher):
    """Simple in-memory dispatcher keyed by event type."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[DomainEventHandler]] = defaultdict(list)

    def register(self, event_type: type[DomainEvent], handler: DomainEventHandler) -> None:
        """Register a handler for a domain event type."""
        self._handlers[event_type].append(handler)

    async def dispatch(
        self, events: Iterable[DomainEvent], context: dict[str, Any] | None = None
    ) -> None:
        """Dispatch each event to all registered handlers."""
        for event in events:
            for handler in self._handlers.get(type(event), []):
                await handler.handle(event, context=context)
