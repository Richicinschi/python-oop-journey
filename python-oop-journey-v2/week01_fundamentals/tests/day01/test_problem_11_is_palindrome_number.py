"""Tests for Problem 11: Is Palindrome Number."""

from __future__ import annotations

from week01_fundamentals.solutions.day01.problem_11_is_palindrome_number import is_palindrome_number


def test_palindrome_numbers() -> None:
    """Test various palindrome numbers."""
    palindromes = [0, 1, 5, 9, 11, 22, 121, 333, 12321, 123321]
    for n in palindromes:
        assert is_palindrome_number(n) is True, f"{n} should be a palindrome"


def test_non_palindrome_numbers() -> None:
    """Test various non-palindrome numbers."""
    non_palindromes = [10, 12, 100, 123, 456, 123456]
    for n in non_palindromes:
        assert is_palindrome_number(n) is False, f"{n} should not be a palindrome"


def test_negative_numbers() -> None:
    """Test that negative numbers are not palindromes."""
    negatives = [-1, -121, -12321, -11]
    for n in negatives:
        assert is_palindrome_number(n) is False, f"{n} should not be a palindrome"


def test_zero() -> None:
    """Test zero is a palindrome."""
    assert is_palindrome_number(0) is True


def test_single_digit() -> None:
    """Test all single-digit numbers are palindromes."""
    for n in range(10):
        assert is_palindrome_number(n) is True


def test_ending_with_zero() -> None:
    """Test numbers ending with 0 (except 0) are not palindromes."""
    assert is_palindrome_number(10) is False
    assert is_palindrome_number(100) is False
    assert is_palindrome_number(1010) is False
    assert is_palindrome_number(1001) is True  # Doesn't end with 0


def test_large_palindrome() -> None:
    """Test larger palindrome numbers."""
    assert is_palindrome_number(123454321) is True
    assert is_palindrome_number(1234554321) is True


def test_large_non_palindrome() -> None:
    """Test larger non-palindrome numbers."""
    assert is_palindrome_number(123456789) is False
    assert is_palindrome_number(2147483647) is False
