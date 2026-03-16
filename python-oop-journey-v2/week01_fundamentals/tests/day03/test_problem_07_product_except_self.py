"""Tests for Problem 07: Product of Array Except Self."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_07_product_except_self import (
    product_except_self,
)


def test_example_1() -> None:
    """Test first example from problem."""
    nums = [1, 2, 3, 4]
    assert product_except_self(nums) == [24, 12, 8, 6]


def test_example_2() -> None:
    """Test second example from problem (with zero)."""
    nums = [-1, 1, 0, -3, 3]
    assert product_except_self(nums) == [0, 0, 9, 0, 0]


def test_two_elements() -> None:
    """Test with two elements."""
    nums = [2, 3]
    assert product_except_self(nums) == [3, 2]


def test_with_zero() -> None:
    """Test with single zero."""
    nums = [1, 2, 0, 4]
    assert product_except_self(nums) == [0, 0, 8, 0]


def test_with_two_zeros() -> None:
    """Test with two zeros."""
    nums = [1, 0, 2, 0]
    assert product_except_self(nums) == [0, 0, 0, 0]


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    nums = [-1, -2, -3, -4]
    assert product_except_self(nums) == [-24, -12, -8, -6]


def test_mixed_signs() -> None:
    """Test with mixed positive and negative."""
    nums = [1, -1, 2, -2]
    # For [1, -1, 2, -2]:
    # result[0] = (-1) * 2 * (-2) = 4
    # result[1] = 1 * 2 * (-2) = -4
    # result[2] = 1 * (-1) * (-2) = 2
    # result[3] = 1 * (-1) * 2 = -2
    assert product_except_self(nums) == [4, -4, 2, -2]


def test_all_ones() -> None:
    """Test with all ones."""
    nums = [1, 1, 1, 1]
    assert product_except_self(nums) == [1, 1, 1, 1]


def test_large_values() -> None:
    """Test with larger values."""
    nums = [2, 3, 5, 7]
    # Expected: [105, 70, 42, 30]
    assert product_except_self(nums) == [105, 70, 42, 30]


def test_three_elements() -> None:
    """Test with three elements."""
    nums = [5, 6, 7]
    assert product_except_self(nums) == [42, 35, 30]
