"""Tests for Problem 02: Generate Range."""

from __future__ import annotations

from week00_getting_started.solutions.day19.problem_02_generate_range import (
    get_numbers_up_to,
    get_numbers_between,
    get_even_numbers_up_to,
    get_countdown,
)


def test_get_numbers_up_to() -> None:
    """Test generating numbers up to n."""
    assert get_numbers_up_to(5) == [0, 1, 2, 3, 4]
    assert get_numbers_up_to(0) == []
    assert get_numbers_up_to(1) == [0]


def test_get_numbers_between() -> None:
    """Test generating numbers between start and end."""
    assert get_numbers_between(2, 6) == [2, 3, 4, 5]
    assert get_numbers_between(0, 3) == [0, 1, 2]
    assert get_numbers_between(5, 5) == []


def test_get_even_numbers_up_to() -> None:
    """Test generating even numbers up to n."""
    assert get_even_numbers_up_to(10) == [0, 2, 4, 6, 8]
    assert get_even_numbers_up_to(5) == [0, 2, 4]
    assert get_even_numbers_up_to(0) == []
    assert get_even_numbers_up_to(1) == [0]


def test_get_countdown() -> None:
    """Test generating countdown."""
    assert get_countdown(5) == [5, 4, 3, 2, 1]
    assert get_countdown(3) == [3, 2, 1]
    assert get_countdown(1) == [1]
