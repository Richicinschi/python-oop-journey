"""Tests for Problem 04: Package Math Tools."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day03.problem_04_package_math_tools import (
    add,
    subtract,
    multiply,
    divide,
    power,
    sqrt,
    factorial,
    mean,
    median,
    __version__,
)


# ===== Basic operations tests =====
def test_add() -> None:
    """Test add function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0.5, 0.5) == 1.0


def test_subtract() -> None:
    """Test subtract function."""
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0


def test_multiply() -> None:
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


def test_divide() -> None:
    """Test divide function."""
    assert divide(6, 2) == 3.0
    assert divide(5, 2) == 2.5
    assert divide(0, 5) == 0.0


def test_divide_by_zero() -> None:
    """Test divide by zero raises error."""
    try:
        divide(5, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ===== Advanced operations tests =====
def test_power() -> None:
    """Test power function."""
    assert power(2, 3) == 8
    assert power(2, 0) == 1
    assert power(9, 0.5) == 3.0


def test_sqrt() -> None:
    """Test sqrt function."""
    assert sqrt(4) == 2.0
    assert sqrt(9) == 3.0
    assert sqrt(0) == 0.0


def test_sqrt_negative() -> None:
    """Test sqrt of negative number raises error."""
    try:
        sqrt(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_factorial() -> None:
    """Test factorial function."""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800


def test_factorial_negative() -> None:
    """Test factorial of negative number raises error."""
    try:
        factorial(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ===== Statistics tests =====
def test_mean() -> None:
    """Test mean function."""
    assert mean([1, 2, 3]) == 2.0
    assert mean([1, 1, 1]) == 1.0
    assert mean([5]) == 5.0


def test_mean_empty() -> None:
    """Test mean of empty list raises error."""
    try:
        mean([])
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_median_odd() -> None:
    """Test median with odd number of elements."""
    assert median([1, 2, 3]) == 2
    assert median([3, 1, 2]) == 2
    assert median([5]) == 5


def test_median_even() -> None:
    """Test median with even number of elements."""
    assert median([1, 2, 3, 4]) == 2.5
    assert median([1, 3, 5, 7]) == 4.0


def test_median_empty() -> None:
    """Test median of empty list raises error."""
    try:
        median([])
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_version() -> None:
    """Test version is defined."""
    assert __version__ == "1.0.0"
