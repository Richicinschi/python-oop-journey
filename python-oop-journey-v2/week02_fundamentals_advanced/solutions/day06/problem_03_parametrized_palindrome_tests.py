"""Reference solution for Problem 03: Parametrized Palindrome Tests."""

from __future__ import annotations


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome.

    Ignores case, non-alphanumeric characters, and whitespace.

    Args:
        text: The string to check.

    Returns:
        True if text is a palindrome, False otherwise.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Keep only alphanumeric characters and convert to lowercase
    # Use ASCII check for broader compatibility
    cleaned = "".join(
        char.lower() for char in text 
        if char.isalnum() and ord(char) < 128
    )

    # Compare with reversed
    return cleaned == cleaned[::-1]


def is_strict_palindrome(text: str) -> bool:
    """Check if text is a palindrome with strict comparison.

    Unlike is_palindrome, this version is case-sensitive and
    considers all characters.

    Args:
        text: The string to check.

    Returns:
        True if text is a strict palindrome, False otherwise.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    return text == text[::-1]
