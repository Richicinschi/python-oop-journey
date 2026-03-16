"""Reference solution for Problem 05: Reverse Integer."""

from __future__ import annotations

# 32-bit signed integer limits
INT32_MIN = -2**31
INT32_MAX = 2**31 - 1


def reverse_integer(x: int) -> int:
    """Reverse the digits of a 32-bit signed integer.

    Args:
        x: 32-bit signed integer to reverse

    Returns:
        Reversed integer, or 0 if overflow occurs
    """
    result = 0
    sign = -1 if x < 0 else 1
    x = abs(x)

    while x != 0:
        digit = x % 10
        x //= 10

        # Check for overflow before adding the digit
        if result > (INT32_MAX - digit) // 10:
            return 0

        result = result * 10 + digit

    result *= sign

    # Final bounds check
    if result < INT32_MIN or result > INT32_MAX:
        return 0

    return result
