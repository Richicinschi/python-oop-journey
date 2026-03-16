"""Reference solution for Problem 05: Logical Operations."""

from __future__ import annotations


def logical_and(a: bool, b: bool) -> bool:
    """Return the result of a AND b.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if both a and b are True, False otherwise
    """
    return a and b


def logical_or(a: bool, b: bool) -> bool:
    """Return the result of a OR b.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if at least one of a or b is True, False otherwise
    """
    return a or b


def logical_not(a: bool) -> bool:
    """Return the result of NOT a.

    Args:
        a: Boolean to negate

    Returns:
        True if a is False, False if a is True
    """
    return not a


def logical_xor(a: bool, b: bool) -> bool:
    """Return the result of a XOR b (exclusive or).

    XOR is True when exactly one of a or b is True.

    Args:
        a: First boolean
        b: Second boolean

    Returns:
        True if exactly one of a or b is True, False otherwise
    """
    return a != b
