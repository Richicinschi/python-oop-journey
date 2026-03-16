"""Solution for Problem 07: Math Toolkit."""

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
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            GCD of a and b
        """
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a
    
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
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // MathToolkit.gcd(a, b)
    
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
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
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
        if n < 0:
            raise ValueError("Fibonacci is not defined for negative indices")
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        return curr
    
    @staticmethod
    def is_perfect_square(n: int) -> bool:
        """Check if a number is a perfect square.
        
        Args:
            n: Number to check
            
        Returns:
            True if n is a perfect square, False otherwise
        """
        if n < 0:
            return False
        root = int(math.sqrt(n))
        return root * root == n
