"""Tests for Problem 01: Count Down."""

from __future__ import annotations

from week00_getting_started.solutions.day10.problem_01_count_down import count_down


def test_count_down_positive() -> None:
    """Test counting down from positive numbers."""
    assert count_down(5) == [5, 4, 3, 2, 1]
    assert count_down(3) == [3, 2, 1]
    assert count_down(1) == [1]


def test_count_down_zero() -> None:
    """Test counting down from zero."""
    assert count_down(0) == []


def test_count_down_negative() -> None:
    """Test counting down from negative numbers."""
    assert count_down(-5) == []
    assert count_down(-1) == []


def test_count_down_large() -> None:
    """Test counting down from larger numbers."""
    result = count_down(10)
    assert result[0] == 10
    assert result[-1] == 1
    assert len(result) == 10
