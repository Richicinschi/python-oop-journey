"""Tests for Problem 04: Even Square Map."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_04_even_square_map import (
    even_square_map,
)


def test_basic_case() -> None:
    """Test basic case with mixed even and odd."""
    numbers = [1, 2, 3, 4, 5, 6]
    assert even_square_map(numbers) == [4, 16, 36]


def test_all_odd() -> None:
    """Test with all odd numbers."""
    numbers = [1, 3, 5, 7, 9]
    assert even_square_map(numbers) == []


def test_all_even() -> None:
    """Test with all even numbers."""
    numbers = [2, 4, 6, 8]
    assert even_square_map(numbers) == [4, 16, 36, 64]


def test_empty_list() -> None:
    """Test with empty list."""
    assert even_square_map([]) == []


def test_single_even() -> None:
    """Test with single even number."""
    assert even_square_map([4]) == [16]


def test_single_odd() -> None:
    """Test with single odd number."""
    assert even_square_map([3]) == []


def test_negative_numbers() -> None:
    """Test with negative even numbers."""
    numbers = [-2, -3, -4, 5]
    assert even_square_map(numbers) == [4, 16]


def test_zero() -> None:
    """Test with zero (which is even)."""
    numbers = [0, 1, 2]
    assert even_square_map(numbers) == [0, 4]


def test_preserves_order() -> None:
    """Test that output order matches input order."""
    numbers = [6, 2, 4, 3, 8]
    assert even_square_map(numbers) == [36, 4, 16, 64]


def test_large_numbers() -> None:
    """Test with large numbers."""
    numbers = [1000, 1001, 2000]
    assert even_square_map(numbers) == [1000000, 4000000]
