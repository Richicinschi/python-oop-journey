"""Tests for Problem 05: Retry Operation."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_05_retry_operation import (
    retry_operation,
)


def test_retry_operation_success_first_try() -> None:
    """Test successful execution on first try."""
    result = retry_operation(lambda: 42, max_attempts=3)
    assert result == 42


def test_retry_operation_eventual_success() -> None:
    """Test retry until success."""
    call_count = 0
    
    def fail_twice() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError(f"Attempt {call_count} failed")
        return "success"
    
    result = retry_operation(fail_twice, max_attempts=5)
    assert result == "success"
    assert call_count == 3


def test_retry_operation_all_failures() -> None:
    """Test that last exception is raised when all attempts fail."""
    call_count = 0
    
    def always_fail() -> str:
        nonlocal call_count
        call_count += 1
        raise ValueError(f"Attempt {call_count}")
    
    with pytest.raises(ValueError) as exc_info:
        retry_operation(always_fail, max_attempts=3)
    
    assert "Attempt 3" in str(exc_info.value)
    assert call_count == 3


def test_retry_operation_max_attempts_one() -> None:
    """Test with max_attempts=1 (no retries)."""
    result = retry_operation(lambda: "ok", max_attempts=1)
    assert result == "ok"


def test_retry_operation_invalid_max_attempts() -> None:
    """Test that max_attempts < 1 raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        retry_operation(lambda: 42, max_attempts=0)
    assert "at least 1" in str(exc_info.value)
    
    with pytest.raises(ValueError):
        retry_operation(lambda: 42, max_attempts=-1)


def test_retry_operation_different_exception_types() -> None:
    """Test retry works with different exception types."""
    call_count = 0
    
    def fail_with_different_errors() -> str:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise TypeError("First error")
        if call_count == 2:
            raise ValueError("Second error")
        return "success"
    
    result = retry_operation(fail_with_different_errors, max_attempts=3)
    assert result == "success"
    assert call_count == 3
