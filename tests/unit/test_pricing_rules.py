"""Unit tests for advanced pricing rules."""

from app.domain.pricing_rules import BulkDiscountRule, LoyaltyDiscountRule


def test_loyalty_rule_gold_discount():
    result = LoyaltyDiscountRule.apply(subtotal=200.0, loyalty_tier="gold")
    assert result.amount == 20.0
    assert result.metadata["tier"] == "gold"


def test_bulk_discount_threshold_5_items():
    result = BulkDiscountRule.apply(subtotal=100.0, total_quantity=5)
    assert result.amount == 5.0
    assert result.metadata["percentage"] == 0.05


def test_bulk_discount_threshold_10_items():
    result = BulkDiscountRule.apply(subtotal=100.0, total_quantity=10)
    assert result.amount == 10.0
    assert result.metadata["percentage"] == 0.1
