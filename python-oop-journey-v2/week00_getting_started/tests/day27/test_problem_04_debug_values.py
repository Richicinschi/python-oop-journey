"""Tests for Problem 04: Debug Values."""

from __future__ import annotations

from week00_getting_started.solutions.day27.problem_04_debug_values import (
    debug_operations,
)


def test_add_and_multiply() -> None:
    """Test add then multiply operations."""
    result = debug_operations(10, ["add_5", "mul_2"])
    assert result == [("add_5", 15), ("mul_2", 30)]


def test_sub_and_div() -> None:
    """Test subtract then divide operations."""
    result = debug_operations(100, ["sub_20", "div_4"])
    assert result == [("sub_20", 80), ("div_4", 20)]


def test_division_by_zero() -> None:
    """Test division by zero stops execution."""
    result = debug_operations(10, ["add_5", "div_0", "mul_2"])
    assert result == [("add_5", 15)]  # Stops before div_0


def test_single_operation() -> None:
    """Test single operation."""
    result = debug_operations(5, ["mul_3"])
    assert result == [("mul_3", 15)]


def test_empty_operations() -> None:
    """Test empty operations list."""
    result = debug_operations(10, [])
    assert result == []


def test_multiple_operations() -> None:
    """Test multiple operations in sequence."""
    result = debug_operations(10, ["add_10", "sub_5", "mul_2", "div_5"])
    assert result == [
        ("add_10", 20),
        ("sub_5", 15),
        ("mul_2", 30),
        ("div_5", 6),
    ]
