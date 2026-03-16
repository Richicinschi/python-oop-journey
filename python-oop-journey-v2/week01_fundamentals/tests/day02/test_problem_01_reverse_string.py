"""Tests for Problem 01: Reverse String."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_01_reverse_string import reverse_string


def test_reverse_simple_string() -> None:
    """Test reversing a simple string."""
    assert reverse_string("hello") == "olleh"


def test_reverse_mixed_case() -> None:
    """Test reversing a mixed case string."""
    assert reverse_string("Python") == "nohtyP"


def test_reverse_empty_string() -> None:
    """Test reversing an empty string."""
    assert reverse_string("") == ""


def test_reverse_single_character() -> None:
    """Test reversing a single character."""
    assert reverse_string("a") == "a"


def test_reverse_with_spaces() -> None:
    """Test reversing a string with spaces."""
    assert reverse_string("hello world") == "dlrow olleh"


def test_reverse_with_numbers() -> None:
    """Test reversing a string with numbers."""
    assert reverse_string("abc123") == "321cba"


def test_reverse_palindrome() -> None:
    """Test reversing a palindrome."""
    assert reverse_string("racecar") == "racecar"


def test_reverse_unicode() -> None:
    """Test reversing a string with unicode characters."""
    assert reverse_string("こんにちは") == "はちにんこ"
