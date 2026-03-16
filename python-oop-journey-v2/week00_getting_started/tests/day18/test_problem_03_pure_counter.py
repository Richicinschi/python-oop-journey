"""Tests for Problem 03: Pure Counter."""

from __future__ import annotations

from week00_getting_started.solutions.day18.problem_03_pure_counter import (
    increment_counter,
    decrement_counter,
    reset_counter,
)


def test_increment_with_default_step() -> None:
    """Test increment with default step of 1."""
    assert increment_counter(0) == 1
    assert increment_counter(5) == 6
    assert increment_counter(100) == 101


def test_increment_with_custom_step() -> None:
    """Test increment with custom step."""
    assert increment_counter(0, 5) == 5
    assert increment_counter(10, 10) == 20
    assert increment_counter(100, 50) == 150


def test_decrement_with_default_step() -> None:
    """Test decrement with default step of 1."""
    assert decrement_counter(10) == 9
    assert decrement_counter(1) == 0
    assert decrement_counter(100) == 99


def test_decrement_with_custom_step() -> None:
    """Test decrement with custom step."""
    assert decrement_counter(10, 5) == 5
    assert decrement_counter(100, 25) == 75
    assert decrement_counter(0, 5) == -5


def test_reset_counter() -> None:
    """Test reset counter returns 0."""
    assert reset_counter() == 0


def test_counter_workflow() -> None:
    """Test a typical counter workflow."""
    counter = reset_counter()  # 0
    counter = increment_counter(counter)  # 1
    counter = increment_counter(counter, 5)  # 6
    counter = decrement_counter(counter)  # 5
    counter = decrement_counter(counter, 3)  # 2
    assert counter == 2
