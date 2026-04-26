"""Pricing service with deterministic rule pipeline."""

from dataclasses import asdict
from datetime import datetime, timezone

from app.domain.policies import PromotionCombinationPolicy
from app.domain.pricing_rules import (
    BulkDiscountRule,
    CategoryPromoRule,
    LoyaltyDiscountRule,
    TimePromoRule,
    calculate_subtotal,
)
from app.models import Promotion
from app.repositories import PromotionRepository


class PricingService:
    """Service that computes final price with traceable breakdown."""

    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    async def build_breakdown(
        self, items: list[dict[str, float | int]], loyalty_tier: str
    ) -> dict[str, float | list[dict] | list[dict[str, int | float]]]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        subtotal = calculate_subtotal(
            (float(item["unit_price"]), int(item["quantity"])) for item in items
        )
        total_quantity = sum(int(item["quantity"]) for item in items)

        loyalty_result = LoyaltyDiscountRule.apply(subtotal, loyalty_tier)
        bulk_result = BulkDiscountRule.apply(subtotal, total_quantity)

        active_promotions = await self.promotion_repository.get_active(now)
        promo_results = self._apply_promotions(items, subtotal, active_promotions)

        applied_rules = [asdict(loyalty_result), asdict(bulk_result), *[asdict(x) for x in promo_results]]
        total_discount = round(sum(rule["amount"] for rule in applied_rules), 2)
        final_total = round(max(subtotal - total_discount, 0.0), 2)

        return {
            "subtotal": subtotal,
            "total_discount": total_discount,
            "final_total": final_total,
            "applied_rules": applied_rules,
            "items": items,
        }

    def _apply_promotions(
        self, items: list[dict[str, float | int]], subtotal: float, promotions: list[Promotion]
    ):
        if not promotions:
            return []

        if not PromotionCombinationPolicy.allow_combination():
            promotions = promotions[:1]

        promo_results = []
        for promotion in promotions:
            if promotion.promotion_type == "time":
                promo_results.append(
                    TimePromoRule.apply(
                        discountable_total=subtotal,
                        percentage=promotion.discount_percentage,
                        promotion_id=promotion.id,
                    )
                )
                continue

            if promotion.promotion_type == "category" and promotion.category_id is not None:
                category_subtotal = round(
                    sum(
                        float(item["unit_price"]) * int(item["quantity"])
                        for item in items
                        if int(item["category_id"]) == int(promotion.category_id)
                    ),
                    2,
                )
                if category_subtotal > 0:
                    promo_results.append(
                        CategoryPromoRule.apply(
                            category_subtotal=category_subtotal,
                            percentage=promotion.discount_percentage,
                            category_id=promotion.category_id,
                            promotion_id=promotion.id,
                        )
                    )

        return promo_results
