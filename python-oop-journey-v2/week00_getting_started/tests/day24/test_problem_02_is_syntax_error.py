"""Tests for Problem 02: Is Syntax Error."""

from __future__ import annotations

from week00_getting_started.solutions.day24.problem_02_is_syntax_error import (
    is_syntax_error,
)


def test_syntax_error_true() -> None:
    """Test that SyntaxError is identified correctly."""
    assert is_syntax_error("SyntaxError") is True


def test_indentation_error_true() -> None:
    """Test that IndentationError is identified correctly."""
    assert is_syntax_error("IndentationError") is True


def test_zero_division_false() -> None:
    """Test that ZeroDivisionError is not a syntax error."""
    assert is_syntax_error("ZeroDivisionError") is False


def test_name_error_false() -> None:
    """Test that NameError is not a syntax error."""
    assert is_syntax_error("NameError") is False


def test_type_error_false() -> None:
    """Test that TypeError is not a syntax error."""
    assert is_syntax_error("TypeError") is False


def test_value_error_false() -> None:
    """Test that ValueError is not a syntax error."""
    assert is_syntax_error("ValueError") is False
