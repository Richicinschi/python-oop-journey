"""Reference solution for Problem 04: Is Leap Year."""

from __future__ import annotations


def is_leap_year(year: int) -> bool:
    """Determine if a year is a leap year.

    Args:
        year: The year to check

    Returns:
        True if year is a leap year, False otherwise
    """
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False
