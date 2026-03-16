"""Problem 05: String Utils Module

Topic: Module organization, __all__
Difficulty: Easy

Create a utility module for string operations. Define multiple helper
functions and properly control the public API using __all__.

Requirements:
    - Implement various string utility functions
    - Define __all__ to control what gets imported with 'from module import *'
    - Include internal helper functions (prefixed with _) that are not exported
    - Functions should handle edge cases gracefully

Functions to implement (in __all__):
    - capitalize_words(text): Capitalize first letter of each word
    - reverse_words(text): Reverse the order of words
    - is_palindrome(text): Check if text reads same forwards/backwards (case-insensitive, ignores non-alphanumeric)
    - count_words(text): Count number of words in text
    - slugify(text): Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric

Internal helpers (not in __all__):
    - _normalize_whitespace(text): Remove extra whitespace
    - _clean_text(text): Remove non-alphanumeric characters

Example:
    from problem_05_string_utils_module import capitalize_words, slugify
    
    capitalize_words("hello world")  # "Hello World"
    slugify("Hello World 123!")      # "hello-world-123"
    is_palindrome("A man, a plan, a canal: Panama")  # True
"""

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
    raise NotImplementedError("Implement _normalize_whitespace")


def _clean_text(text: str) -> str:
    """Internal helper: Remove non-alphanumeric characters, lowercase."""
    raise NotImplementedError("Implement _clean_text")


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
    raise NotImplementedError("Implement capitalize_words")


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
    raise NotImplementedError("Implement reverse_words")


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
    raise NotImplementedError("Implement is_palindrome")


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
    raise NotImplementedError("Implement count_words")


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
    raise NotImplementedError("Implement slugify")
