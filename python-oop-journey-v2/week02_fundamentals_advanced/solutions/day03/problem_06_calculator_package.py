"""Reference solution for Problem 06: Calculator Package."""

from __future__ import annotations

import math
from typing import List

# ===== Constants (as if from 'constants' submodule) =====
PI: float = math.pi
E: float = math.e


# ===== Arithmetic operations (as if from 'arithmetic' submodule) =====
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def modulo(a: float, b: float) -> float:
    """Calculate a modulo b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot calculate modulo by zero")
    return a % b


# ===== Scientific operations (as if from 'scientific' submodule) =====
def sin(angle: float) -> float:
    """Calculate sine of angle (in radians)."""
    return math.sin(angle)


def cos(angle: float) -> float:
    """Calculate cosine of angle (in radians)."""
    return math.cos(angle)


def tan(angle: float) -> float:
    """Calculate tangent of angle (in radians)."""
    return math.tan(angle)


def log(x: float, base: float = math.e) -> float:
    """Calculate logarithm of x with given base."""
    if x <= 0:
        raise ValueError("Cannot calculate logarithm of non-positive number")
    if base <= 0 or base == 1:
        raise ValueError("Invalid logarithm base")
    return math.log(x, base)


def exp(x: float) -> float:
    """Calculate e raised to the power of x."""
    return math.exp(x)


# ===== Calculator class =====
class Calculator:
    """A calculator with history tracking and method chaining.
    
    The calculator maintains a running result and tracks all operations
    performed on it. Methods return self to enable chaining.
    
    Example:
        calc = Calculator(start_value=10)
        result = calc.add(5).multiply(2).subtract(3).result
        print(result)  # 27
        print(calc.history)
    """
    
    def __init__(self, start_value: float = 0.0) -> None:
        """Initialize calculator with optional starting value.
        
        Args:
            start_value: Initial value for the calculator
        """
        self._result = float(start_value)
        self._history: List[str] = []
        if start_value != 0:
            self._history.append(f"init({start_value})")
    
    @property
    def result(self) -> float:
        """Get the current calculated result."""
        return self._result
    
    @property
    def history(self) -> List[str]:
        """Get the operation history."""
        return list(self._history)
    
    def clear(self) -> Calculator:
        """Reset calculator to zero and clear history.
        
        Returns:
            Self for method chaining
        """
        self._result = 0.0
        self._history.clear()
        return self
    
    def add(self, value: float) -> Calculator:
        """Add value to current result.
        
        Returns:
            Self for method chaining
        """
        self._result = add(self._result, value)
        self._history.append(f"add({value}) -> {self._result}")
        return self
    
    def subtract(self, value: float) -> Calculator:
        """Subtract value from current result.
        
        Returns:
            Self for method chaining
        """
        self._result = subtract(self._result, value)
        self._history.append(f"subtract({value}) -> {self._result}")
        return self
    
    def multiply(self, value: float) -> Calculator:
        """Multiply current result by value.
        
        Returns:
            Self for method chaining
        """
        self._result = multiply(self._result, value)
        self._history.append(f"multiply({value}) -> {self._result}")
        return self
    
    def divide(self, value: float) -> Calculator:
        """Divide current result by value.
        
        Raises:
            ValueError: If value is zero
            
        Returns:
            Self for method chaining
        """
        if value == 0:
            raise ValueError("Cannot divide by zero")
        self._result = divide(self._result, value)
        self._history.append(f"divide({value}) -> {self._result}")
        return self
    
    def power(self, exponent: float) -> Calculator:
        """Raise current result to the power of exponent.
        
        Returns:
            Self for method chaining
        """
        self._result = power(self._result, exponent)
        self._history.append(f"power({exponent}) -> {self._result}")
        return self
