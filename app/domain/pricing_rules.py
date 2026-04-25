"""Pricing rules for deterministic pricing pipeline."""

from dataclasses import dataclass
from typing import Iterable

from app.domain.enums import LoyaltyTier


@dataclass(slots=True)
class PricingRuleResult:
    """Represents a single pricing rule application."""

    rule: str
    amount: float
    metadata: dict[str, str | float | int]


class LoyaltyDiscountRule:
    """Tier-based loyalty discount rule."""

    name = "loyalty_tier_discount"

    @staticmethod
    def apply(subtotal: float, loyalty_tier: str) -> PricingRuleResult:
        try:
            percentage = LoyaltyTier(loyalty_tier).get_discount_percentage()
        except ValueError:
            percentage = 0.0

        return PricingRuleResult(
            rule=LoyaltyDiscountRule.name,
            amount=round(subtotal * percentage, 2),
            metadata={"tier": loyalty_tier, "percentage": percentage},
        )


class BulkDiscountRule:
    """Bulk discount rule by total item quantity."""

    name = "bulk_quantity_discount"

    @staticmethod
    def _resolve_percentage(quantity: int) -> float:
        if quantity >= 10:
            return 0.1
        if quantity >= 5:
            return 0.05
        return 0.0

    @classmethod
    def apply(cls, subtotal: float, total_quantity: int) -> PricingRuleResult:
        percentage = cls._resolve_percentage(total_quantity)
        return PricingRuleResult(
            rule=cls.name,
            amount=round(subtotal * percentage, 2),
            metadata={"total_quantity": total_quantity, "percentage": percentage},
        )


class TimePromoRule:
    """Time window promotion rule."""

    name = "time_promotion_discount"

    @staticmethod
    def apply(discountable_total: float, percentage: float, promotion_id: int) -> PricingRuleResult:
        return PricingRuleResult(
            rule=TimePromoRule.name,
            amount=round(discountable_total * percentage, 2),
            metadata={"promotion_id": promotion_id, "percentage": percentage},
        )


class CategoryPromoRule:
    """Category promotion rule."""

    name = "category_promotion_discount"

    @staticmethod
    def apply(
        category_subtotal: float, percentage: float, category_id: int, promotion_id: int
    ) -> PricingRuleResult:
        return PricingRuleResult(
            rule=CategoryPromoRule.name,
            amount=round(category_subtotal * percentage, 2),
            metadata={
                "promotion_id": promotion_id,
                "category_id": category_id,
                "percentage": percentage,
            },
        )


def calculate_subtotal(unit_prices: Iterable[tuple[float, int]]) -> float:
    """Calculate subtotal from unit price and quantity pairs."""
    return round(sum(price * quantity for price, quantity in unit_prices), 2)
