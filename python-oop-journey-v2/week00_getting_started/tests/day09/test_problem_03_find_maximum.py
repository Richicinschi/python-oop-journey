"""Tests for Problem 03: Find Maximum."""

from __future__ import annotations

from week00_getting_started.solutions.day09.problem_03_find_maximum import find_maximum


def test_find_maximum_first() -> None:
    """Test when first number is maximum."""
    assert find_maximum(5, 2, 3) == 5
    assert find_maximum(10, 5, 5) == 10
    assert find_maximum(100, 1, 1) == 100


def test_find_maximum_second() -> None:
    """Test when second number is maximum."""
    assert find_maximum(2, 5, 3) == 5
    assert find_maximum(1, 10, 1) == 10
    assert find_maximum(5, 100, 50) == 100


def test_find_maximum_third() -> None:
    """Test when third number is maximum."""
    assert find_maximum(1, 2, 3) == 3
    assert find_maximum(5, 5, 10) == 10
    assert find_maximum(1, 1, 100) == 100


def test_find_maximum_ties() -> None:
    """Test with ties."""
    assert find_maximum(5, 5, 3) == 5
    assert find_maximum(5, 3, 5) == 5
    assert find_maximum(3, 5, 5) == 5
    assert find_maximum(5, 5, 5) == 5


def test_find_maximum_negative() -> None:
    """Test with negative numbers."""
    assert find_maximum(-1, -5, -3) == -1
    assert find_maximum(-10, -5, -20) == -5
    assert find_maximum(-1, -1, -5) == -1


def test_find_maximum_floats() -> None:
    """Test with floats."""
    assert find_maximum(1.5, 2.5, 3.5) == 3.5
    assert find_maximum(3.14, 2.71, 1.41) == 3.14
