"""Tests for Problem 01: Trace Debug."""

from __future__ import annotations

from week00_getting_started.solutions.day27.problem_01_trace_debug import (
    trace_calculation,
)


def test_trace_with_5() -> None:
    """Test tracing calculation with input 5."""
    result = trace_calculation(5)
    assert result == [
        "start: 5",
        "after_add: 10",
        "after_multiply: 20",
        "final: 20",
    ]


def test_trace_with_0() -> None:
    """Test tracing calculation with input 0."""
    result = trace_calculation(0)
    assert result == [
        "start: 0",
        "after_add: 5",
        "after_multiply: 10",
        "final: 10",
    ]


def test_trace_with_negative() -> None:
    """Test tracing calculation with negative input."""
    result = trace_calculation(-3)
    assert result == [
        "start: -3",
        "after_add: 2",
        "after_multiply: 4",
        "final: 4",
    ]


def test_trace_returns_list() -> None:
    """Test that result is a list."""
    result = trace_calculation(1)
    assert isinstance(result, list)
    assert len(result) == 4
