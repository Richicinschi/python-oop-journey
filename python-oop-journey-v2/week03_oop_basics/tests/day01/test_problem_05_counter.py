"""Tests for Problem 05: Counter."""

from __future__ import annotations

from week03_oop_basics.solutions.day01.problem_05_counter import Counter


def test_counter_default_start() -> None:
    """Test counter with default start value."""
    counter = Counter()
    assert counter.get_count() == 0


def test_counter_custom_start() -> None:
    """Test counter with custom start value."""
    counter = Counter(10)
    assert counter.get_count() == 10


def test_counter_increment() -> None:
    """Test incrementing the counter."""
    counter = Counter()
    result = counter.increment()
    assert result == 1
    assert counter.get_count() == 1


def test_counter_multiple_increments() -> None:
    """Test multiple increments."""
    counter = Counter()
    counter.increment()
    counter.increment()
    counter.increment()
    assert counter.get_count() == 3


def test_counter_decrement() -> None:
    """Test decrementing the counter."""
    counter = Counter(5)
    result = counter.decrement()
    assert result == 4
    assert counter.get_count() == 4


def test_counter_increment_decrement() -> None:
    """Test alternating increment and decrement."""
    counter = Counter()
    counter.increment()
    counter.increment()
    counter.decrement()
    assert counter.get_count() == 1


def test_counter_reset() -> None:
    """Test resetting the counter."""
    counter = Counter(5)
    counter.increment()
    counter.increment()
    counter.reset()
    assert counter.get_count() == 5


def test_counter_reset_to_zero() -> None:
    """Test resetting counter that started at 0."""
    counter = Counter()
    counter.increment()
    counter.increment()
    counter.reset()
    assert counter.get_count() == 0


def test_counter_negative_values() -> None:
    """Test counter can go negative."""
    counter = Counter(0)
    counter.decrement()
    counter.decrement()
    assert counter.get_count() == -2


def test_increment_returns_new_value() -> None:
    """Test that increment returns the new count."""
    counter = Counter(10)
    assert counter.increment() == 11
    assert counter.increment() == 12


def test_decrement_returns_new_value() -> None:
    """Test that decrement returns the new count."""
    counter = Counter(10)
    assert counter.decrement() == 9
    assert counter.decrement() == 8


def test_str_representation() -> None:
    """Test the __str__ method."""
    counter = Counter(5)
    result = str(counter)
    assert "5" in result


def test_repr_representation() -> None:
    """Test the __repr__ method."""
    counter = Counter(5)
    result = repr(counter)
    assert "Counter" in result
