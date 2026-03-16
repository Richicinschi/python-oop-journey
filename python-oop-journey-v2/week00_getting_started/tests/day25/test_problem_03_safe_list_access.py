"""Tests for Problem 03: Safe List Access."""

from __future__ import annotations

from week00_getting_started.solutions.day25.problem_03_safe_list_access import safe_get


def test_valid_index() -> None:
    """Test accessing valid index."""
    assert safe_get([1, 2, 3], 0) == 1
    assert safe_get([1, 2, 3], 1) == 2
    assert safe_get([1, 2, 3], 2) == 3


def test_index_out_of_range() -> None:
    """Test out of range index returns None."""
    assert safe_get([1, 2, 3], 10) is None
    assert safe_get([1, 2, 3], -10) is None


def test_empty_list() -> None:
    """Test accessing empty list."""
    assert safe_get([], 0) is None


def test_not_a_list() -> None:
    """Test accessing non-list returns None."""
    assert safe_get("string", 0) is None
    assert safe_get(123, 0) is None
    assert safe_get(None, 0) is None


def test_tuple_access() -> None:
    """Test accessing tuple (should work)."""
    assert safe_get((1, 2, 3), 1) == 2
