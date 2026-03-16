"""Tests for Problem 05: Max of Three."""

from __future__ import annotations

from week00_getting_started.solutions.day16.problem_05_max_of_three import max_of_three


def test_max_first() -> None:
    """Test when the first number is maximum."""
    assert max_of_three(10, 5, 3) == 10
    assert max_of_three(5, 3, 1) == 5


def test_max_second() -> None:
    """Test when the second number is maximum."""
    assert max_of_three(3, 10, 5) == 10
    assert max_of_three(1, 5, 3) == 5


def test_max_third() -> None:
    """Test when the third number is maximum."""
    assert max_of_three(3, 5, 10) == 10
    assert max_of_three(1, 3, 5) == 5


def test_all_equal() -> None:
    """Test when all numbers are equal."""
    assert max_of_three(5, 5, 5) == 5


def test_two_equal_max() -> None:
    """Test when two numbers are equal and maximum."""
    assert max_of_three(5, 5, 3) == 5
    assert max_of_three(5, 3, 5) == 5
    assert max_of_three(3, 5, 5) == 5


def test_with_negative_numbers() -> None:
    """Test with negative numbers."""
    assert max_of_three(-1, -5, -3) == -1
    assert max_of_three(-10, -5, -20) == -5
