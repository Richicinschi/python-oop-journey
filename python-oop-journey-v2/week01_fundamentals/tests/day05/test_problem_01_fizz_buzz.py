"""Tests for Problem 01: FizzBuzz."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_01_fizz_buzz import fizz_buzz


def test_fizz_buzz_basic() -> None:
    result = fizz_buzz(5)
    assert result == ['1', '2', 'Fizz', '4', 'Buzz']


def test_fizz_buzz_with_fizzbuzz() -> None:
    result = fizz_buzz(15)
    expected = [
        '1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz',
        '11', 'Fizz', '13', '14', 'FizzBuzz'
    ]
    assert result == expected


def test_fizz_buzz_n_is_1() -> None:
    assert fizz_buzz(1) == ['1']


def test_fizz_buzz_n_is_3() -> None:
    result = fizz_buzz(3)
    assert result == ['1', '2', 'Fizz']


def test_fizz_buzz_n_is_0() -> None:
    assert fizz_buzz(0) == []


def test_fizz_buzz_negative() -> None:
    assert fizz_buzz(-5) == []
