"""Reference solution for Problem 03: String Utilities Module."""

from __future__ import annotations
import re


def reverse(text: str) -> str:
    """Reverse the input string.

    Args:
        text: The string to reverse

    Returns:
        The reversed string
    """
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome (ignoring case and non-alphanumeric).

    Args:
        text: The string to check

    Returns:
        True if palindrome, False otherwise
    """
    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    """Count the number of words in a text.

    Words are separated by whitespace.

    Args:
        text: The input text

    Returns:
        Number of words
    """
    return len(text.split())


def to_snake_case(text: str) -> str:
    """Convert text to snake_case.

    Handles CamelCase and space-separated text.

    Examples:
        "HelloWorld" -> "hello_world"
        "hello world" -> "hello_world"
        "someVariableName" -> "some_variable_name"

    Args:
        text: The text to convert

    Returns:
        snake_case version of the text
    """
    # Insert underscore before uppercase letters (except first)
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Replace spaces with underscores and lowercase
    return s2.replace(" ", "_").lower()


def truncate(text: str, max_length: int) -> str:
    """Truncate text to max_length, adding ellipsis if truncated.

    Args:
        text: The text to truncate
        max_length: Maximum allowed length (including "..." if truncated)

    Returns:
        Truncated text with "..." if it was too long
    """
    if len(text) <= max_length:
        return text
    if max_length <= 3:
        return text[:max_length]
    return text[: max_length - 3] + "..."
