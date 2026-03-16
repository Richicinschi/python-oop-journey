"""Tests for Problem 09: Timer Context Manager."""

from __future__ import annotations

import time

from week02_fundamentals_advanced.solutions.day01.problem_09_timer_context import Timer


def test_timer_records_elapsed_time() -> None:
    """Test that timer records elapsed time."""
    with Timer() as timer:
        time.sleep(0.05)  # 50ms
    
    assert timer.elapsed >= 0.05
    assert timer.elapsed < 0.5  # Should be much less than 500ms


def test_timer_returns_self() -> None:
    """Test that __enter__ returns the timer instance."""
    timer = Timer()
    with timer as t:
        assert t is timer


def test_timer_elapsed_before_exit() -> None:
    """Test that elapsed is 0 before exiting context."""
    timer = Timer()
    with timer:
        assert timer.elapsed == 0.0


def test_timer_records_time_with_exception() -> None:
    """Test that timer records time even when exception occurs."""
    timer = Timer()
    
    try:
        with timer:
            time.sleep(0.05)
            raise ValueError("Test exception")
    except ValueError:
        pass
    
    assert timer.elapsed >= 0.05


def test_timer_precision() -> None:
    """Test that timer uses high precision counter."""
    with Timer() as timer:
        time.sleep(0.01)  # 10ms
    
    # Should have sub-second precision
    assert timer.elapsed > 0
    assert timer.elapsed < 1.0


def test_timer_multiple_uses() -> None:
    """Test that timer can be reused."""
    timer = Timer()
    
    with timer:
        time.sleep(0.01)
    first_elapsed = timer.elapsed
    
    with timer:
        time.sleep(0.02)
    second_elapsed = timer.elapsed
    
    # Second measurement should be larger
    assert second_elapsed > first_elapsed or second_elapsed >= 0.02
