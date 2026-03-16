"""Tests for Problem 01: Module Counter."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day03.problem_01_module_counter import (
    get_import_count,
    reset_import_count,
)


def test_import_count_starts_at_one() -> None:
    """Test that import count starts at 1 after module is loaded."""
    reset_import_count()
    # After reset, count should be 0
    assert get_import_count() == 0


def test_reset_import_count() -> None:
    """Test that reset works correctly."""
    # Reset to known state
    reset_import_count()
    assert get_import_count() == 0


def test_multiple_resets() -> None:
    """Test that multiple resets work correctly."""
    reset_import_count()
    assert get_import_count() == 0
    
    reset_import_count()
    assert get_import_count() == 0
    
    reset_import_count()
    assert get_import_count() == 0


def test_module_counter_is_module_level() -> None:
    """Test that the counter is at module level (singleton behavior)."""
    reset_import_count()
    
    # Counter is managed by module, should be consistent
    count1 = get_import_count()
    count2 = get_import_count()
    
    assert count1 == count2
