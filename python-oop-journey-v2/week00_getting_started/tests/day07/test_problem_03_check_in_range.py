"""Tests for Problem 03."""

from __future__ import annotations

from week00_getting_started.solutions.day07.problem_03_check_in_range import check_in_range


def test_in_range() -> None:
    """Test case 1."""
    assert check_in_range(5, 1, 10) is True
    assert check_in_range(1, 1, 10) is True
    assert check_in_range(10, 1, 10) is True


def test_out_of_range() -> None:
    """Test case 2."""
    assert check_in_range(0, 1, 10) is False
    assert check_in_range(11, 1, 10) is False
