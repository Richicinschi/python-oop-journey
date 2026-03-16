"""Reference solution for Problem 06: Is Happy Number."""

from __future__ import annotations


def is_happy_number(n: int) -> bool:
    """Determine if a number is a happy number.

    Args:
        n: A positive integer.

    Returns:
        True if n is a happy number, False otherwise.
    """
    if n <= 0:
        return False

    def get_next(num: int) -> int:
        """Calculate sum of squares of digits."""
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    # Use Floyd's Cycle Detection (tortoise and hare)
    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)           # Move one step
        fast = get_next(get_next(fast))  # Move two steps

    return fast == 1
