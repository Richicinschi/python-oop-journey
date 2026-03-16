"""Tests for Problem 01: Flatten Nested List."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_01_flatten_nested_list import (
    flatten_nested_list,
)


def test_basic_flattening() -> None:
    """Test basic nested list flattening."""
    nested = [[1, 2], [3, 4], [5, 6]]
    assert flatten_nested_list(nested) == [1, 2, 3, 4, 5, 6]


def test_empty_sublists() -> None:
    """Test with empty sublists."""
    nested = [[1], [], [2, 3], [], [4]]
    assert flatten_nested_list(nested) == [1, 2, 3, 4]


def test_all_empty_sublists() -> None:
    """Test with all empty sublists."""
    nested = [[], [], []]
    assert flatten_nested_list(nested) == []


def test_empty_list() -> None:
    """Test with empty outer list."""
    assert flatten_nested_list([]) == []


def test_single_element_sublists() -> None:
    """Test with single-element sublists."""
    nested = [[1], [2], [3]]
    assert flatten_nested_list(nested) == [1, 2, 3]


def test_varied_length_sublists() -> None:
    """Test with sublists of varying lengths."""
    nested = [[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]]
    assert flatten_nested_list(nested) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    nested = [[-1, -2], [3, -4], [5]]
    assert flatten_nested_list(nested) == [-1, -2, 3, -4, 5]


def test_zeros() -> None:
    """Test with zeros."""
    nested = [[0, 0], [0], [0, 0, 0]]
    assert flatten_nested_list(nested) == [0, 0, 0, 0, 0, 0]


def test_large_numbers() -> None:
    """Test with large numbers."""
    nested = [[1000000, 2000000], [3000000]]
    assert flatten_nested_list(nested) == [1000000, 2000000, 3000000]


def test_preserves_order() -> None:
    """Test that order within and across sublists is preserved."""
    nested = [[3, 1, 4], [1, 5], [9, 2, 6]]
    assert flatten_nested_list(nested) == [3, 1, 4, 1, 5, 9, 2, 6]
