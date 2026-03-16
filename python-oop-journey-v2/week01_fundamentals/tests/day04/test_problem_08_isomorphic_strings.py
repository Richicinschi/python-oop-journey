"""Tests for Problem 08: Isomorphic Strings."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_08_isomorphic_strings import (
    isomorphic_strings,
)


def test_basic_true_case() -> None:
    """Test basic isomorphic strings."""
    assert isomorphic_strings("egg", "add") is True


def test_basic_false_case() -> None:
    """Test non-isomorphic strings."""
    assert isomorphic_strings("foo", "bar") is False


def test_longer_isomorphic() -> None:
    """Test longer isomorphic strings."""
    assert isomorphic_strings("paper", "title") is True


def test_different_lengths() -> None:
    """Test strings of different lengths."""
    assert isomorphic_strings("ab", "abc") is False


def test_empty_strings() -> None:
    """Test empty strings."""
    assert isomorphic_strings("", "") is True


def test_single_character() -> None:
    """Test single character strings."""
    assert isomorphic_strings("a", "a") is True


def test_one_to_many_mapping() -> None:
    """Test where one character maps to multiple."""
    assert isomorphic_strings("ab", "aa") is False


def test_many_to_one_mapping() -> None:
    """Test where multiple characters map to one."""
    assert isomorphic_strings("aa", "ab") is False


def test_complex_pattern() -> None:
    """Test complex pattern matching."""
    assert isomorphic_strings("abba", "cddc") is True


def test_same_pattern_different_chars() -> None:
    """Test same pattern with different characters."""
    assert isomorphic_strings("abab", "cdcd") is True
