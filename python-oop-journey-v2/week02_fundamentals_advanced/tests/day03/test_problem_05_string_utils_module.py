"""Tests for Problem 05: String Utils Module."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day03.problem_05_string_utils_module import (
    capitalize_words,
    reverse_words,
    is_palindrome,
    count_words,
    slugify,
)


def test_capitalize_words_basic() -> None:
    """Test basic capitalize_words."""
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("python") == "Python"


def test_capitalize_words_multiple() -> None:
    """Test capitalize_words with multiple words."""
    assert capitalize_words("the quick brown fox") == "The Quick Brown Fox"


def test_capitalize_words_empty() -> None:
    """Test capitalize_words with empty string."""
    assert capitalize_words("") == ""


def test_reverse_words_basic() -> None:
    """Test basic reverse_words."""
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("a b c") == "c b a"


def test_reverse_words_single() -> None:
    """Test reverse_words with single word."""
    assert reverse_words("hello") == "hello"


def test_reverse_words_empty() -> None:
    """Test reverse_words with empty string."""
    assert reverse_words("") == ""


def test_is_palindrome_basic() -> None:
    """Test basic is_palindrome."""
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False


def test_is_palindrome_case_insensitive() -> None:
    """Test is_palindrome is case insensitive."""
    assert is_palindrome("Racecar") is True
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_with_punctuation() -> None:
    """Test is_palindrome ignores non-alphanumeric."""
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("Was it a car or a cat I saw?") is True


def test_is_palindrome_empty() -> None:
    """Test empty string is considered palindrome."""
    assert is_palindrome("") is True


def test_count_words_basic() -> None:
    """Test basic count_words."""
    assert count_words("hello world") == 2
    assert count_words("one two three four") == 4


def test_count_words_single() -> None:
    """Test count_words with single word."""
    assert count_words("hello") == 1


def test_count_words_empty() -> None:
    """Test count_words with empty string."""
    assert count_words("") == 0
    assert count_words("   ") == 0


def test_count_words_multiple_spaces() -> None:
    """Test count_words handles multiple spaces."""
    assert count_words("hello    world") == 2


def test_slugify_basic() -> None:
    """Test basic slugify."""
    assert slugify("Hello World") == "hello-world"


def test_slugify_lowercase() -> None:
    """Test slugify converts to lowercase."""
    assert slugify("HELLO WORLD") == "hello-world"


def test_slugify_removes_special_chars() -> None:
    """Test slugify removes special characters."""
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("Test@#$%123") == "test123"


def test_slugify_multiple_spaces() -> None:
    """Test slugify handles multiple spaces."""
    assert slugify("Hello    World") == "hello-world"


def test_slugify_empty() -> None:
    """Test slugify with empty string."""
    assert slugify("") == ""


def test_slugify_with_numbers() -> None:
    """Test slugify preserves numbers."""
    assert slugify("Hello World 123") == "hello-world-123"
