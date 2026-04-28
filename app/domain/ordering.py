"""Tactical DDD order aggregate and child entities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.domain.base import AggregateRoot
from app.domain.enums import OrderStatus
from app.domain.events import OrderCreatedEvent
from app.domain.exceptions import ValidationError
from app.domain.value_objects import Money, Quantity, Sku
from app.domain.workflow import OrderWorkflowValidator


@dataclass(frozen=True, slots=True)
class OrderLine:
    """Entity-like child object kept inside the Order aggregate."""

    product_id: int
    sku: Sku
    quantity: Quantity
    unit_price: Money

    @classmethod
    def create(
        cls, product_id: int, sku: str, quantity: int, unit_price: float, currency: str
    ) -> "OrderLine":
        if int(product_id) <= 0:
            raise ValidationError("Product id must be positive")
        return cls(
            product_id=int(product_id),
            sku=Sku.create(sku),
            quantity=Quantity.create(quantity),
            unit_price=Money.create(unit_price, currency),
        )

    @property
    def line_total(self) -> Money:
        return self.unit_price.multiply(self.quantity.value)


class Order(AggregateRoot):
    """Rich domain model for the Order aggregate root."""

    def __init__(
        self,
        *,
        customer_id: int,
        lines: list[OrderLine],
        total_price: Money,
        pricing_breakdown: dict[str, Any] | None = None,
        status: str = OrderStatus.PENDING.value,
    ) -> None:
        super().__init__()
        self._id: int | None = None
        self._customer_id = self._validate_customer_id(customer_id)
        self._status = self._validate_status(status)
        self._lines = list(lines)
        self._pricing_breakdown = pricing_breakdown
        self._total_price = total_price
        self._ensure_invariants()

    @classmethod
    def create(
        cls,
        *,
        customer_id: int,
        lines: list[OrderLine],
        total_price: Money,
        pricing_breakdown: dict[str, Any] | None = None,
    ) -> "Order":
        order = cls(
            customer_id=customer_id,
            lines=lines,
            total_price=total_price,
            pricing_breakdown=pricing_breakdown,
            status=OrderStatus.PENDING.value,
        )
        order.raise_domain_event(
            OrderCreatedEvent(
                customer_id=order.customer_id,
                total_amount=order.total_price.amount,
                currency=order.total_price.currency,
                item_count=sum(line.quantity.value for line in order.lines),
            )
        )
        return order

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def total_price(self) -> Money:
        return self._total_price

    @property
    def pricing_breakdown(self) -> dict[str, Any] | None:
        return self._pricing_breakdown

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        return tuple(self._lines)

    def assign_persistence_id(self, order_id: int) -> None:
        if self._id is not None:
            raise ValidationError("Order id is already assigned")
        if int(order_id) <= 0:
            raise ValidationError("Order id must be positive")
        self._id = int(order_id)

    def add_item(self, line: OrderLine) -> None:
        self._ensure_currency(line.unit_price.currency)
        self._lines.append(line)
        self._ensure_invariants()

    def confirm(self) -> None:
        OrderWorkflowValidator.validate_transition(self._status, OrderStatus.CONFIRMED.value)
        self._status = OrderStatus.CONFIRMED.value

    def cancel(self) -> None:
        OrderWorkflowValidator.validate_transition(self._status, OrderStatus.CANCELLED.value)
        self._status = OrderStatus.CANCELLED.value

    def mark_shipped(self) -> None:
        OrderWorkflowValidator.validate_transition(self._status, OrderStatus.SHIPPED.value)
        self._status = OrderStatus.SHIPPED.value

    def mark_delivered(self) -> None:
        OrderWorkflowValidator.validate_transition(self._status, OrderStatus.DELIVERED.value)
        self._status = OrderStatus.DELIVERED.value

    def _ensure_invariants(self) -> None:
        if not self._lines:
            raise ValidationError("Order must contain at least one item")

        self._ensure_currency(self._total_price.currency)

        subtotal = Money.create(0, self._total_price.currency)
        for line in self._lines:
            self._ensure_currency(line.unit_price.currency)
            subtotal = subtotal.add(line.line_total)

        if self._pricing_breakdown is not None:
            breakdown_subtotal = self._pricing_breakdown.get("subtotal")
            if breakdown_subtotal is not None and round(float(breakdown_subtotal), 2) != subtotal.amount:
                raise ValidationError("Pricing breakdown subtotal must match order lines subtotal")

            breakdown_total = self._pricing_breakdown.get("final_total")
            if breakdown_total is not None and round(float(breakdown_total), 2) != self._total_price.amount:
                raise ValidationError("Pricing breakdown final_total must match order total")

    def _ensure_currency(self, currency: str) -> None:
        if currency != self._total_price.currency:
            raise ValidationError("All order monetary values must use the same currency")

    def _validate_customer_id(self, customer_id: int) -> int:
        if int(customer_id) <= 0:
            raise ValidationError("Customer id must be positive")
        return int(customer_id)

    def _validate_status(self, status: str) -> str:
        try:
            return OrderStatus(status).value
        except ValueError as exc:
            raise ValidationError(f"Invalid order status: {status}") from exc
