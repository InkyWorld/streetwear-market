"""Base classes for tactical DDD domain models."""

from __future__ import annotations

from app.domain.events import DomainEvent


class AggregateRoot:
    """Base aggregate root that stores raised domain events."""

    def __init__(self) -> None:
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        return tuple(self._domain_events)

    def raise_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
