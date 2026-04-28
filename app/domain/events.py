"""Domain event types used by tactical DDD models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base immutable domain event."""

    occurred_at: datetime = field(default_factory=_utcnow)


@dataclass(frozen=True, slots=True)
class OrderCreatedEvent(DomainEvent):
    """Raised when a new order aggregate is created."""

    customer_id: int = 0
    total_amount: float = 0.0
    currency: str = "USD"
    item_count: int = 0
