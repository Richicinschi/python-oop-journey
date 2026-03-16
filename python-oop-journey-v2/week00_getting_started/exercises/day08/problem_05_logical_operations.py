"""Problem 05: Logical Operations

Topic: Boolean Logic, Logical Operators
Difficulty: Easy

Write functions that demonstrate logical operations.

Examples:
    >>> logical_and(True, True)
    True
    >>> logical_and(True, False)
    False
    >>> logical_or(False, True)
    True
    >>> logical_or(False, False)
    False
    >>> logical_not(True)
    False
    >>> logical_not(False)
    True
    >>> logical_xor(True, True)
    False
    >>> logical_xor(True, False)
    True

Requirements:
    - Implement and, or, not, xor operations
    - Use Python's logical operators: and, or, not
    - XOR is True when exactly one operand is True
"""

from __future__ import annotations


def logical_and(a: bool, b: bool) -> bool:
    """Return the result of a AND b.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if both a and b are True, False otherwise
    """
    raise NotImplementedError("Implement logical_and")


def logical_or(a: bool, b: bool) -> bool:
    """Return the result of a OR b.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if at least one of a or b is True, False otherwise
    """
    raise NotImplementedError("Implement logical_or")


def logical_not(a: bool) -> bool:
    """Return the result of NOT a.

    Args:
        a: Boolean to negate

    Returns:
        True if a is False, False if a is True
    """
    raise NotImplementedError("Implement logical_not")


def logical_xor(a: bool, b: bool) -> bool:
    """Return the result of a XOR b (exclusive or).

    XOR is True when exactly one of a or b is True.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if exactly one of a or b is True, False otherwise
    """
    raise NotImplementedError("Implement logical_xor")
