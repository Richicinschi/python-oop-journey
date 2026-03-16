"""Reference solution for Problem 05: String Utils Module."""

from __future__ import annotations

import re

# Define what should be imported with 'from module import *'
__all__ = [
    "capitalize_words",
    "reverse_words",
    "is_palindrome",
    "count_words",
    "slugify",
]


def _normalize_whitespace(text: str) -> str:
    """Internal helper: Replace multiple spaces with single space, strip ends."""
    return " ".join(text.split())


def _clean_text(text: str) -> str:
    """Internal helper: Remove non-alphanumeric characters, lowercase."""
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()


def capitalize_words(text: str) -> str:
    """Capitalize the first letter of each word.
    
    Args:
        text: Input string
        
    Returns:
        String with each word capitalized
        
    Example:
        >>> capitalize_words("hello world")
        "Hello World"
    """
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())


def reverse_words(text: str) -> str:
    """Reverse the order of words in the text.
    
    Args:
        text: Input string
        
    Returns:
        String with words in reverse order
        
    Example:
        >>> reverse_words("hello world python")
        "python world hello"
    """
    if not text:
        return ""
    return " ".join(reversed(text.split()))


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome (case-insensitive, ignores non-alphanumeric).
    
    Args:
        text: Input string
        
    Returns:
        True if text is a palindrome, False otherwise
        
    Example:
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    if not text:
        return True
    cleaned = _clean_text(text)
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    """Count the number of words in the text.
    
    Words are sequences of non-whitespace characters.
    
    Args:
        text: Input string
        
    Returns:
        Number of words
        
    Example:
        >>> count_words("hello world")
        2
        >>> count_words("")
        0
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.
    
    Converts to lowercase, replaces spaces with hyphens,
    removes non-alphanumeric characters (except hyphens).
    
    Args:
        text: Input string
        
    Returns:
        URL-friendly slug string
        
    Example:
        >>> slugify("Hello World 123!")
        "hello-world-123"
    """
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove non-alphanumeric except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip hyphens from ends
    return text.strip('-')
