"""Tests for Problem 10: Lazy Filter Map."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day04.problem_10_lazy_filter_map import (
    lazy_filter_map,
)


def test_basic_filter_map() -> None:
    """Test basic filter and map pipeline."""
    data = [1, 2, 3, 4, 5, 6]
    pred = lambda x: x % 2 == 0
    trans = lambda x: x * x
    result = list(lazy_filter_map(data, pred, trans))
    assert result == [4, 16, 36]


def test_filter_all() -> None:
    """Test when all elements pass filter."""
    data = [2, 4, 6]
    pred = lambda x: x > 0
    trans = lambda x: x * 2
    result = list(lazy_filter_map(data, pred, trans))
    assert result == [4, 8, 12]


def test_filter_none() -> None:
    """Test when no elements pass filter."""
    data = [1, 3, 5]
    pred = lambda x: x % 2 == 0
    trans = lambda x: x * x
    result = list(lazy_filter_map(data, pred, trans))
    assert result == []


def test_empty_data() -> None:
    """Test with empty data."""
    result = list(lazy_filter_map([], lambda x: True, lambda x: x))
    assert result == []


def test_single_element_passes() -> None:
    """Test with single element that passes filter."""
    data = [5]
    pred = lambda x: x > 3
    trans = lambda x: x + 10
    result = list(lazy_filter_map(data, pred, trans))
    assert result == [15]


def test_single_element_fails() -> None:
    """Test with single element that fails filter."""
    data = [2]
    pred = lambda x: x > 5
    trans = lambda x: x * 2
    result = list(lazy_filter_map(data, pred, trans))
    assert result == []


def test_negative_numbers() -> None:
    """Test with negative numbers."""
    data = [-3, -2, -1, 0, 1, 2, 3]
    pred = lambda x: x < 0
    trans = lambda x: abs(x)
    result = list(lazy_filter_map(data, pred, trans))
    assert result == [3, 2, 1]


def test_string_transformation() -> None:
    """Test with string data."""
    data = ["hello", "hi", "world", "a"]
    pred = lambda x: len(x) > 2
    trans = lambda x: x.upper()
    result = list(lazy_filter_map(data, pred, trans))
    assert result == ["HELLO", "WORLD"]


def test_lazy_evaluation() -> None:
    """Test that pipeline evaluates lazily."""
    data = [1, 2, 3, 4, 5, 6]
    pred = lambda x: x % 2 == 0
    trans = lambda x: x * x

    gen = lazy_filter_map(data, pred, trans)

    # Get values one at a time
    assert next(gen) == 4   # 2 squared
    assert next(gen) == 16  # 4 squared
    assert next(gen) == 36  # 6 squared

    try:
        next(gen)
        assert False, "Generator should be exhausted"
    except StopIteration:
        pass


def test_chained_operations() -> None:
    """Test that operations are chained correctly."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # First pipeline: even numbers -> square
    result1 = list(lazy_filter_map(data, lambda x: x % 2 == 0, lambda x: x * x))
    assert result1 == [4, 16, 36, 64, 100]

    # Second pipeline: > 5 -> double
    result2 = list(lazy_filter_map(data, lambda x: x > 5, lambda x: x * 2))
    assert result2 == [12, 14, 16, 18, 20]


def test_type_conversion() -> None:
    """Test type conversion in transformation."""
    data = [1, 2, 3, 4]
    pred = lambda x: x > 2
    trans = lambda x: str(x)
    result = list(lazy_filter_map(data, pred, trans))
    assert result == ["3", "4"]
