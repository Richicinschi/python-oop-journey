"""Tests for Problem 09: Word Pattern."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_09_word_pattern import word_pattern


def test_basic_true_case() -> None:
    """Test basic pattern match."""
    assert word_pattern("abba", "dog cat cat dog") is True


def test_basic_false_case() -> None:
    """Test pattern mismatch."""
    assert word_pattern("abba", "dog cat cat fish") is False


def test_one_to_many_words() -> None:
    """Test where pattern letter maps to multiple words."""
    assert word_pattern("aaaa", "dog cat cat dog") is False


def test_many_to_one_pattern() -> None:
    """Test where multiple pattern letters map to same word."""
    assert word_pattern("abba", "dog dog dog dog") is False


def test_different_word_count() -> None:
    """Test when word count doesn't match pattern length."""
    assert word_pattern("aaa", "dog cat") is False


def test_empty_pattern() -> None:
    """Test empty pattern."""
    assert word_pattern("", "") is True


def test_single_pattern() -> None:
    """Test single character pattern."""
    assert word_pattern("a", "dog") is True


def test_complex_pattern() -> None:
    """Test complex pattern matching."""
    assert word_pattern("abcba", "hello world test world hello") is True


def test_case_sensitivity() -> None:
    """Test case sensitivity."""
    assert word_pattern("ab", "Dog dog") is True
    # Words are different by case
    assert word_pattern("ab", "dog dog") is False
