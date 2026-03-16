"""Tests for Problem 09: Batch Processor with Error Handling."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_09_batch_processor import (
    batch_statistics,
    parse_int_batch,
    process_batch,
    safe_divide_batch,
)


def test_process_batch_all_success() -> None:
    """Test process_batch with all successful items."""
    result = process_batch([1, 2, 3], lambda x: x * 2)
    assert len(result["success"]) == 3
    assert len(result["failed"]) == 0
    assert result["stats"]["success_count"] == 3


def test_process_batch_with_failures() -> None:
    """Test process_batch with some failures."""
    # Use a function that will fail on non-numbers
    def only_numbers(x):
        if not isinstance(x, (int, float)):
            raise TypeError("Only numbers allowed")
        return x * 2
    
    result = process_batch([1, 2, "three", 4], only_numbers)
    assert len(result["success"]) == 3
    assert len(result["failed"]) == 1
    assert result["failed"][0][0] == "three"


def test_process_batch_all_failures() -> None:
    """Test process_batch with all failures."""
    result = process_batch(["a", "b"], lambda x: x * 2)
    # Strings can be multiplied, so this shouldn't fail
    assert len(result["success"]) == 2


def test_process_batch_empty() -> None:
    """Test process_batch with empty list."""
    result = process_batch([], lambda x: x)
    assert result["stats"]["total"] == 0


def test_safe_divide_batch_normal() -> None:
    """Test safe_divide_batch with valid divisor."""
    result = safe_divide_batch([10, 20, 30], 2)
    assert result == [5.0, 10.0, 15.0]


def test_safe_divide_batch_by_zero() -> None:
    """Test safe_divide_batch with divisor of zero."""
    result = safe_divide_batch([10, 20, 30], 0)
    assert result == [None, None, None]


def test_safe_divide_batch_floats() -> None:
    """Test safe_divide_batch with float inputs."""
    result = safe_divide_batch([10.0, 25.0], 2.5)
    assert result == [4.0, 10.0]


def test_parse_int_batch_all_valid() -> None:
    """Test parse_int_batch with all valid strings."""
    result = parse_int_batch(["1", "2", "3"])
    assert result["values"] == [1, 2, 3]
    assert result["failed"] == []
    assert result["indices"] == []


def test_parse_int_batch_with_invalid() -> None:
    """Test parse_int_batch with some invalid strings."""
    result = parse_int_batch(["1", "two", "3", "four"])
    assert result["values"] == [1, 3]
    assert len(result["failed"]) == 2
    assert result["indices"] == [1, 3]


def test_parse_int_batch_empty() -> None:
    """Test parse_int_batch with empty list."""
    result = parse_int_batch([])
    assert result["values"] == []
    assert result["failed"] == []


def test_batch_statistics_full_success() -> None:
    """Test batch_statistics with all successes."""
    results = {
        "stats": {"total": 10, "success_count": 10, "failure_count": 0}
    }
    stats = batch_statistics(results)
    assert stats["success_rate"] == 100.0
    assert stats["failure_rate"] == 0.0


def test_batch_statistics_half_success() -> None:
    """Test batch_statistics with 50% success."""
    results = {
        "stats": {"total": 10, "success_count": 5, "failure_count": 5}
    }
    stats = batch_statistics(results)
    assert stats["success_rate"] == 50.0
    assert stats["failure_rate"] == 50.0


def test_batch_statistics_empty() -> None:
    """Test batch_statistics with empty results."""
    results = {"stats": {}}
    stats = batch_statistics(results)
    assert stats["total"] == 0
