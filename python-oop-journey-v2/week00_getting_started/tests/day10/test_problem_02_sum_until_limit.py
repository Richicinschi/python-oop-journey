"""Tests for Problem 02: Sum Until Limit."""

from __future__ import annotations

from week00_getting_started.solutions.day10.problem_02_sum_until_limit import sum_until_limit


def test_sum_until_limit_exact() -> None:
    """Test when sum exactly equals limit."""
    assert sum_until_limit(10) == (4, 10)  # 1+2+3+4=10
    assert sum_until_limit(15) == (5, 15)  # 1+2+3+4+5=15
    assert sum_until_limit(1) == (1, 1)    # 1=1
    assert sum_until_limit(3) == (2, 3)    # 1+2=3


def test_sum_until_limit_below() -> None:
    """Test when sum stays below limit."""
    assert sum_until_limit(4) == (2, 3)    # 1+2=3, next would be 6
    assert sum_until_limit(5) == (2, 3)    # 1+2=3, next would be 6
    assert sum_until_limit(8) == (3, 6)    # 1+2+3=6, next would be 10


def test_sum_until_limit_zero() -> None:
    """Test with zero limit."""
    assert sum_until_limit(0) == (0, 0)


def test_sum_until_limit_negative() -> None:
    """Test with negative limit."""
    assert sum_until_limit(-5) == (0, 0)
