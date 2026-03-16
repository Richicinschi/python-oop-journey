"""Tests for Problem 03: Validate Password."""

from __future__ import annotations

from week00_getting_started.solutions.day08.problem_03_validate_password import validate_password


def test_validate_password_valid() -> None:
    """Test valid passwords that meet all criteria."""
    assert validate_password("HelloWorld1") is True
    assert validate_password("Password123") is True
    assert validate_password("A1b2C3d4E5") is True
    assert validate_password("MyP@ssw0rd") is True


def test_validate_password_too_short() -> None:
    """Test passwords that are too short."""
    assert validate_password("Hello1") is False  # 6 chars
    assert validate_password("Aa1") is False  # 3 chars
    assert validate_password("") is False  # Empty


def test_validate_password_no_uppercase() -> None:
    """Test passwords without uppercase letters."""
    assert validate_password("helloworld1") is False
    assert validate_password("password123") is False
    assert validate_password("abcdefgh1") is False


def test_validate_password_no_lowercase() -> None:
    """Test passwords without lowercase letters."""
    assert validate_password("HELLOWORLD1") is False
    assert validate_password("PASSWORD123") is False
    assert validate_password("ABCDEFGH1") is False


def test_validate_password_no_digit() -> None:
    """Test passwords without digits."""
    assert validate_password("HelloWorld") is False
    assert validate_password("PasswordOnly") is False
    assert validate_password("ABCDEFGHi") is False


def test_validate_password_multiple_missing() -> None:
    """Test passwords missing multiple criteria."""
    assert validate_password("hello") is False  # No upper, no digit, short
    assert validate_password("HELLO") is False  # No lower, no digit, short
    assert validate_password("12345678") is False  # No upper, no lower
