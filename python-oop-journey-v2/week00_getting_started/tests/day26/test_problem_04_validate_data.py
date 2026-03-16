"""Tests for Problem 04: Validate Data."""

from __future__ import annotations

from week00_getting_started.solutions.day26.problem_04_validate_data import (
    validate_data,
)


def test_valid_data() -> None:
    """Test valid data returns empty list."""
    data = {"name": "Alice", "age": "30", "email": "a@test.com"}
    assert validate_data(data) == []


def test_all_invalid() -> None:
    """Test all fields invalid."""
    data = {"name": "", "age": "-5", "email": "invalid"}
    errors = validate_data(data)
    assert "name cannot be empty" in errors
    assert "age must be non-negative" in errors
    assert "email must contain @" in errors


def test_missing_fields() -> None:
    """Test missing required fields."""
    assert "name is required" in validate_data({})
    assert "age is required" in validate_data({})
    assert "email is required" in validate_data({})


def test_invalid_age_type() -> None:
    """Test invalid age type."""
    data = {"name": "Alice", "age": "abc", "email": "a@test.com"}
    assert "age must be a valid integer" in validate_data(data)


def test_name_not_string() -> None:
    """Test name that's not a string."""
    data = {"name": 123, "age": "30", "email": "a@test.com"}
    assert "name must be a string" in validate_data(data)


def test_age_zero() -> None:
    """Test age of zero (should be valid)."""
    data = {"name": "Baby", "age": "0", "email": "baby@test.com"}
    assert validate_data(data) == []
