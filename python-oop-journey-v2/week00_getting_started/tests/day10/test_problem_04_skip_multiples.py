"""Tests for Problem 04: Skip Multiples."""

from __future__ import annotations

from week00_getting_started.solutions.day10.problem_04_skip_multiples import skip_multiples


def test_skip_multiples_basic() -> None:
    """Test basic skip multiples."""
    # 1+2+4+5+7+8+10 = 37 (skip 3, 6, 9)
    assert skip_multiples(10, 3) == 37


def test_skip_multiples_even() -> None:
    """Test skipping even numbers."""
    # 1+3+5+7+9 = 25 (skip even)
    assert skip_multiples(10, 2) == 25


def test_skip_multiples_no_matches() -> None:
    """Test when no multiples to skip."""
    # 1+2+3+4+5 = 15 (no multiples of 10)
    assert skip_multiples(5, 10) == 15


def test_skip_multiples_all_skipped() -> None:
    """Test when all numbers are skipped."""
    # All multiples of 1, sum = 0
    assert skip_multiples(5, 1) == 0


def test_skip_multiples_skip_one() -> None:
    """Test skipping multiples of 1 (everything)."""
    # 2+3+4+5+... (skip 1)
    assert skip_multiples(5, 1) == 0


def test_skip_multiples_single() -> None:
    """Test with single number."""
    assert skip_multiples(1, 2) == 1  # 1 is not multiple of 2
    assert skip_multiples(1, 1) == 0  # 1 is multiple of 1
