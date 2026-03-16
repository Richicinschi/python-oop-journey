"""Tests for Problem 04: Get Sign."""

from __future__ import annotations

from week00_getting_started.solutions.day16.problem_04_get_sign import get_sign


def test_get_sign_with_positive_numbers() -> None:
    """Test with positive numbers."""
    assert get_sign(1) == "positive"
    assert get_sign(100) == "positive"
    assert get_sign(999) == "positive"


def test_get_sign_with_negative_numbers() -> None:
    """Test with negative numbers."""
    assert get_sign(-1) == "negative"
    assert get_sign(-100) == "negative"
    assert get_sign(-999) == "negative"


def test_get_sign_with_zero() -> None:
    """Test with zero."""
    assert get_sign(0) == "zero"
