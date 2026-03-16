"""Tests for Problem 05."""

from __future__ import annotations

from week00_getting_started.solutions.day04.problem_05_unpack_and_sum import unpack_and_sum


def test_unpack_sum() -> None:
    """Test case 1."""
    assert unpack_and_sum((1, 2, 3)) == 6
    assert unpack_and_sum((10, 20, 30)) == 60


def test_unpack_zeros() -> None:
    """Test case 2."""
    assert unpack_and_sum((0, 0, 0)) == 0


def test_unpack_negatives() -> None:
    """Test case 3."""
    assert unpack_and_sum((-1, -2, -3)) == -6
    assert unpack_and_sum((-5, 10, -3)) == 2
