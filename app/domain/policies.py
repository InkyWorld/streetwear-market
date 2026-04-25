"""Domain policies for promotions and inventory reservations."""

from datetime import datetime, timedelta, timezone


class PromotionCombinationPolicy:
    """Policy that constrains promotion combination behavior."""

    @staticmethod
    def allow_combination() -> bool:
        """Allow stackable promotions for this practice."""
        return True


class InventoryHoldPolicy:
    """Policy for reservation hold/release lifecycle."""

    HOLD_TTL_MINUTES = 15

    @classmethod
    def expires_at(cls, now: datetime | None = None) -> datetime:
        base_now = now or datetime.now(timezone.utc).replace(tzinfo=None)
        return base_now + timedelta(minutes=cls.HOLD_TTL_MINUTES)
