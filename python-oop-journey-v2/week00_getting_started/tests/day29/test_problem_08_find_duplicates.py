"""Tests for Problem 08: Find Duplicates Efficiently."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_08_find_duplicates import (
    count_duplicates,
    find_duplicates,
    find_first_duplicate,
    remove_duplicates_keep_order,
)


def test_find_duplicates_basic() -> None:
    """Test find_duplicates with basic case."""
    assert find_duplicates([1, 2, 3, 2, 4, 3, 5]) == {2, 3}


def test_find_duplicates_no_duplicates() -> None:
    """Test find_duplicates with no duplicates."""
    assert find_duplicates([1, 2, 3, 4, 5]) == set()


def test_find_duplicates_empty() -> None:
    """Test find_duplicates with empty list."""
    assert find_duplicates([]) == set()


def test_find_duplicates_all_same() -> None:
    """Test find_duplicates with all same values."""
    assert find_duplicates([1, 1, 1, 1]) == {1}


def test_find_duplicates_strings() -> None:
    """Test find_duplicates with strings."""
    assert find_duplicates(["a", "b", "a", "c", "b"]) == {"a", "b"}


def test_find_first_duplicate_basic() -> None:
    """Test find_first_duplicate with basic case."""
    assert find_first_duplicate([1, 2, 3, 2, 4, 3]) == 2


def test_find_first_duplicate_no_duplicates() -> None:
    """Test find_first_duplicate with no duplicates."""
    assert find_first_duplicate([1, 2, 3, 4, 5]) is None


def test_find_first_duplicate_empty() -> None:
    """Test find_first_duplicate with empty list."""
    assert find_first_duplicate([]) is None


def test_find_first_duplicate_later() -> None:
    """Test find_first_duplicate finds earliest duplicate."""
    assert find_first_duplicate([1, 2, 3, 1, 2]) == 1


def test_count_duplicates_basic() -> None:
    """Test count_duplicates with basic case."""
    result = count_duplicates([1, 2, 2, 3, 3, 3])
    assert result == {2: 2, 3: 3}


def test_count_duplicates_no_duplicates() -> None:
    """Test count_duplicates with no duplicates."""
    assert count_duplicates([1, 2, 3]) == {}


def test_count_duplicates_includes_count() -> None:
    """Test count_duplicates returns correct counts."""
    result = count_duplicates(["a", "a", "a", "b", "b"])
    assert result["a"] == 3
    assert result["b"] == 2


def test_remove_duplicates_keep_order_basic() -> None:
    """Test remove_duplicates_keep_order with basic case."""
    assert remove_duplicates_keep_order([1, 2, 1, 3, 2, 4]) == [1, 2, 3, 4]


def test_remove_duplicates_keep_order_no_duplicates() -> None:
    """Test remove_duplicates_keep_order with no duplicates."""
    assert remove_duplicates_keep_order([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_remove_duplicates_keep_order_empty() -> None:
    """Test remove_duplicates_keep_order with empty list."""
    assert remove_duplicates_keep_order([]) == []


def test_remove_duplicates_keep_order_preserves_first() -> None:
    """Test remove_duplicates_keep_order preserves first occurrence."""
    result = remove_duplicates_keep_order([3, 1, 2, 1, 3, 4])
    assert result == [3, 1, 2, 4]
    assert result[0] == 3  # First 3 is kept


def test_remove_duplicates_keep_order_strings() -> None:
    """Test remove_duplicates_keep_order with strings."""
    assert remove_duplicates_keep_order(["a", "b", "a", "c"]) == ["a", "b", "c"]
