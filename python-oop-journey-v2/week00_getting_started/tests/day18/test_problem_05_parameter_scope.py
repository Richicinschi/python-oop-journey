"""Tests for Problem 05: Parameter Scope."""

from __future__ import annotations

from week00_getting_started.solutions.day18.problem_05_parameter_scope import (
    double_value,
    triple_in_place,
    get_final_value,
)


def test_double_value() -> None:
    """Test doubling values."""
    assert double_value(5) == 10
    assert double_value(0) == 0
    assert double_value(-3) == -6


def test_triple_in_place() -> None:
    """Test tripling list elements in place."""
    numbers = [1, 2, 3]
    triple_in_place(numbers)
    assert numbers == [3, 6, 9]

    numbers = [0, 5, 10]
    triple_in_place(numbers)
    assert numbers == [0, 15, 30]


def test_triple_in_place_empty_list() -> None:
    """Test tripling an empty list."""
    numbers: list[int] = []
    triple_in_place(numbers)
    assert numbers == []


def test_get_final_value_with_additions() -> None:
    """Test get_final_value with addition operations."""
    assert get_final_value(0, ["+", "+", "+"]) == 3
    assert get_final_value(10, ["+"]) == 11


def test_get_final_value_with_subtractions() -> None:
    """Test get_final_value with subtraction operations."""
    assert get_final_value(5, ["-", "-"]) == 3
    assert get_final_value(0, ["-"]) == -1


def test_get_final_value_with_multiplications() -> None:
    """Test get_final_value with multiplication operations."""
    assert get_final_value(2, ["*"]) == 4
    assert get_final_value(3, ["*", "*"]) == 12  # 3 * 2 * 2


def test_get_final_value_mixed() -> None:
    """Test get_final_value with mixed operations."""
    # Start with 5, +1 = 6, *2 = 12, -1 = 11
    assert get_final_value(5, ["+", "*", "-"]) == 11
