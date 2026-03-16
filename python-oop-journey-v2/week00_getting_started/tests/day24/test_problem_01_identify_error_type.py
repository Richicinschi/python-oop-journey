"""Tests for Problem 01: Identify Error Type."""

from __future__ import annotations

from week00_getting_started.solutions.day24.problem_01_identify_error_type import (
    identify_error,
)


def test_identify_zero_division() -> None:
    """Test division by zero scenario."""
    assert identify_error("division_by_zero") == "ZeroDivisionError"


def test_identify_name_error() -> None:
    """Test undefined variable scenario."""
    assert identify_error("undefined_variable") == "NameError"


def test_identify_type_error() -> None:
    """Test wrong type scenario."""
    assert identify_error("wrong_type") == "TypeError"


def test_identify_index_error() -> None:
    """Test index too big scenario."""
    assert identify_error("index_too_big") == "IndexError"


def test_identify_key_error() -> None:
    """Test key not found scenario."""
    assert identify_error("key_not_found") == "KeyError"


def test_identify_value_error() -> None:
    """Test invalid conversion scenario."""
    assert identify_error("invalid_conversion") == "ValueError"
