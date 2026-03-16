"""Problem 03: Parametrized Palindrome Tests

Topic: Using @pytest.mark.parametrize
Difficulty: Easy

Write parametrized tests for palindrome checking functions.

Your task:
    1. Implement the is_palindrome function
    2. Create parametrized tests for multiple test cases
    3. Test both palindromes and non-palindromes

A palindrome reads the same forwards and backwards, ignoring:
    - Case (A == a)
    - Non-alphanumeric characters
    - Whitespace

Examples:
    >>> is_palindrome("radar")
    True
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("")
    True
"""

from __future__ import annotations


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome.

    Ignores case, non-alphanumeric characters, and whitespace.

    Args:
        text: The string to check.

    Returns:
        True if text is a palindrome, False otherwise.

    Examples:
        >>> is_palindrome("radar")
        True
        >>> is_palindrome("Radar")
        True
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("")
        True
    """
    # TODO: Implement palindrome checking
    raise NotImplementedError("Implement is_palindrome")


def is_strict_palindrome(text: str) -> bool:
    """Check if text is a palindrome with strict comparison.

    Unlike is_palindrome, this version is case-sensitive and
    considers all characters.

    Args:
        text: The string to check.

    Returns:
        True if text is a strict palindrome, False otherwise.

    Examples:
        >>> is_strict_palindrome("radar")
        True
        >>> is_strict_palindrome("Radar")
        False
        >>> is_strict_palindrome("a man a plan a canal panama")
        True
    """
    # TODO: Implement strict palindrome checking
    raise NotImplementedError("Implement is_strict_palindrome")


# TODO: Create parametrized tests using @pytest.mark.parametrize
# Test cases should include:
# - Simple palindromes: "radar", "level", "madam"
# - Phrases: "A man, a plan, a canal: Panama"
# - Numbers: "12321", "123321"
# - Edge cases: "", "a", "ab"
# - Non-palindromes: "hello", "python"
