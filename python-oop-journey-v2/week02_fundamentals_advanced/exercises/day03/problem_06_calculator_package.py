"""Problem 06: Calculator Package

Topic: Package structure, relative imports simulation
Difficulty: Medium

Create a calculator package structure with operations organized into
submodules. This file acts as the main package interface.

Requirements:
    - Organize functions as if they come from different submodules:
      * arithmetic: add, subtract, multiply, divide, modulo
      * scientific: sin, cos, tan, log, exp (use math module)
      * constants: PI, E
    - Provide a Calculator class that uses these operations
    - The Calculator should maintain a history of operations
    - Support method chaining (fluent interface)

Example:
    from problem_06_calculator_package import Calculator, add, PI
    
    # Functional usage
    print(add(2, 3))  # 5
    print(PI)         # 3.14159...
    
    # Calculator class usage
    calc = Calculator()
    result = calc.add(5).multiply(2).divide(10).result
    print(result)     # 1.0
    print(calc.history)  # ['add(5) -> 5', 'multiply(2) -> 10', 'divide(10) -> 1.0']
"""

from __future__ import annotations

import math
from typing import List

# ===== Constants (as if from 'constants' submodule) =====
PI: float = math.pi
E: float = math.e


# ===== Arithmetic operations (as if from 'arithmetic' submodule) =====
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
    """Divide a by b. Raises ValueError on division by zero."""
    raise NotImplementedError("Implement divide")


def modulo(a: float, b: float) -> float:
    """Calculate a modulo b. Raises ValueError if b is zero."""
    raise NotImplementedError("Implement modulo")


# ===== Scientific operations (as if from 'scientific' submodule) =====
def sin(angle: float) -> float:
    """Calculate sine of angle (in radians)."""
    raise NotImplementedError("Implement sin")


def cos(angle: float) -> float:
    """Calculate cosine of angle (in radians)."""
    raise NotImplementedError("Implement cos")


def tan(angle: float) -> float:
    """Calculate tangent of angle (in radians)."""
    raise NotImplementedError("Implement tan")


def log(x: float, base: float = math.e) -> float:
    """Calculate logarithm of x with given base."""
    raise NotImplementedError("Implement log")


def exp(x: float) -> float:
    """Calculate e raised to the power of x."""
    raise NotImplementedError("Implement exp")


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
        raise NotImplementedError("Implement __init__")
    
    @property
    def result(self) -> float:
        """Get the current calculated result."""
        raise NotImplementedError("Implement result property")
    
    @property
    def history(self) -> List[str]:
        """Get the operation history."""
        raise NotImplementedError("Implement history property")
    
    def clear(self) -> Calculator:
        """Reset calculator to zero and clear history.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement clear")
    
    def add(self, value: float) -> Calculator:
        """Add value to current result.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement add")
    
    def subtract(self, value: float) -> Calculator:
        """Subtract value from current result.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement subtract")
    
    def multiply(self, value: float) -> Calculator:
        """Multiply current result by value.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement multiply")
    
    def divide(self, value: float) -> Calculator:
        """Divide current result by value.
        
        Raises:
            ValueError: If value is zero
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement divide")
    
    def power(self, exponent: float) -> Calculator:
        """Raise current result to the power of exponent.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement power")
