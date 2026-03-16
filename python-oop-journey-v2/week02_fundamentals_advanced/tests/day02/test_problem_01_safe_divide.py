"""Tests for Problem 01: Safe Divide."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_01_safe_divide import (
    safe_divide,
)


def test_safe_divide_normal() -> None:
    """Test normal division."""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 2) == 3.5
    assert safe_divide(100, 4) == 25.0


def test_safe_divide_by_zero() -> None:
    """Test division by zero returns error message."""
    result = safe_divide(10, 0)
    assert result == "Error: Division by zero"
    assert isinstance(result, str)


def test_safe_divide_zero_dividend() -> None:
    """Test zero as dividend."""
    assert safe_divide(0, 5) == 0.0
    assert safe_divide(0, 100) == 0.0


def test_safe_divide_negative_numbers() -> None:
    """Test division with negative numbers."""
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
    assert safe_divide(-10, -2) == 5.0


def test_safe_divide_float_inputs() -> None:
    """Test division with float inputs."""
    assert safe_divide(7.5, 2.5) == 3.0
    assert safe_divide(10.0, 4.0) == 2.5


def test_safe_divide_mixed_types() -> None:
    """Test division with mixed int and float."""
    assert safe_divide(10, 2.5) == 4.0
    assert safe_divide(7.5, 3) == 2.5
