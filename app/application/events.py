"""Application contracts for domain event dispatching."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Protocol

from app.domain.events import DomainEvent


class DomainEventHandler(Protocol):
    """Contract for asynchronous domain event handlers."""

    async def handle(self, event: DomainEvent, context: dict[str, Any] | None = None) -> None:
        """Handle a single domain event."""


class IDomainEventDispatcher(Protocol):
    """Contract for dispatching raised domain events."""

    async def dispatch(
        self, events: Iterable[DomainEvent], context: dict[str, Any] | None = None
    ) -> None:
        """Dispatch a collection of events."""
