"""Value objects for tactical DDD order modeling."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable money value object with basic validation."""

    amount: float
    currency: str

    @classmethod
    def create(cls, amount: float, currency: str) -> "Money":
        normalized_currency = currency.strip().upper()
        normalized_amount = round(float(amount), 2)

        if normalized_amount < 0:
            raise ValidationError("Amount cannot be negative")
        if len(normalized_currency) != 3 or not normalized_currency.isalpha():
            raise ValidationError("Currency must be a 3-letter ISO-like code")

        return cls(amount=normalized_amount, currency=normalized_currency)

    def add(self, other: "Money") -> "Money":
        self._ensure_same_currency(other)
        return Money.create(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        if factor <= 0:
            raise ValidationError("Money multiplier must be positive")
        return Money.create(self.amount * factor, self.currency)

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValidationError("Money currency mismatch")


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable quantity value object."""

    value: int

    @classmethod
    def create(cls, value: int) -> "Quantity":
        normalized = int(value)
        if normalized <= 0:
            raise ValidationError("Quantity must be positive")
        return cls(value=normalized)


@dataclass(frozen=True, slots=True)
class Sku:
    """Immutable SKU value object."""

    value: str

    @classmethod
    def create(cls, value: str) -> "Sku":
        normalized = value.strip().upper()
        if not normalized:
            raise ValidationError("SKU cannot be empty")
        if not normalized.replace("-", "").replace("_", "").isalnum():
            raise ValidationError("SKU must be alphanumeric with optional hyphens or underscores")
        return cls(value=normalized)
