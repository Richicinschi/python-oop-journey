"""Tests for Problem 11: Best Time to Buy and Sell Stock."""

from __future__ import annotations

from week01_fundamentals.solutions.day03.problem_11_best_time_to_buy_sell_stock import (
    max_profit,
    max_profit_with_days,
)


def test_example_1() -> None:
    """Test first example from problem."""
    prices = [7, 1, 5, 3, 6, 4]
    assert max_profit(prices) == 5


def test_example_2() -> None:
    """Test second example from problem (decreasing prices)."""
    prices = [7, 6, 4, 3, 1]
    assert max_profit(prices) == 0


def test_single_element() -> None:
    """Test with single element."""
    prices = [5]
    assert max_profit(prices) == 0


def test_two_elements_profit() -> None:
    """Test with two elements where profit is possible."""
    prices = [1, 5]
    assert max_profit(prices) == 4


def test_two_elements_no_profit() -> None:
    """Test with two elements where no profit is possible."""
    prices = [5, 1]
    assert max_profit(prices) == 0


def test_ascending_prices() -> None:
    """Test with ascending prices."""
    prices = [1, 2, 3, 4, 5]
    assert max_profit(prices) == 4  # Buy at 1, sell at 5


def test_descending_prices() -> None:
    """Test with descending prices."""
    prices = [5, 4, 3, 2, 1]
    assert max_profit(prices) == 0


def test_constant_prices() -> None:
    """Test with constant prices."""
    prices = [5, 5, 5, 5, 5]
    assert max_profit(prices) == 0


def test_peak_then_drop() -> None:
    """Test where best profit is before a drop."""
    prices = [3, 2, 6, 5, 0, 3]
    assert max_profit(prices) == 4  # Buy at 2, sell at 6


def test_multiple_peaks() -> None:
    """Test with multiple peaks."""
    prices = [1, 5, 3, 8, 4, 9]
    assert max_profit(prices) == 8  # Buy at 1, sell at 9


def test_large_profit() -> None:
    """Test with large profit."""
    prices = [1, 10000]
    assert max_profit(prices) == 9999


def test_zero_prices() -> None:
    """Test with zero prices."""
    prices = [0, 0, 0, 5]
    assert max_profit(prices) == 5


def test_with_days() -> None:
    """Test the extended version that returns days."""
    prices = [7, 1, 5, 3, 6, 4]
    profit, buy_day, sell_day = max_profit_with_days(prices)
    assert profit == 5
    assert buy_day == 1  # Price 1
    assert sell_day == 4  # Price 6


def test_with_days_no_profit() -> None:
    """Test days version with no profit."""
    prices = [5, 4, 3, 2, 1]
    profit, buy_day, sell_day = max_profit_with_days(prices)
    assert profit == 0
