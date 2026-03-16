"""Tests for Problem 05: Guess Number Pattern."""

from __future__ import annotations

from week00_getting_started.solutions.day10.problem_05_guess_number_pattern import guess_number_pattern


def test_guess_number_found() -> None:
    """Test when target is found."""
    assert guess_number_pattern([5, 10, 15, 20], 15, 5) == (3, True)
    assert guess_number_pattern([1, 2, 3], 1, 5) == (1, True)
    assert guess_number_pattern([5], 5, 1) == (1, True)


def test_guess_number_not_found_exhausted() -> None:
    """Test when guesses exhausted without finding."""
    assert guess_number_pattern([1, 2, 3], 5, 5) == (3, False)
    assert guess_number_pattern([10, 20], 15, 5) == (2, False)


def test_guess_number_max_attempts() -> None:
    """Test when max attempts reached before finding."""
    assert guess_number_pattern([5, 10, 15, 20], 20, 2) == (2, False)
    assert guess_number_pattern([1, 2, 3, 4, 5], 5, 3) == (3, False)


def test_guess_number_first_attempt() -> None:
    """Test when found on first attempt."""
    assert guess_number_pattern([5, 10, 15], 5, 5) == (1, True)


def test_guess_number_empty() -> None:
    """Test with empty guesses."""
    assert guess_number_pattern([], 5, 5) == (0, False)


def test_guess_number_zero_attempts() -> None:
    """Test with zero max attempts."""
    assert guess_number_pattern([1, 2, 3], 1, 0) == (0, False)
