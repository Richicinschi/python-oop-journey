"""Problem 07: Math Toolkit

Topic: @staticmethod math utilities
Difficulty: Medium

Create a MathToolkit class with various static methods for mathematical
operations and utilities.

Example:
    >>> MathToolkit.is_prime(7)
    True
    >>> MathToolkit.is_prime(10)
    False
    >>> 
    >>> MathToolkit.gcd(48, 18)
    6
    >>> 
    >>> MathToolkit.lcm(4, 6)
    12
    >>> 
    >>> MathToolkit.factorial(5)
    120
    >>> 
    >>> MathToolkit.fibonacci(10)
    55
    >>> 
    >>> MathToolkit.is_perfect_square(16)
    True
    >>> MathToolkit.is_perfect_square(15)
    False

Requirements:
    - is_prime(n: int) -> bool: static method
    - gcd(a: int, b: int) -> int: static method (Greatest Common Divisor)
    - lcm(a: int, b: int) -> int: static method (Least Common Multiple)
    - factorial(n: int) -> int: static method
    - fibonacci(n: int) -> int: static method (nth Fibonacci number)
    - is_perfect_square(n: int) -> bool: static method
    - All methods must be @staticmethod
    - Handle edge cases (n < 0, etc.)
"""

from __future__ import annotations
import math


class MathToolkit:
    """Collection of mathematical utility functions."""
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime.
        
        Args:
            n: Number to check
            
        Returns:
            True if prime, False otherwise
        """
        raise NotImplementedError("Implement is_prime")
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            GCD of a and b
        """
        raise NotImplementedError("Implement gcd")
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate Least Common Multiple.
        
        LCM(a, b) = |a * b| / GCD(a, b)
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            LCM of a and b
        """
        raise NotImplementedError("Implement lcm")
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of n.
        
        Args:
            n: Non-negative integer
            
        Returns:
            n! (factorial of n)
            
        Raises:
            ValueError: If n is negative
        """
        raise NotImplementedError("Implement factorial")
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculate the nth Fibonacci number.
        
        F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
        
        Args:
            n: Index in Fibonacci sequence (0-indexed)
            
        Returns:
            nth Fibonacci number
            
        Raises:
            ValueError: If n is negative
        """
        raise NotImplementedError("Implement fibonacci")
    
    @staticmethod
    def is_perfect_square(n: int) -> bool:
        """Check if a number is a perfect square.
        
        Args:
            n: Number to check
            
        Returns:
            True if n is a perfect square, False otherwise
        """
        raise NotImplementedError("Implement is_perfect_square")
