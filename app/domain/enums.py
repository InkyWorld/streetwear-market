"""Domain enums for Order workflow and Customer loyalty."""

from enum import Enum


class OrderStatus(str, Enum):
    """Order status enum with valid workflow states."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    @classmethod
    def get_valid_transitions(cls, current_status: "OrderStatus") -> list["OrderStatus"]:
        """Get valid next statuses for a given current status."""
        transitions = {
            cls.PENDING: [cls.CONFIRMED, cls.CANCELLED],
            cls.CONFIRMED: [cls.SHIPPED, cls.CANCELLED],
            cls.SHIPPED: [cls.DELIVERED],
            cls.DELIVERED: [],
            cls.CANCELLED: [],
        }
        return transitions.get(current_status, [])

    def can_transition_to(self, new_status: "OrderStatus") -> bool:
        """Check if transition to new status is valid."""
        return new_status in self.get_valid_transitions(self)


class LoyaltyTier(str, Enum):
    """Customer loyalty tier enum for pricing."""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    def get_discount_percentage(self) -> float:
        """Get discount percentage for this tier."""
        discounts = {
            self.BRONZE: 0.0,
            self.SILVER: 0.05,  # 5% discount
            self.GOLD: 0.10,  # 10% discount
        }
        return discounts.get(self, 0.0)
