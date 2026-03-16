"""Tests for Problem 06: Parse and Validate Records."""

from __future__ import annotations

from week00_getting_started.solutions.day29.problem_06_parse_validate import (
    parse_email_record,
    process_email_records,
    validate_age,
    validate_email,
)


def test_parse_email_record_valid() -> None:
    """Test parse_email_record with valid input."""
    result = parse_email_record("john@example.com|John Doe|25")
    assert result == {"email": "john@example.com", "name": "John Doe", "age": "25"}


def test_parse_email_record_invalid() -> None:
    """Test parse_email_record with invalid format."""
    assert parse_email_record("only|two") is None
    assert parse_email_record("no pipes here") is None


def test_validate_email_valid() -> None:
    """Test validate_email with valid emails."""
    assert validate_email("john@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    assert validate_email("a@b.c") is True


def test_validate_email_invalid() -> None:
    """Test validate_email with invalid emails."""
    assert validate_email("invalid-email") is False
    assert validate_email("@nodomain.com") is False
    assert validate_email("noat.com") is False
    assert validate_email("spaces in@name.com") is False
    assert validate_email("") is False


def test_validate_age_valid() -> None:
    """Test validate_age with valid ages."""
    is_valid, age, error = validate_age("25")
    assert is_valid is True
    assert age == 25
    assert error == ""


def test_validate_age_boundary() -> None:
    """Test validate_age at boundaries."""
    assert validate_age("18")[0] is True
    assert validate_age("120")[0] is True


def test_validate_age_too_young() -> None:
    """Test validate_age with age too young."""
    is_valid, age, error = validate_age("17")
    assert is_valid is False
    assert "18" in error or "120" in error


def test_validate_age_too_old() -> None:
    """Test validate_age with age too old."""
    is_valid, age, error = validate_age("121")
    assert is_valid is False


def test_validate_age_not_integer() -> None:
    """Test validate_age with non-integer."""
    is_valid, age, error = validate_age("twenty")
    assert is_valid is False
    assert "integer" in error.lower()


def test_process_email_records_mixed() -> None:
    """Test process_email_records with mixed valid/invalid."""
    records = [
        "john@example.com|John Doe|25",
        "invalid-email|Jane Doe|30",
        "bob@test.com|Bob|17",  # Too young
        "malformed",
    ]
    result = process_email_records(records)

    assert len(result["valid"]) == 1
    assert len(result["invalid"]) == 3
    assert result["valid"][0]["email"] == "john@example.com"


def test_process_email_records_valid_only() -> None:
    """Test process_email_records with all valid."""
    records = [
        "alice@test.com|Alice Smith|30",
        "bob@test.com|Bob Jones|45",
    ]
    result = process_email_records(records)
    assert len(result["valid"]) == 2
    assert len(result["invalid"]) == 0


def test_process_email_records_invalid_name() -> None:
    """Test process_email_records with invalid name."""
    records = ["test@test.com|John123|25"]  # Numbers in name
    result = process_email_records(records)
    assert len(result["invalid"]) == 1
