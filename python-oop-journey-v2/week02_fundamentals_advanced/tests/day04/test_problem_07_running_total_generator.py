"""Tests for Problem 07: Running Total Generator."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_07_running_total_generator import (
    running_total_generator,
)


def test_basic_running_total() -> None:
    """Test basic running total."""
    numbers = [1, 2, 3, 4]
    assert list(running_total_generator(numbers)) == [1, 3, 6, 10]


def test_with_negatives() -> None:
    """Test with negative numbers."""
    numbers = [5, -2, 7]
    assert list(running_total_generator(numbers)) == [5, 3, 10]


def test_all_negatives() -> None:
    """Test with all negative numbers."""
    numbers = [-1, -2, -3]
    assert list(running_total_generator(numbers)) == [-1, -3, -6]


def test_empty_list() -> None:
    """Test with empty list."""
    assert list(running_total_generator([])) == []


def test_single_element() -> None:
    """Test with single element."""
    assert list(running_total_generator([42])) == [42]


def test_zeros() -> None:
    """Test with zeros."""
    numbers = [0, 0, 1, 0]
    assert list(running_total_generator(numbers)) == [0, 0, 1, 1]


def test_large_numbers() -> None:
    """Test with large numbers."""
    numbers = [1000000, 2000000, 3000000]
    assert list(running_total_generator(numbers)) == [1000000, 3000000, 6000000]


def test_lazy_evaluation() -> None:
    """Test that generator evaluates lazily (one at a time)."""
    numbers = [1, 2, 3, 4, 5]
    gen = running_total_generator(numbers)

    # Get values one by one
    assert next(gen) == 1
    assert next(gen) == 3
    assert next(gen) == 6
    assert next(gen) == 10
    assert next(gen) == 15

    # Generator is exhausted
    try:
        next(gen)
        assert False, "Generator should be exhausted"
    except StopIteration:
        pass


def test_generator_can_be_consumed_multiple_times() -> None:
    """Test that creating new generator works each time."""
    numbers = [1, 2, 3]
    # Each call creates a fresh generator
    assert list(running_total_generator(numbers)) == [1, 3, 6]
    assert list(running_total_generator(numbers)) == [1, 3, 6]
