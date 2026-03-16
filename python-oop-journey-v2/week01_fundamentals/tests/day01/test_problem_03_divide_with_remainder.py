"""Tests for Problem 03: Divide with Remainder."""

from __future__ import annotations

import pytest

from week01_fundamentals.solutions.day01.problem_03_divide_with_remainder import divide_with_remainder


def test_basic_division() -> None:
    """Test basic division with remainder."""
    assert divide_with_remainder(10, 3) == (3, 1)
    assert divide_with_remainder(17, 5) == (3, 2)


def test_exact_division() -> None:
    """Test division with no remainder."""
    assert divide_with_remainder(20, 4) == (5, 0)
    assert divide_with_remainder(100, 10) == (10, 0)


def test_division_by_one() -> None:
    """Test division by 1."""
    assert divide_with_remainder(42, 1) == (42, 0)


def test_zero_dividend() -> None:
    """Test when dividend is zero."""
    assert divide_with_remainder(0, 5) == (0, 0)


def test_negative_dividend() -> None:
    """Test with negative dividend."""
    assert divide_with_remainder(-10, 3) == (-4, 2)


def test_negative_divisor() -> None:
    """Test with negative divisor."""
    assert divide_with_remainder(10, -3) == (-4, -2)


def test_both_negative() -> None:
    """Test with both numbers negative."""
    assert divide_with_remainder(-10, -3) == (3, -1)


def test_divide_by_zero() -> None:
    """Test that dividing by zero raises an exception."""
    with pytest.raises(ZeroDivisionError):
        divide_with_remainder(10, 0)
