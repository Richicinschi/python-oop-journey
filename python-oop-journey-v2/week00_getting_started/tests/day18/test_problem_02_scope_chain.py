"""Tests for Problem 02: Scope Chain."""

from __future__ import annotations

from week00_getting_started.solutions.day18 import problem_02_scope_chain as scope_module


def test_outer_function_returns_enclosing() -> None:
    """Test that outer_function returns 'enclosing' from inner function."""
    result = scope_module.outer_function()
    assert result == "enclosing"


def test_read_global_returns_global() -> None:
    """Test that read_global returns the global value."""
    result = scope_module.read_global()
    assert result == "global"


def test_global_unchanged() -> None:
    """Test that global level is unchanged after function calls."""
    original = scope_module.level
    scope_module.outer_function()
    scope_module.read_global()
    assert scope_module.level == original
