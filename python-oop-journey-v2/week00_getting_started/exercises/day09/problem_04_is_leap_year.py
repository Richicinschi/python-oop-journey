"""Problem 04: Is Leap Year

Topic: If Statements, Complex conditions
Difficulty: Easy

Write a function that determines if a year is a leap year.

Leap year rules:
    - Divisible by 4: leap year
    - Except if divisible by 100: not leap year
    - Unless also divisible by 400: leap year

Examples:
    >>> is_leap_year(2000)
    True
    >>> is_leap_year(1900)
    False
    >>> is_leap_year(2020)
    True
    >>> is_leap_year(2021)
    False
    >>> is_leap_year(1600)
    True
    >>> is_leap_year(1700)
    False

Requirements:
    - Implement the leap year algorithm correctly
    - Use modulo operator (%) for divisibility checks
"""

from __future__ import annotations


def is_leap_year(year: int) -> bool:
    """Determine if a year is a leap year.

    Args:
        year: The year to check

    Returns:
        True if year is a leap year, False otherwise
    """
    raise NotImplementedError("Implement is_leap_year")
