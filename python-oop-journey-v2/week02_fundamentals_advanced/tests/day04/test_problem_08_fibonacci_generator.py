"""Tests for Problem 08: Fibonacci Generator."""

from __future__ import annotations

import itertools

from week02_fundamentals_advanced.solutions.day04.problem_08_fibonacci_generator import (
    fibonacci_generator,
)


def test_first_few_values() -> None:
    """Test the first few Fibonacci numbers."""
    gen = fibonacci_generator()
    assert next(gen) == 0
    assert next(gen) == 1
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 5
    assert next(gen) == 8
    assert next(gen) == 13


def test_islice_first_ten() -> None:
    """Test first 10 Fibonacci numbers using islice."""
    gen = fibonacci_generator()
    first_ten = list(itertools.islice(gen, 10))
    assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fibonacci_sequence_property() -> None:
    """Test that each number is sum of previous two (after first two)."""
    gen = fibonacci_generator()
    values = list(itertools.islice(gen, 20))

    # Check the Fibonacci property
    for i in range(2, len(values)):
        assert values[i] == values[i - 1] + values[i - 2]


def test_generator_is_infinite() -> None:
    """Test that generator can produce many values."""
    gen = fibonacci_generator()
    # Get 100 values - should not raise or hang
    values = list(itertools.islice(gen, 100))
    assert len(values) == 100
    assert values[-1] == 218922995834555169026  # 100th Fibonacci number


def test_multiple_independent_generators() -> None:
    """Test that multiple generators are independent."""
    gen1 = fibonacci_generator()
    gen2 = fibonacci_generator()

    # Advance gen1
    for _ in range(5):
        next(gen1)

    # gen2 should still start at 0
    assert next(gen2) == 0
    assert next(gen2) == 1


def test_lazy_nature() -> None:
    """Test that values are produced on demand."""
    gen = fibonacci_generator()

    # Only get first value, no infinite loop
    first = next(gen)
    assert first == 0

    # Get second
    second = next(gen)
    assert second == 1
