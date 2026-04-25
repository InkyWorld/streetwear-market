"""Unit tests for order workflow transitions and loyalty tier pricing."""

import pytest

from app.domain.enums import LoyaltyTier, OrderStatus
from app.domain.exceptions import ValidationError
from app.domain.workflow import OrderWorkflowValidator


class TestOrderStatusEnum:
    """Tests for OrderStatus enum."""

    def test_valid_status_values(self):
        """Test all valid status values exist."""
        assert OrderStatus.PENDING.value == "pending"
        assert OrderStatus.CONFIRMED.value == "confirmed"
        assert OrderStatus.SHIPPED.value == "shipped"
        assert OrderStatus.DELIVERED.value == "delivered"

    def test_pending_can_transition_to_confirmed(self):
        """Test pending can transition to confirmed."""
        assert OrderStatus.PENDING.can_transition_to(OrderStatus.CONFIRMED)

    def test_pending_cannot_transition_to_shipped(self):
        """Test pending cannot transition directly to shipped."""
        assert not OrderStatus.PENDING.can_transition_to(OrderStatus.SHIPPED)

    def test_pending_cannot_transition_to_delivered(self):
        """Test pending cannot transition directly to delivered."""
        assert not OrderStatus.PENDING.can_transition_to(OrderStatus.DELIVERED)

    def test_confirmed_can_transition_to_shipped(self):
        """Test confirmed can transition to shipped."""
        assert OrderStatus.CONFIRMED.can_transition_to(OrderStatus.SHIPPED)

    def test_confirmed_cannot_transition_to_pending(self):
        """Test confirmed cannot transition back to pending."""
        assert not OrderStatus.CONFIRMED.can_transition_to(OrderStatus.PENDING)

    def test_shipped_can_transition_to_delivered(self):
        """Test shipped can transition to delivered."""
        assert OrderStatus.SHIPPED.can_transition_to(OrderStatus.DELIVERED)

    def test_delivered_is_terminal_state(self):
        """Test delivered has no valid transitions."""
        assert OrderStatus.DELIVERED.get_valid_transitions(OrderStatus.DELIVERED) == []

class TestOrderWorkflowValidator:
    """Tests for OrderWorkflowValidator."""

    def test_valid_transition_pending_to_confirmed(self):
        """Test valid transition from pending to confirmed."""
        # Should not raise
        OrderWorkflowValidator.validate_transition("pending", "confirmed")

    def test_valid_transition_confirmed_to_shipped(self):
        """Test valid transition from confirmed to shipped."""
        OrderWorkflowValidator.validate_transition("confirmed", "shipped")

    def test_valid_transition_shipped_to_delivered(self):
        """Test valid transition from shipped to delivered."""
        OrderWorkflowValidator.validate_transition("shipped", "delivered")

    def test_invalid_transition_pending_to_shipped(self):
        """Test invalid transition raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            OrderWorkflowValidator.validate_transition("pending", "shipped")
        assert "Cannot transition" in str(exc_info.value)

    def test_invalid_transition_pending_to_delivered(self):
        """Test invalid transition raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            OrderWorkflowValidator.validate_transition("pending", "delivered")
        assert "Cannot transition" in str(exc_info.value)

    def test_invalid_transition_confirmed_to_delivered(self):
        """Test invalid transition raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            OrderWorkflowValidator.validate_transition("confirmed", "delivered")
        assert "Cannot transition" in str(exc_info.value)

    def test_invalid_current_status_raises_error(self):
        """Test invalid current status raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            OrderWorkflowValidator.validate_transition("invalid_status", "confirmed")
        assert "Invalid current status" in str(exc_info.value)

    def test_invalid_new_status_raises_error(self):
        """Test invalid new status raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            OrderWorkflowValidator.validate_transition("pending", "invalid_status")
        assert "Invalid new status" in str(exc_info.value)

    def test_get_valid_transitions_from_pending(self):
        """Test getting valid transitions from pending."""
        valid = OrderWorkflowValidator.get_valid_transitions("pending")
        assert "confirmed" in valid
        assert len(valid) == 1

    def test_get_valid_transitions_from_confirmed(self):
        """Test getting valid transitions from confirmed."""
        valid = OrderWorkflowValidator.get_valid_transitions("confirmed")
        assert "shipped" in valid
        assert len(valid) == 1

    def test_get_valid_transitions_from_delivered(self):
        """Test delivered has no valid transitions."""
        valid = OrderWorkflowValidator.get_valid_transitions("delivered")
        assert valid == []

    def test_get_valid_transitions_invalid_status(self):
        """Test invalid status returns empty list."""
        valid = OrderWorkflowValidator.get_valid_transitions("invalid")
        assert valid == []


class TestLoyaltyTierEnum:
    """Tests for LoyaltyTier enum."""

    def test_bronze_tier_no_discount(self):
        """Test bronze tier has no discount."""
        assert LoyaltyTier.BRONZE.get_discount_percentage() == 0.0

    def test_silver_tier_five_percent_discount(self):
        """Test silver tier has 5% discount."""
        assert LoyaltyTier.SILVER.get_discount_percentage() == 0.05

    def test_gold_tier_ten_percent_discount(self):
        """Test gold tier has 10% discount."""
        assert LoyaltyTier.GOLD.get_discount_percentage() == 0.10

    def test_tier_values(self):
        """Test tier values."""
        assert LoyaltyTier.BRONZE.value == "bronze"
        assert LoyaltyTier.SILVER.value == "silver"
        assert LoyaltyTier.GOLD.value == "gold"


class TestLoyaltyPricingCalculation:
    """Tests for loyalty tier pricing calculation in OrderService."""

    def test_bronze_tier_no_discount(self):
        """Test bronze tier calculates no discount."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        discount = service._calculate_loyalty_discount("bronze")
        assert discount == 0.0

    def test_silver_tier_five_percent_discount(self):
        """Test silver tier calculates 5% discount."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        discount = service._calculate_loyalty_discount("silver")
        assert discount == 0.05

    def test_gold_tier_ten_percent_discount(self):
        """Test gold tier calculates 10% discount."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        discount = service._calculate_loyalty_discount("gold")
        assert discount == 0.10

    def test_unknown_tier_defaults_to_no_discount(self):
        """Test unknown tier defaults to no discount."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        discount = service._calculate_loyalty_discount("unknown")
        assert discount == 0.0

    def test_price_calculation_with_bronze_tier(self):
        """Test price calculation with bronze tier (no discount)."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        subtotal = 100.0
        discount = service._calculate_loyalty_discount("bronze")
        total = subtotal - (subtotal * discount)
        assert total == 100.0

    def test_price_calculation_with_silver_tier(self):
        """Test price calculation with silver tier (5% discount)."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        subtotal = 100.0
        discount = service._calculate_loyalty_discount("silver")
        total = subtotal - (subtotal * discount)
        assert total == 95.0

    def test_price_calculation_with_gold_tier(self):
        """Test price calculation with gold tier (10% discount)."""
        from app.services.order import OrderService

        service = OrderService.__new__(OrderService)
        subtotal = 100.0
        discount = service._calculate_loyalty_discount("gold")
        total = subtotal - (subtotal * discount)
        assert total == 90.0
