"""Tests for Problem 07: Subsets."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_07_subsets import subsets


def test_subsets_empty() -> None:
    """Test subsets of empty list."""
    result = subsets([])
    assert result == [[]]


def test_subsets_single_element() -> None:
    """Test subsets of single element."""
    result = subsets([1])
    assert len(result) == 2
    assert [] in result
    assert [1] in result


def test_subsets_two_elements() -> None:
    """Test subsets of two elements."""
    result = subsets([1, 2])
    assert len(result) == 4
    assert [] in result
    assert [1] in result
    assert [2] in result
    assert [1, 2] in result


def test_subsets_three_elements() -> None:
    """Test subsets of three elements."""
    result = subsets([1, 2, 3])
    assert len(result) == 8
    expected = [
        [],
        [1], [2], [3],
        [1, 2], [1, 3], [2, 3],
        [1, 2, 3]
    ]
    # Sort both lists for comparison
    assert sorted(result, key=lambda x: (len(x), x)) == sorted(expected, key=lambda x: (len(x), x))


def test_subsets_count() -> None:
    """Test that n elements produce 2^n subsets."""
    assert len(subsets([1, 2, 3, 4])) == 16  # 2^4 = 16
    assert len(subsets([1, 2, 3, 4, 5])) == 32  # 2^5 = 32


def test_subsets_strings() -> None:
    """Test subsets with strings."""
    result = subsets(['a', 'b'])
    assert len(result) == 4
    assert [] in result
    assert ['a'] in result
    assert ['b'] in result
    assert ['a', 'b'] in result


def test_subsets_with_duplicates() -> None:
    """Test subsets with duplicate elements."""
    result = subsets([1, 1])
    # Note: With duplicates, we get duplicate subsets
    assert len(result) == 4  # 2^2 = 4, including duplicates
