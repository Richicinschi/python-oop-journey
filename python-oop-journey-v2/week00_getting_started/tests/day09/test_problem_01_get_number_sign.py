"""Tests for Problem 01: Get Number Sign."""

from __future__ import annotations

from week00_getting_started.solutions.day09.problem_01_get_number_sign import get_number_sign


def test_get_number_sign_positive() -> None:
    """Test positive numbers."""
    assert get_number_sign(5) == "positive"
    assert get_number_sign(1) == "positive"
    assert get_number_sign(100) == "positive"
    assert get_number_sign(0.5) == "positive"


def test_get_number_sign_negative() -> None:
    """Test negative numbers."""
    assert get_number_sign(-5) == "negative"
    assert get_number_sign(-1) == "negative"
    assert get_number_sign(-100) == "negative"
    assert get_number_sign(-0.5) == "negative"


def test_get_number_sign_zero() -> None:
    """Test zero."""
    assert get_number_sign(0) == "zero"
    assert get_number_sign(0.0) == "zero"
