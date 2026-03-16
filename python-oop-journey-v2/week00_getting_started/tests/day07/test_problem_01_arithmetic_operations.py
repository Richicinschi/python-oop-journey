"""Tests for Problem 01."""

from __future__ import annotations

from week00_getting_started.solutions.day07.problem_01_arithmetic_operations import arithmetic_operations


def test_arithmetic() -> None:
    """Test case 1."""
    result = arithmetic_operations(10, 3)
    assert result['sum'] == 13
    assert result['difference'] == 7
    assert result['product'] == 30
    assert result['quotient'] == 3.33


def test_arithmetic_zero() -> None:
    """Test case 2."""
    result = arithmetic_operations(5, 0)
    assert result['quotient'] == 0
