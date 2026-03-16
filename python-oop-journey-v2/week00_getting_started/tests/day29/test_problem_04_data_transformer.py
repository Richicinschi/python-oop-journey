"""Tests for Problem 04: Data Transformer Pipeline."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_04_data_transformer import (
    parse_record,
    process_records,
    transform_record,
    validate_record,
)


def test_parse_record_valid() -> None:
    """Test parse_record with valid input."""
    result = parse_record("john doe,30,new york,50000")
    assert result == {
        "name": "john doe",
        "age": "30",
        "city": "new york",
        "salary": "50000",
    }


def test_parse_record_invalid_format() -> None:
    """Test parse_record with invalid format."""
    assert parse_record("only,two,fields") is None
    assert parse_record("one field only") is None


def test_validate_record_valid() -> None:
    """Test validate_record with valid record."""
    record = {"name": "John", "age": "30", "city": "NYC", "salary": "50000"}
    is_valid, error = validate_record(record)
    assert is_valid is True
    assert error == ""


def test_validate_record_missing_field() -> None:
    """Test validate_record with missing field."""
    record = {"name": "John", "age": "30", "salary": "50000"}
    is_valid, error = validate_record(record)
    assert is_valid is False
    assert "Missing field" in error


def test_validate_record_invalid_age() -> None:
    """Test validate_record with invalid age."""
    record = {"name": "John", "age": "200", "city": "NYC", "salary": "50000"}
    is_valid, error = validate_record(record)
    assert is_valid is False
    assert "Age" in error


def test_validate_record_negative_salary() -> None:
    """Test validate_record with negative salary."""
    record = {"name": "John", "age": "30", "city": "NYC", "salary": "-50000"}
    is_valid, error = validate_record(record)
    assert is_valid is False
    assert "Salary" in error


def test_transform_record_valid() -> None:
    """Test transform_record with valid data."""
    record = {"name": "john doe", "age": "30", "city": "new york", "salary": "50000.50"}
    result = transform_record(record)
    assert result == {
        "name": "John Doe",
        "age": 30,
        "city": "new york",
        "salary": 50000.50,
    }


def test_transform_record_invalid() -> None:
    """Test transform_record returns None for invalid data."""
    record = {"name": "John", "age": "200", "city": "NYC", "salary": "50000"}
    result = transform_record(record)
    assert result is None


def test_process_records_mixed() -> None:
    """Test process_records with mixed valid/invalid records."""
    lines = [
        "john doe,30,new york,50000",
        "invalid format",
        "jane smith,25,boston,60000",
        "bad age,999,city,1000",
    ]
    result = process_records(lines)

    assert len(result["success"]) == 2
    assert len(result["failed"]) == 2
    assert result["stats"]["count_success"] == 2
    assert result["stats"]["count_failed"] == 2


def test_process_records_empty() -> None:
    """Test process_records with empty list."""
    result = process_records([])
    assert result["success"] == []
    assert result["failed"] == []
    assert result["stats"]["count_total"] == 0


def test_process_records_whitespace_handling() -> None:
    """Test process_records handles whitespace correctly."""
    lines = ["  john doe  ,  30  ,  new york  ,  50000  "]
    result = process_records(lines)
    assert len(result["success"]) == 1
    assert result["success"][0]["name"] == "John Doe"
