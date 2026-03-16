"""Problem 04: Accumulator - Solution."""

from __future__ import annotations


def accumulate(current_total: float, new_value: float) -> float:
    """Return the new total after adding a value.

    This is a pure function that takes the current total and a new value,
    returning their sum. No external state is modified.

    Args:
        current_total: The running total so far.
        new_value: The new value to add.

    Returns:
        The updated total (current_total + new_value).
    """
    return current_total + new_value


def calculate_average(total: float, count: int) -> float:
    """Calculate the average from a total and count.

    Args:
        total: The sum of all values.
        count: The number of values.

    Returns:
        The average (total / count). Returns 0.0 if count is 0.
    """
    if count == 0:
        return 0.0
    return total / count


def apply_discount(total: float, discount_percent: float) -> float:
    """Apply a percentage discount to a total.

    Args:
        total: The original total amount.
        discount_percent: Discount percentage (e.g., 10.0 for 10%).

    Returns:
        The total after discount is applied.
    """
    discount_multiplier = 1 - (discount_percent / 100)
    return round(total * discount_multiplier, 2)
