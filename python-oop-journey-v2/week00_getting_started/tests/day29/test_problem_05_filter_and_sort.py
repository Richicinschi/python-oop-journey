"""Tests for Problem 05: Filter and Sort Mixed Data."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_05_filter_and_sort import (
    filter_by_type,
    find_extremes,
    group_by_type,
    sort_mixed_numbers,
)


def test_filter_by_type_int() -> None:
    """Test filter_by_type for integers."""
    data = [1, "hello", 3.5, "world", 2, None]
    result = filter_by_type(data, int)
    assert result == [1, 2]


def test_filter_by_type_str() -> None:
    """Test filter_by_type for strings."""
    data = [1, "hello", 3.5, "world", 2, None]
    result = filter_by_type(data, str)
    assert result == ["hello", "world"]


def test_filter_by_type_empty() -> None:
    """Test filter_by_type with empty list."""
    assert filter_by_type([], int) == []


def test_sort_mixed_numbers_basic() -> None:
    """Test sort_mixed_numbers with mixed data."""
    data = [3, "hello", 1.5, "world", 2, None, 4.0]
    result = sort_mixed_numbers(data)
    assert result == [1.5, 2, 3, 4.0]


def test_sort_mixed_numbers_empty() -> None:
    """Test sort_mixed_numbers with no numbers."""
    assert sort_mixed_numbers(["hello", "world"]) == []


def test_sort_mixed_numbers_all_numbers() -> None:
    """Test sort_mixed_numbers with all numbers."""
    data = [3, 1.5, 2, 4.0]
    result = sort_mixed_numbers(data)
    assert result == [1.5, 2, 3, 4.0]


def test_find_extremes_basic() -> None:
    """Test find_extremes with mixed data."""
    data = [3, "hello", 1.5, "world", 2, None, 4.0]
    min_val, max_val = find_extremes(data)
    assert min_val == 1.5
    assert max_val == 4.0


def test_find_extremes_no_numbers() -> None:
    """Test find_extremes with no numbers."""
    min_val, max_val = find_extremes(["hello", "world", None])
    assert min_val is None
    assert max_val is None


def test_find_extremes_negative_numbers() -> None:
    """Test find_extremes with negative numbers."""
    min_val, max_val = find_extremes([-10, 5, -5, 10])
    assert min_val == -10
    assert max_val == 10


def test_group_by_type_mixed() -> None:
    """Test group_by_type with mixed data."""
    data = [1, "hello", 3.5, "world", 2, None, 4.0]
    result = group_by_type(data)
    assert result["int"] == [1, 2]
    assert result["str"] == ["hello", "world"]
    assert result["float"] == [3.5, 4.0]
    assert result["NoneType"] == [None]


def test_group_by_type_empty() -> None:
    """Test group_by_type with empty list."""
    assert group_by_type([]) == {}


def test_group_by_type_single_type() -> None:
    """Test group_by_type with single type."""
    data = [1, 2, 3]
    result = group_by_type(data)
    assert result == {"int": [1, 2, 3]}
