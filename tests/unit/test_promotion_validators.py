"""Unit tests for promotion validators."""

from datetime import UTC, datetime, timedelta

import pytest

from app.domain.exceptions import ValidationError
from app.domain.validators import validate_promotion_window


def test_validate_promotion_window_accepts_valid_range():
    now = datetime.now(UTC).replace(tzinfo=None)
    validate_promotion_window(now, now + timedelta(hours=1))


def test_validate_promotion_window_rejects_equal_bounds():
    now = datetime.now(UTC).replace(tzinfo=None)
    with pytest.raises(ValidationError):
        validate_promotion_window(now, now)


def test_validate_promotion_window_rejects_reversed_bounds():
    now = datetime.now(UTC).replace(tzinfo=None)
    with pytest.raises(ValidationError):
        validate_promotion_window(now + timedelta(hours=1), now)
