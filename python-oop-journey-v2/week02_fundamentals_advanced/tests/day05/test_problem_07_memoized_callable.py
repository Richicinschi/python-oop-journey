"""Tests for Problem 07: Memoized Callable."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_07_memoized_callable import (
    memoize,
    MemoizedCallable,
    FibonacciMemoized,
)


class TestMemoize:
    """Tests for memoize decorator."""

    def test_basic_memoization(self) -> None:
        """Test that results are cached."""
        call_count = 0

        @memoize
        def double(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        assert double(5) == 10
        assert call_count == 1

        # Second call with same arg - should use cache
        assert double(5) == 10
        assert call_count == 1  # Not incremented

        # Different arg - should call function
        assert double(3) == 6
        assert call_count == 2

    def test_fibonacci_memoization(self) -> None:
        """Test memoization with recursive Fibonacci."""
        call_count = 0

        @memoize
        def fib(n: int) -> int:
            nonlocal call_count
            call_count += 1
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)

        result = fib(10)
        assert result == 55
        # Without memoization would be 177 calls
        # With memoization should be only 11 calls (0-10)
        assert call_count == 11

    def test_multiple_args(self) -> None:
        """Test memoization with multiple arguments."""
        call_count = 0

        @memoize
        def add(a: int, b: int) -> int:
            nonlocal call_count
            call_count += 1
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3  # Cached
        assert call_count == 1

        assert add(2, 1) == 3  # Different order - new call
        assert call_count == 2

    def test_with_kwargs(self) -> None:
        """Test memoization with keyword arguments."""
        call_count = 0

        @memoize
        def greet(name: str, greeting: str = "Hello") -> str:
            nonlocal call_count
            call_count += 1
            return f"{greeting}, {name}!"

        assert greet("Alice") == "Hello, Alice!"
        assert greet("Alice") == "Hello, Alice!"  # Cached
        assert call_count == 1

        assert greet("Bob", greeting="Hi") == "Hi, Bob!"
        assert call_count == 2

    def test_cache_exposure(self) -> None:
        """Test that cache can be accessed and cleared."""
        @memoize
        def square(x: int) -> int:
            return x ** 2

        square(5)
        square(3)

        assert len(square._cache) == 2  # type: ignore

        square.clear_cache()  # type: ignore
        assert len(square._cache) == 0  # type: ignore


class TestMemoizedCallable:
    """Tests for MemoizedCallable class."""

    def test_basic_usage(self) -> None:
        """Test basic memoized callable usage."""
        call_count = 0

        def double(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        memoized = MemoizedCallable(double)

        assert memoized(5) == 10
        assert memoized(5) == 10  # Cached
        assert call_count == 1

        assert memoized(3) == 6
        assert call_count == 2

    def test_get_stats(self) -> None:
        """Test get_stats method."""
        def slow_func(x: int) -> int:
            return x * 2

        memoized = MemoizedCallable(slow_func)

        # No calls yet
        stats = memoized.get_stats()
        assert stats["cache_size"] == 0
        assert stats["call_count"] == 0

        # Make some calls
        memoized(1)
        memoized(2)
        memoized(1)  # Cached

        stats = memoized.get_stats()
        assert stats["cache_size"] == 2
        assert stats["call_count"] == 2

    def test_clear_cache(self) -> None:
        """Test clear_cache method."""
        def func(x: int) -> int:
            return x

        memoized = MemoizedCallable(func)

        memoized(1)
        memoized(2)

        assert memoized.get_stats()["cache_size"] == 2

        memoized.clear_cache()

        assert memoized.get_stats()["cache_size"] == 0
        assert memoized.get_stats()["call_count"] == 0

    def test_with_multiple_args(self) -> None:
        """Test with multiple positional arguments."""
        def add(a: int, b: int, c: int) -> int:
            return a + b + c

        memoized = MemoizedCallable(add)

        assert memoized(1, 2, 3) == 6
        assert memoized(1, 2, 3) == 6  # Cached

        stats = memoized.get_stats()
        assert stats["call_count"] == 1
        assert stats["cache_size"] == 1


class TestFibonacciMemoized:
    """Tests for FibonacciMemoized class."""

    def test_base_cases(self) -> None:
        """Test base cases."""
        fib = FibonacciMemoized()

        assert fib(0) == 0
        assert fib(1) == 1

    def test_small_values(self) -> None:
        """Test small Fibonacci numbers."""
        fib = FibonacciMemoized()

        assert fib(2) == 1
        assert fib(3) == 2
        assert fib(4) == 3
        assert fib(5) == 5
        assert fib(6) == 8

    def test_larger_values(self) -> None:
        """Test larger Fibonacci numbers."""
        fib = FibonacciMemoized()

        assert fib(10) == 55
        assert fib(20) == 6765
        assert fib(30) == 832040

    def test_negative_raises_error(self) -> None:
        """Test that negative input raises ValueError."""
        fib = FibonacciMemoized()

        with pytest.raises(ValueError, match="non-negative"):
            fib(-1)

    def test_sequence(self) -> None:
        """Test sequence generation."""
        fib = FibonacciMemoized()

        result = fib.sequence(10)
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_sequence_zero_count(self) -> None:
        """Test sequence with zero count."""
        fib = FibonacciMemoized()

        result = fib.sequence(0)
        assert result == []

    def test_sequence_negative_count(self) -> None:
        """Test sequence with negative count."""
        fib = FibonacciMemoized()

        result = fib.sequence(-5)
        assert result == []

    def test_caching(self) -> None:
        """Test that results are cached between calls."""
        fib = FibonacciMemoized()

        # First call
        fib(20)
        first_count = fib._call_count

        # Second call - should use cache
        fib(15)
        # 15 was calculated as part of calculating 20
        assert fib._call_count == first_count

    def test_sequence_uses_cache(self) -> None:
        """Test that sequence generation uses cache."""
        fib = FibonacciMemoized()

        # Generate sequence
        fib.sequence(20)
        count_after_sequence = fib._call_count

        # Getting a smaller number should use cache
        fib(10)
        assert fib._call_count == count_after_sequence
