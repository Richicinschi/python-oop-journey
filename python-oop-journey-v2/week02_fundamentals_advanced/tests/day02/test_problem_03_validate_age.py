"""Tests for Problem 03: Validate Age with Custom Exception."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_03_validate_age import (
    InvalidAgeError,
    validate_age,
)


def test_validate_age_valid() -> None:
    """Test valid ages."""
    assert validate_age(1) == 1
    assert validate_age(25) == 25
    assert validate_age(150) == 150
    assert validate_age(100) == 100


def test_validate_age_zero() -> None:
    """Test age zero raises InvalidAgeError."""
    with pytest.raises(InvalidAgeError) as exc_info:
        validate_age(0)
    assert "Age must be between 1 and 150" in str(exc_info.value)
    assert "got 0" in str(exc_info.value)


def test_validate_age_negative() -> None:
    """Test negative age raises InvalidAgeError."""
    with pytest.raises(InvalidAgeError) as exc_info:
        validate_age(-5)
    assert "got -5" in str(exc_info.value)


def test_validate_age_too_high() -> None:
    """Test age above 150 raises InvalidAgeError."""
    with pytest.raises(InvalidAgeError) as exc_info:
        validate_age(151)
    assert "got 151" in str(exc_info.value)
    
    with pytest.raises(InvalidAgeError) as exc_info:
        validate_age(200)
    assert "got 200" in str(exc_info.value)


def test_invalid_age_error_inheritance() -> None:
    """Test InvalidAgeError inherits from ValueError."""
    assert issubclass(InvalidAgeError, ValueError)
    
    with pytest.raises(ValueError):
        validate_age(0)
