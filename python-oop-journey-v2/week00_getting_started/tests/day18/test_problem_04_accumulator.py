"""Tests for Problem 04: Accumulator."""

from __future__ import annotations

from week00_getting_started.solutions.day18.problem_04_accumulator import (
    accumulate,
    calculate_average,
    apply_discount,
)


def test_accumulate_positive_values() -> None:
    """Test accumulating positive values."""
    total = 0.0
    total = accumulate(total, 10.0)
    assert total == 10.0
    total = accumulate(total, 25.5)
    assert total == 35.5


def test_accumulate_negative_values() -> None:
    """Test accumulating negative values."""
    total = 100.0
    total = accumulate(total, -30.0)
    assert total == 70.0


def test_calculate_average_normal() -> None:
    """Test calculating average with valid count."""
    assert calculate_average(100.0, 4) == 25.0
    assert calculate_average(50.0, 2) == 25.0


def test_calculate_average_zero_count() -> None:
    """Test calculating average with zero count."""
    assert calculate_average(100.0, 0) == 0.0


def test_apply_discount() -> None:
    """Test applying discount."""
    # 10% off $100 = $90
    assert apply_discount(100.0, 10.0) == 90.0
    # 25% off $200 = $150
    assert apply_discount(200.0, 25.0) == 150.0
    # 0% off = no change
    assert apply_discount(100.0, 0.0) == 100.0


def test_workflow_accumulate_and_average() -> None:
    """Test a complete workflow of accumulating and averaging."""
    total = 0.0
    count = 0

    values = [10.0, 20.0, 30.0, 40.0]
    for value in values:
        total = accumulate(total, value)
        count += 1

    assert total == 100.0
    assert count == 4
    assert calculate_average(total, count) == 25.0
