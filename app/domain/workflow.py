"""Domain workflow validators for order status transitions."""

from app.domain.enums import OrderStatus
from app.domain.exceptions import ValidationError


class OrderWorkflowValidator:
    """Validator for order status workflow transitions."""

    @staticmethod
    def validate_transition(current_status: str, new_status: str) -> None:
        """
        Validate that a status transition is allowed.

        Args:
            current_status: Current order status
            new_status: Desired new status

        Raises:
            ValidationError: If transition is not allowed
        """
        try:
            current = OrderStatus(current_status)
        except ValueError:
            raise ValidationError(f"Invalid current status: {current_status}")

        try:
            new = OrderStatus(new_status)
        except ValueError:
            raise ValidationError(f"Invalid new status: {new_status}")

        if not current.can_transition_to(new):
            valid_transitions = current.get_valid_transitions(current)
            valid_str = (
                ", ".join([s.value for s in valid_transitions]) if valid_transitions else "none"
            )
            raise ValidationError(
                f"Cannot transition from '{current_status}' to '{new_status}'. "
                f"Valid transitions from '{current_status}': {valid_str}"
            )

    @staticmethod
    def get_valid_transitions(current_status: str) -> list[str]:
        """Get list of valid next statuses for a given current status."""
        try:
            status = OrderStatus(current_status)
            return [s.value for s in status.get_valid_transitions(status)]
        except ValueError:
            return []
