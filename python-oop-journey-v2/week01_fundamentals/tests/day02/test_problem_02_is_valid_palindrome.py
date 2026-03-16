"""Tests for Problem 02: Valid Palindrome."""

from __future__ import annotations

from week01_fundamentals.solutions.day02.problem_02_is_valid_palindrome import is_valid_palindrome


def test_palindrome_with_punctuation_and_spaces() -> None:
    """Test classic palindrome with punctuation and spaces."""
    assert is_valid_palindrome("A man, a plan, a canal: Panama") is True


def test_not_palindrome() -> None:
    """Test non-palindrome string."""
    assert is_valid_palindrome("race a car") is False


def test_empty_string() -> None:
    """Test empty string."""
    assert is_valid_palindrome("") is True


def test_single_space() -> None:
    """Test single space (no alphanumeric characters)."""
    assert is_valid_palindrome(" ") is True


def test_single_character() -> None:
    """Test single alphanumeric character."""
    assert is_valid_palindrome("a") is True


def test_two_different_characters() -> None:
    """Test two different alphanumeric characters."""
    assert is_valid_palindrome("ab") is False


def test_two_same_characters() -> None:
    """Test two same alphanumeric characters."""
    assert is_valid_palindrome("aa") is True


def test_mixed_case_palindrome() -> None:
    """Test palindrome with mixed case."""
    assert is_valid_palindrome("RaCeCaR") is True


def test_numbers_in_palindrome() -> None:
    """Test palindrome containing numbers."""
    assert is_valid_palindrome("0P0") is True


def test_zero_and_p() -> None:
    """Test '0P' which is not a palindrome (0 != P)."""
    assert is_valid_palindrome("0P") is False


def test_only_special_characters() -> None:
    """Test string with only special characters."""
    assert is_valid_palindrome(".,;:!?") is True
