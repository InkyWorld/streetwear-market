"""Command models for order use cases."""

from __future__ import annotations

from dataclasses import dataclass


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
