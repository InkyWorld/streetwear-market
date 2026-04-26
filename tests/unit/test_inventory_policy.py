"""Unit tests for inventory hold policy."""

from datetime import UTC, datetime, timedelta

from app.domain.policies import InventoryHoldPolicy


def test_hold_expiration_uses_policy_ttl():
    now = datetime.now(UTC).replace(tzinfo=None, microsecond=0)
    expires = InventoryHoldPolicy.expires_at(now)
    assert expires - now == timedelta(minutes=InventoryHoldPolicy.HOLD_TTL_MINUTES)
