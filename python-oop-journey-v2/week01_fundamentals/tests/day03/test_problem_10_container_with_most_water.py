"""Tests for Problem 10: Container With Most Water."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_10_container_with_most_water import (
    max_area,
)


def test_example_1() -> None:
    """Test first example from problem."""
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    assert max_area(height) == 49


def test_example_2() -> None:
    """Test second example from problem."""
    height = [1, 1]
    assert max_area(height) == 1


def test_ascending() -> None:
    """Test with ascending heights."""
    height = [1, 2, 3, 4, 5]
    assert max_area(height) == 6  # (4-0) * min(1,5) = 4, but best is (3-1)*min(2,4)=4
    # Actually: positions 1 and 4: (4-1) * min(2,5) = 3*2 = 6


def test_descending() -> None:
    """Test with descending heights."""
    height = [5, 4, 3, 2, 1]
    assert max_area(height) == 6  # positions 0 and 3: (3-0) * min(5,2) = 3*2 = 6


def test_same_height() -> None:
    """Test with all same heights."""
    height = [5, 5, 5, 5, 5]
    assert max_area(height) == 20  # (4-0) * 5 = 20


def test_zero_height() -> None:
    """Test with zero height."""
    height = [0, 0, 0, 0]
    assert max_area(height) == 0


def test_mixed_with_zero() -> None:
    """Test with mixed heights including zero."""
    height = [0, 2, 0, 2]
    assert max_area(height) == 4  # positions 1 and 3: (3-1) * min(2,2) = 4


def test_two_elements() -> None:
    """Test with two elements."""
    height = [5, 10]
    assert max_area(height) == 5  # (1-0) * min(5,10) = 5


def test_peak_in_middle() -> None:
    """Test with peak in middle."""
    height = [1, 2, 100, 2, 1]
    assert max_area(height) == 4  # positions 0 and 4: (4-0) * min(1,1) = 4
    # Actually positions 1 and 3: (3-1) * min(2,2) = 4
    # Or positions 0 and 2: (2-0) * min(1,100) = 2


def test_large_gap() -> None:
    """Test where best container is not at ends."""
    height = [1, 8, 6, 2, 5, 4, 8, 25, 7]
    # Positions 1 (height 8) and 7 (height 25): width = 6, height = 8, area = 48
    # Positions 0 (height 1) and 7 (height 25): width = 7, height = 1, area = 7
    # Positions 1 (height 8) and 8 (height 7): width = 7, height = 7, area = 49
    # Best is positions 1 and 8: area = 49
    assert max_area(height) == 49
