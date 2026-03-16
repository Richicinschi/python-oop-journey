"""Tests for Problem 07: Math Toolkit."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_07_math_toolkit import MathToolkit


class TestIsPrime:
    """Test suite for is_prime."""
    
    def test_small_primes(self) -> None:
        """Test small prime numbers."""
        assert MathToolkit.is_prime(2) is True
        assert MathToolkit.is_prime(3) is True
        assert MathToolkit.is_prime(5) is True
        assert MathToolkit.is_prime(7) is True
    
    def test_small_composites(self) -> None:
        """Test small composite numbers."""
        assert MathToolkit.is_prime(1) is False
        assert MathToolkit.is_prime(4) is False
        assert MathToolkit.is_prime(6) is False
        assert MathToolkit.is_prime(9) is False
    
    def test_larger_primes(self) -> None:
        """Test larger prime numbers."""
        assert MathToolkit.is_prime(97) is True
        assert MathToolkit.is_prime(101) is True
    
    def test_negative_and_zero(self) -> None:
        """Test negative numbers and zero."""
        assert MathToolkit.is_prime(0) is False
        assert MathToolkit.is_prime(-5) is False


class TestGCD:
    """Test suite for gcd."""
    
    def test_basic_gcd(self) -> None:
        """Test basic GCD calculations."""
        assert MathToolkit.gcd(48, 18) == 6
        assert MathToolkit.gcd(56, 98) == 14
    
    def test_coprime(self) -> None:
        """Test coprime numbers."""
        assert MathToolkit.gcd(17, 19) == 1
    
    def test_one_is_multiple(self) -> None:
        """Test when one number is multiple of other."""
        assert MathToolkit.gcd(12, 4) == 4
    
    def test_equal_numbers(self) -> None:
        """Test equal numbers."""
        assert MathToolkit.gcd(7, 7) == 7
    
    def test_zero(self) -> None:
        """Test with zero."""
        assert MathToolkit.gcd(5, 0) == 5
        assert MathToolkit.gcd(0, 5) == 5
    
    def test_negative(self) -> None:
        """Test with negative numbers."""
        assert MathToolkit.gcd(-48, 18) == 6
        assert MathToolkit.gcd(48, -18) == 6
        assert MathToolkit.gcd(-48, -18) == 6


class TestLCM:
    """Test suite for lcm."""
    
    def test_basic_lcm(self) -> None:
        """Test basic LCM calculations."""
        assert MathToolkit.lcm(4, 6) == 12
        assert MathToolkit.lcm(21, 6) == 42
    
    def test_coprime(self) -> None:
        """Test coprime numbers."""
        assert MathToolkit.lcm(5, 7) == 35
    
    def test_one_is_multiple(self) -> None:
        """Test when one number is multiple of other."""
        assert MathToolkit.lcm(4, 12) == 12
    
    def test_zero(self) -> None:
        """Test with zero."""
        assert MathToolkit.lcm(5, 0) == 0
        assert MathToolkit.lcm(0, 5) == 0


class TestFactorial:
    """Test suite for factorial."""
    
    def test_small_factorials(self) -> None:
        """Test small factorial values."""
        assert MathToolkit.factorial(0) == 1
        assert MathToolkit.factorial(1) == 1
        assert MathToolkit.factorial(5) == 120
    
    def test_larger_factorial(self) -> None:
        """Test larger factorial."""
        assert MathToolkit.factorial(10) == 3628800
    
    def test_negative_raises_error(self) -> None:
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError):
            MathToolkit.factorial(-1)


class TestFibonacci:
    """Test suite for fibonacci."""
    
    def test_base_cases(self) -> None:
        """Test base cases."""
        assert MathToolkit.fibonacci(0) == 0
        assert MathToolkit.fibonacci(1) == 1
    
    def test_small_values(self) -> None:
        """Test small Fibonacci values."""
        assert MathToolkit.fibonacci(2) == 1
        assert MathToolkit.fibonacci(3) == 2
        assert MathToolkit.fibonacci(4) == 3
        assert MathToolkit.fibonacci(5) == 5
        assert MathToolkit.fibonacci(10) == 55
    
    def test_negative_raises_error(self) -> None:
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError):
            MathToolkit.fibonacci(-1)


class TestIsPerfectSquare:
    """Test suite for is_perfect_square."""
    
    def test_perfect_squares(self) -> None:
        """Test perfect squares."""
        assert MathToolkit.is_perfect_square(0) is True
        assert MathToolkit.is_perfect_square(1) is True
        assert MathToolkit.is_perfect_square(4) is True
        assert MathToolkit.is_perfect_square(16) is True
        assert MathToolkit.is_perfect_square(25) is True
    
    def test_non_perfect_squares(self) -> None:
        """Test non-perfect squares."""
        assert MathToolkit.is_perfect_square(2) is False
        assert MathToolkit.is_perfect_square(3) is False
        assert MathToolkit.is_perfect_square(15) is False
        assert MathToolkit.is_perfect_square(26) is False
    
    def test_negative(self) -> None:
        """Test negative numbers."""
        assert MathToolkit.is_perfect_square(-4) is False
