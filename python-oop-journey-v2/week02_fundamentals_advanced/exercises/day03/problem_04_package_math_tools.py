"""Problem 04: Package Math Tools

Topic: Creating packages, submodules, __init__.py
Difficulty: Medium

Create a mini math package with submodules for different mathematical
operations. This file represents the package's __init__.py that exposes
selected functions from submodules.

Requirements:
    - Import and expose functions from 'basic' submodule: add, subtract, multiply, divide
    - Import and expose functions from 'advanced' submodule: power, sqrt, factorial
    - Import and expose functions from 'stats' submodule: mean, median
    - Define __version__ = "1.0.0"
    - Define __all__ listing all public exports
    - Handle import errors gracefully with fallback implementations

Example:
    # User imports the package
    from problem_04_package_math_tools import add, power, mean
    
    print(add(2, 3))        # 5
    print(power(2, 3))      # 8
    print(mean([1, 2, 3]))  # 2.0

Note: Since we can't create actual submodules in this exercise,
implement the functions directly in this file but organize them
as if they came from submodules (use internal naming conventions).
"""

from __future__ import annotations

from typing import List

__version__ = "1.0.0"

# TODO: Define __all__ with all public exports


# ===== Basic operations (as if from 'basic' submodule) =====
def add(a: float, b: float) -> float:
    """Add two numbers."""
    raise NotImplementedError("Implement add")


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    raise NotImplementedError("Implement subtract")


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    raise NotImplementedError("Implement multiply")


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ValueError if b is zero."""
    raise NotImplementedError("Implement divide")


# ===== Advanced operations (as if from 'advanced' submodule) =====
def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent."""
    raise NotImplementedError("Implement power")


def sqrt(x: float) -> float:
    """Calculate the square root of x. Raises ValueError if x < 0."""
    raise NotImplementedError("Implement sqrt")


def factorial(n: int) -> int:
    """Calculate factorial of n. Raises ValueError if n < 0."""
    raise NotImplementedError("Implement factorial")


# ===== Statistics operations (as if from 'stats' submodule) =====
def mean(data: List[float]) -> float:
    """Calculate arithmetic mean. Raises ValueError if data is empty."""
    raise NotImplementedError("Implement mean")


def median(data: List[float]) -> float:
    """Calculate median. Raises ValueError if data is empty."""
    raise NotImplementedError("Implement median")
