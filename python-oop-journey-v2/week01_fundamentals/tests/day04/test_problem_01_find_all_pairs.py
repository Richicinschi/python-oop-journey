"""Tests for Problem 01: Find All Pairs."""

from __future__ import annotations

from week01_fundamentals.solutions.day04.problem_01_find_all_pairs import find_all_pairs


def test_basic_case() -> None:
    """Test basic case with multiple valid pairs."""
    result = find_all_pairs([1, 2, 3, 4, 5], 5)
    assert sorted(result) == [(1, 4), (2, 3)]


def test_duplicates() -> None:
    """Test with duplicate values."""
    result = find_all_pairs([1, 1, 1, 1], 2)
    assert result == [(1, 1)]


def test_no_pairs() -> None:
    """Test when no pairs exist."""
    result = find_all_pairs([1, 2, 3], 10)
    assert result == []


def test_empty_list() -> None:
    """Test with empty list."""
    result = find_all_pairs([], 5)
    assert result == []


def test_single_element() -> None:
    """Test with single element."""
    result = find_all_pairs([5], 5)
    assert result == []


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    result = find_all_pairs([-1, 0, 1, 2, -2], 0)
    assert sorted(result) == [(-2, 2), (-1, 1)]


def test_target_zero() -> None:
    """Test with target of zero."""
    result = find_all_pairs([1, -1, 2, -2, 3, -3], 0)
    assert sorted(result) == [(-3, 3), (-2, 2), (-1, 1)]


def test_same_pair_not_duplicated() -> None:
    """Test that same pair is not duplicated."""
    result = find_all_pairs([1, 2, 3, 4, 1, 2, 3, 4], 5)
    assert sorted(result) == [(1, 4), (2, 3)]


def test_multiple_same_value_pairs() -> None:
    """Test with multiple same-value pairs possible."""
    result = find_all_pairs([1, 1, 2, 2, 3, 3], 4)
    assert sorted(result) == [(1, 3), (2, 2)]


def test_large_numbers() -> None:
    """Test with large numbers."""
    result = find_all_pairs([1000000, 2000000, 3000000], 3000000)
    assert result == [(1000000, 2000000)]
