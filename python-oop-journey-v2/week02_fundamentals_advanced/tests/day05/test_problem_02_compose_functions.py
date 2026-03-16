"""Tests for Problem 02: Compose Functions."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_02_compose_functions import (
    compose_two,
    compose,
    pipe,
)


def add_one(x: int) -> int:
    return x + 1


def double(x: int) -> int:
    return x * 2


def negate(x: int) -> int:
    return -x


def square(x: int) -> int:
    return x ** 2


class TestComposeTwo:
    """Tests for compose_two function."""

    def test_basic_composition(self) -> None:
        """Test basic composition of two functions."""
        h = compose_two(double, add_one)
        # double(add_one(3)) = double(4) = 8
        assert h(3) == 8

    def test_composition_order(self) -> None:
        """Test that composition order is correct."""
        # compose_two(f, g) means f(g(x))
        h1 = compose_two(double, add_one)  # 2 * (x + 1)
        h2 = compose_two(add_one, double)  # (2 * x) + 1

        assert h1(3) == 8  # 2 * (3 + 1) = 8
        assert h2(3) == 7  # (2 * 3) + 1 = 7

    def test_with_string_functions(self) -> None:
        """Test with string functions."""
        def add_exclaim(s: str) -> str:
            return s + "!"

        def to_upper(s: str) -> str:
            return s.upper()

        h = compose_two(add_exclaim, to_upper)
        assert h("hello") == "HELLO!"


class TestCompose:
    """Tests for compose function."""

    def test_single_function(self) -> None:
        """Test with single function."""
        h = compose(add_one)
        assert h(5) == 6

    def test_two_functions(self) -> None:
        """Test with two functions."""
        h = compose(double, add_one)
        # Right to left: add_one then double
        # double(add_one(3)) = double(4) = 8
        assert h(3) == 8

    def test_multiple_functions(self) -> None:
        """Test with multiple functions."""
        h = compose(negate, double, add_one)
        # Right to left: add_one, then double, then negate
        # negate(double(add_one(3))) = negate(double(4)) = negate(8) = -8
        assert h(3) == -8

    def test_four_functions(self) -> None:
        """Test with four functions."""
        h = compose(square, add_one, double, negate)
        # square(add_one(double(negate(3))))
        # = square(add_one(double(-3)))
        # = square(add_one(-6))
        # = square(-5)
        # = 25
        assert h(3) == 25

    def test_empty_compose(self) -> None:
        """Test with no functions returns identity."""
        h = compose()
        assert h(42) == 42
        assert h("hello") == "hello"

    def test_with_lambdas(self) -> None:
        """Test with lambda functions."""
        h = compose(
            lambda x: x * 3,
            lambda x: x + 2,
            lambda x: x - 1
        )
        # ((5 - 1) + 2) * 3 = (4 + 2) * 3 = 18
        assert h(5) == 18


class TestPipe:
    """Tests for pipe function."""

    def test_single_function(self) -> None:
        """Test with single function."""
        h = pipe(add_one)
        assert h(5) == 6

    def test_two_functions(self) -> None:
        """Test with two functions."""
        h = pipe(add_one, double)
        # Left to right: add_one then double
        # double(add_one(3)) = double(4) = 8
        assert h(3) == 8

    def test_multiple_functions(self) -> None:
        """Test with multiple functions."""
        h = pipe(add_one, double, negate)
        # Left to right: add_one, then double, then negate
        # negate(double(add_one(3))) = negate(double(4)) = negate(8) = -8
        assert h(3) == -8

    def test_compose_vs_pipe(self) -> None:
        """Test that compose and pipe produce same result with reversed args."""
        composed = compose(negate, double, add_one)
        piped = pipe(add_one, double, negate)

        for i in range(-5, 6):
            assert composed(i) == piped(i)

    def test_string_pipeline(self) -> None:
        """Test pipe with string operations (more intuitive order)."""
        def strip(s: str) -> str:
            return s.strip()

        def capitalize(s: str) -> str:
            return s.capitalize()

        def add_period(s: str) -> str:
            return s + "."

        h = pipe(strip, capitalize, add_period)
        assert h("  hello world  ") == "Hello world."

    def test_empty_pipe(self) -> None:
        """Test with no functions returns identity."""
        h = pipe()
        assert h(42) == 42
