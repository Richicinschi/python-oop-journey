"""Tests for Problem 06: Calculator Package."""

from __future__ import annotations

import math

from week02_fundamentals_advanced.solutions.day03.problem_06_calculator_package import (
    add,
    subtract,
    multiply,
    divide,
    modulo,
    sin,
    cos,
    tan,
    log,
    exp,
    PI,
    E,
    Calculator,
)


# ===== Arithmetic function tests =====
def test_add_function() -> None:
    """Test add function."""
    assert add(2, 3) == 5


def test_subtract_function() -> None:
    """Test subtract function."""
    assert subtract(5, 3) == 2


def test_multiply_function() -> None:
    """Test multiply function."""
    assert multiply(2, 3) == 6


def test_divide_function() -> None:
    """Test divide function."""
    assert divide(6, 2) == 3.0


def test_divide_by_zero() -> None:
    """Test divide by zero raises error."""
    try:
        divide(5, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_modulo_function() -> None:
    """Test modulo function."""
    assert modulo(7, 3) == 1
    assert modulo(10, 5) == 0


def test_modulo_by_zero() -> None:
    """Test modulo by zero raises error."""
    try:
        modulo(5, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ===== Scientific function tests =====
def test_sin() -> None:
    """Test sin function."""
    assert abs(sin(0)) < 1e-10
    assert abs(sin(math.pi / 2) - 1) < 1e-10


def test_cos() -> None:
    """Test cos function."""
    assert abs(cos(0) - 1) < 1e-10
    assert abs(cos(math.pi / 2)) < 1e-10


def test_tan() -> None:
    """Test tan function."""
    assert abs(tan(0)) < 1e-10
    assert abs(tan(math.pi / 4) - 1) < 1e-10


def test_log() -> None:
    """Test log function."""
    assert abs(log(math.e) - 1) < 1e-10
    assert abs(log(100, 10) - 2) < 1e-10


def test_log_invalid() -> None:
    """Test log with invalid inputs."""
    try:
        log(-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        log(10, 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_exp() -> None:
    """Test exp function."""
    assert abs(exp(0) - 1) < 1e-10
    assert abs(exp(1) - math.e) < 1e-10


# ===== Constants tests =====
def test_pi_constant() -> None:
    """Test PI constant."""
    assert abs(PI - math.pi) < 1e-10


def test_e_constant() -> None:
    """Test E constant."""
    assert abs(E - math.e) < 1e-10


# ===== Calculator class tests =====
def test_calculator_init() -> None:
    """Test Calculator initialization."""
    calc = Calculator()
    assert calc.result == 0.0


def test_calculator_init_with_value() -> None:
    """Test Calculator initialization with start value."""
    calc = Calculator(10)
    assert calc.result == 10.0


def test_calculator_add() -> None:
    """Test Calculator add."""
    calc = Calculator()
    calc.add(5)
    assert calc.result == 5.0


def test_calculator_subtract() -> None:
    """Test Calculator subtract."""
    calc = Calculator(10)
    calc.subtract(3)
    assert calc.result == 7.0


def test_calculator_multiply() -> None:
    """Test Calculator multiply."""
    calc = Calculator(5)
    calc.multiply(3)
    assert calc.result == 15.0


def test_calculator_divide() -> None:
    """Test Calculator divide."""
    calc = Calculator(10)
    calc.divide(2)
    assert calc.result == 5.0


def test_calculator_divide_by_zero() -> None:
    """Test Calculator divide by zero."""
    calc = Calculator(10)
    try:
        calc.divide(0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_calculator_chaining() -> None:
    """Test Calculator method chaining."""
    calc = Calculator()
    result = calc.add(5).multiply(2).subtract(3).result
    assert result == 7.0


def test_calculator_clear() -> None:
    """Test Calculator clear."""
    calc = Calculator()
    calc.add(10).multiply(2)
    calc.clear()
    assert calc.result == 0.0
    assert calc.history == []


def test_calculator_history() -> None:
    """Test Calculator history tracking."""
    calc = Calculator()
    calc.add(5)
    calc.multiply(2)
    
    history = calc.history
    assert len(history) == 2
    assert "add(5)" in history[0]
    assert "multiply(2)" in history[1]


def test_calculator_history_with_init() -> None:
    """Test Calculator history with init value."""
    calc = Calculator(10)
    calc.add(5)
    
    history = calc.history
    assert len(history) == 2
    assert "init(10)" in history[0]
