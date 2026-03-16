"""Reference solution for Problem 04: Package Math Tools."""

from __future__ import annotations

from typing import List
import math

__version__ = "1.0.0"
__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "sqrt",
    "factorial",
    "mean",
    "median",
    "__version__",
]


# ===== Basic operations (as if from 'basic' submodule) =====
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
    """Divide a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# ===== Advanced operations (as if from 'advanced' submodule) =====
def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent."""
    return base ** exponent


def sqrt(x: float) -> float:
    """Calculate the square root of x. Raises ValueError if x < 0."""
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(x)


def factorial(n: int) -> int:
    """Calculate factorial of n. Raises ValueError if n < 0."""
    if n < 0:
        raise ValueError("Cannot calculate factorial of negative number")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ===== Statistics operations (as if from 'stats' submodule) =====
def mean(data: List[float]) -> float:
    """Calculate arithmetic mean. Raises ValueError if data is empty."""
    if not data:
        raise ValueError("Cannot calculate mean of empty data")
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """Calculate median. Raises ValueError if data is empty."""
    if not data:
        raise ValueError("Cannot calculate median of empty data")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]
