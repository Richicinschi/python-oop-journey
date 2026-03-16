"""Tests for Problem 03: Is Even."""

from __future__ import annotations

from week00_getting_started.solutions.day16.problem_03_is_even import is_even


def test_is_even_with_positive_even_numbers() -> None:
    """Test with positive even numbers."""
    assert is_even(2) is True
    assert is_even(4) is True
    assert is_even(100) is True


def test_is_even_with_positive_odd_numbers() -> None:
    """Test with positive odd numbers."""
    assert is_even(1) is False
    assert is_even(3) is False
    assert is_even(99) is False


def test_is_even_with_zero() -> None:
    """Test with zero."""
    assert is_even(0) is True


def test_is_even_with_negative_numbers() -> None:
    """Test with negative numbers."""
    assert is_even(-2) is True
    assert is_even(-4) is True
    assert is_even(-1) is False
    assert is_even(-3) is False
