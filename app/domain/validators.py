"""Domain validators for promotions and reservations."""

from datetime import datetime

from app.domain.exceptions import ValidationError


def validate_promotion_window(active_from: datetime | None, active_to: datetime | None) -> None:
    """Validate promotion dates."""
    if active_from and active_to and active_from >= active_to:
        raise ValidationError("Promotion active_from must be before active_to")


def validate_release_transition(current_status: str) -> None:
    """Validate that reservation can be released."""
    if current_status not in {"held"}:
        raise ValidationError(f"Reservation with status '{current_status}' cannot be released")
