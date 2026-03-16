"""Tests for Problem 01: Local vs Global."""

from __future__ import annotations

from week00_getting_started.solutions.day18 import problem_01_local_vs_global as scope_module


def test_get_local_message() -> None:
    """Test that get_local_message returns the correct local value."""
    result = scope_module.get_local_message()
    assert result == "Hello from local"


def test_get_global_message() -> None:
    """Test that get_global_message reads the global correctly."""
    result = scope_module.get_global_message()
    assert result == "Hello from global"


def test_global_unchanged() -> None:
    """Test that functions don't modify the global variable."""
    original = scope_module.global_message
    scope_module.get_local_message()
    scope_module.get_global_message()
    assert scope_module.global_message == original


def test_local_does_not_affect_global() -> None:
    """Test that local variable creation doesn't affect global."""
    # Call multiple times to ensure consistency
    for _ in range(3):
        local = scope_module.get_local_message()
        global_msg = scope_module.get_global_message()
        assert local == "Hello from local"
        assert global_msg == "Hello from global"
        assert local != global_msg
