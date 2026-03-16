"""Tests for Problem 03: Valid Anagram."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_03_is_anagram import is_anagram


def test_valid_anagram() -> None:
    """Test valid anagram."""
    assert is_anagram("anagram", "nagaram") is True


def test_not_anagram() -> None:
    """Test non-anagram strings."""
    assert is_anagram("rat", "car") is False


def test_empty_strings() -> None:
    """Test two empty strings."""
    assert is_anagram("", "") is True


def test_different_lengths() -> None:
    """Test strings with different lengths."""
    assert is_anagram("a", "ab") is False


def test_single_character_same() -> None:
    """Test single same character."""
    assert is_anagram("a", "a") is True


def test_single_character_different() -> None:
    """Test single different characters."""
    assert is_anagram("a", "b") is False


def test_case_sensitive() -> None:
    """Test case sensitivity - uppercase != lowercase."""
    assert is_anagram("A", "a") is False


def test_repeated_characters() -> None:
    """Test strings with repeated characters."""
    assert is_anagram("aab", "baa") is True


def test_same_string() -> None:
    """Test identical strings."""
    assert is_anagram("hello", "hello") is True


def test_unicode_characters() -> None:
    """Test unicode characters."""
    assert is_anagram("こんにちは", "はちにんこ") is True
