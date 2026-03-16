"""Tests for Problem 05: Fix Off By One."""

from __future__ import annotations

from week00_getting_started.solutions.day27.problem_05_fix_off_by_one import sum_evens


def test_sum_evens_to_4() -> None:
    """Test sum of evens from 0 to 4."""
    assert sum_evens(4) == 6  # 0 + 2 + 4


def test_sum_evens_to_5() -> None:
    """Test sum of evens from 0 to 5."""
    assert sum_evens(5) == 6  # 0 + 2 + 4


def test_sum_evens_to_10() -> None:
    """Test sum of evens from 0 to 10."""
    assert sum_evens(10) == 30  # 0 + 2 + 4 + 6 + 8 + 10


def test_sum_evens_to_0() -> None:
    """Test sum of evens to 0."""
    assert sum_evens(0) == 0


def test_sum_evens_to_1() -> None:
    """Test sum of evens to 1."""
    assert sum_evens(1) == 0  # Only 0 is even


def test_sum_evens_to_2() -> None:
    """Test sum of evens to 2."""
    assert sum_evens(2) == 2  # 0 + 2


def test_sum_evens_negative() -> None:
    """Test sum with negative input."""
    assert sum_evens(-5) == 0


def test_sum_evens_large() -> None:
    """Test sum with larger number."""
    assert sum_evens(6) == 12  # 0 + 2 + 4 + 6
