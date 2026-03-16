"""Problem 06: Is Happy Number

Topic: While loops, cycle detection, digit manipulation
Difficulty: Medium

Write a function to determine if a number n is "happy".

A happy number is defined by the following process:
- Starting with any positive integer, replace the number by the sum of 
  the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), 
  or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Example: 19 is happy because:
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
"""

from __future__ import annotations


def is_happy_number(n: int) -> bool:
    """Determine if a number is a happy number.

    Args:
        n: A positive integer.

    Returns:
        True if n is a happy number, False otherwise.

    Example:
        >>> is_happy_number(19)
        True
        >>> is_happy_number(2)
        False
        >>> is_happy_number(1)
        True
    """
    raise NotImplementedError("Implement is_happy_number")
