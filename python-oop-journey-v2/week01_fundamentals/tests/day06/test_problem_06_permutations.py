"""Tests for Problem 06: Permutations."""

from __future__ import annotations

from week01_fundamentals.solutions.day06.problem_06_permutations import permutations


def test_permutations_empty() -> None:
    """Test permutations of empty list."""
    result = permutations([])
    assert result == [[]]


def test_permutations_single_element() -> None:
    """Test permutations of single element."""
    result = permutations([1])
    assert len(result) == 1
    assert [1] in result


def test_permutations_two_elements() -> None:
    """Test permutations of two elements."""
    result = permutations([1, 2])
    assert len(result) == 2
    assert sorted(result) == [[1, 2], [2, 1]]


def test_permutations_three_elements() -> None:
    """Test permutations of three elements."""
    result = permutations([1, 2, 3])
    assert len(result) == 6
    expected = [
        [1, 2, 3], [1, 3, 2],
        [2, 1, 3], [2, 3, 1],
        [3, 1, 2], [3, 2, 1]
    ]
    assert sorted(result) == sorted(expected)


def test_permutations_with_duplicates() -> None:
    """Test permutations with duplicate elements."""
    result = permutations([1, 1, 2])
    # Note: With duplicates, we get duplicate permutations
    assert len(result) == 6  # 3! = 6, including duplicates


def test_permutations_strings() -> None:
    """Test permutations with strings."""
    result = permutations(['a', 'b'])
    assert sorted(result) == [['a', 'b'], ['b', 'a']]


def test_permutations_count() -> None:
    """Test that n elements produce n! permutations."""
    assert len(permutations([1, 2, 3, 4])) == 24  # 4! = 24
