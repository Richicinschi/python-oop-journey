"""Tests for Problem 05."""

from __future__ import annotations

from week00_getting_started.solutions.day07.problem_05_calculate_remainder_and_quotient import calculate_remainder_and_quotient


def test_division() -> None:
    """Test case 1."""
    result = calculate_remainder_and_quotient(17, 5)
    assert result['quotient'] == 3
    assert result['remainder'] == 2


def test_exact_division() -> None:
    """Test case 2."""
    result = calculate_remainder_and_quotient(20, 4)
    assert result['quotient'] == 5
    assert result['remainder'] == 0


def test_divide_by_one() -> None:
    """Test case 3."""
    result = calculate_remainder_and_quotient(7, 1)
    assert result['quotient'] == 7
    assert result['remainder'] == 0
