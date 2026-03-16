"""Tests for Problem 04: Generate Parentheses."""

from __future__ import annotations

from week01_fundamentals.solutions.day05.problem_04_generate_parentheses import generate_parentheses


def test_generate_parentheses_n_equals_1() -> None:
    result = generate_parentheses(1)
    assert result == ['()']


def test_generate_parentheses_n_equals_2() -> None:
    result = generate_parentheses(2)
    result.sort()
    expected = ['(())', '()()']
    expected.sort()
    assert result == expected


def test_generate_parentheses_n_equals_3() -> None:
    result = generate_parentheses(3)
    result.sort()
    expected = ['((()))', '(()())', '(())()', '()(())', '()()()']
    expected.sort()
    assert result == expected


def test_generate_parentheses_n_equals_0() -> None:
    assert generate_parentheses(0) == ['']


def test_generate_parentheses_negative() -> None:
    assert generate_parentheses(-1) == []


def test_generate_parentheses_n_equals_4() -> None:
    result = generate_parentheses(4)
    assert len(result) == 14  # Catalan number C4 = 14
