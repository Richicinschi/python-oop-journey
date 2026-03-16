"""Tests for Problem 06: Closure Counter."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day05.problem_06_closure_counter import (
    create_counter,
    create_multi_counter,
    create_rate_limiter,
    make_multiplier_of,
)


class TestCreateCounter:
    """Tests for create_counter function."""

    def test_default_counter(self) -> None:
        """Test counter with default start and step."""
        counter = create_counter()
        assert counter() == 0
        assert counter() == 1
        assert counter() == 2
        assert counter() == 3

    def test_custom_start(self) -> None:
        """Test counter with custom start value."""
        counter = create_counter(start=10)
        assert counter() == 10
        assert counter() == 11
        assert counter() == 12

    def test_custom_step(self) -> None:
        """Test counter with custom step."""
        counter = create_counter(step=5)
        assert counter() == 0
        assert counter() == 5
        assert counter() == 10

    def test_custom_start_and_step(self) -> None:
        """Test counter with custom start and step."""
        counter = create_counter(start=100, step=10)
        assert counter() == 100
        assert counter() == 110
        assert counter() == 120

    def test_multiple_counters_independent(self) -> None:
        """Test that multiple counters are independent."""
        counter1 = create_counter(start=0)
        counter2 = create_counter(start=100)

        assert counter1() == 0
        assert counter2() == 100
        assert counter1() == 1
        assert counter2() == 101
        assert counter1() == 2

    def test_negative_step(self) -> None:
        """Test counter with negative step (decrementing)."""
        counter = create_counter(start=10, step=-2)
        assert counter() == 10
        assert counter() == 8
        assert counter() == 6


class TestCreateMultiCounter:
    """Tests for create_multi_counter function."""

    def test_single_channel(self) -> None:
        """Test with single channel."""
        mc = create_multi_counter(1)
        assert mc(0) == 0
        assert mc(0) == 1
        assert mc(0) == 2

    def test_multiple_channels(self) -> None:
        """Test with multiple independent channels."""
        mc = create_multi_counter(3)

        # First call to each channel
        assert mc(0) == 0
        assert mc(1) == 0
        assert mc(2) == 0

        # Second call to each channel
        assert mc(0) == 1
        assert mc(1) == 1
        assert mc(2) == 1

    def test_interleaved_calls(self) -> None:
        """Test interleaved calls to different channels."""
        mc = create_multi_counter(2)

        assert mc(0) == 0
        assert mc(0) == 1
        assert mc(1) == 0
        assert mc(0) == 2
        assert mc(1) == 1
        assert mc(1) == 2

    def test_invalid_channel(self) -> None:
        """Test that invalid channel raises error."""
        mc = create_multi_counter(3)

        with pytest.raises(ValueError):
            mc(3)  # Out of range

        with pytest.raises(ValueError):
            mc(-1)  # Negative


class TestCreateRateLimiter:
    """Tests for create_rate_limiter function."""

    def test_within_limit(self) -> None:
        """Test calls within rate limit."""
        limiter = create_rate_limiter(3, 5)

        assert limiter() is True
        assert limiter() is True
        assert limiter() is True

    def test_exceeds_limit(self) -> None:
        """Test that exceeding limit returns False."""
        limiter = create_rate_limiter(2, 5)

        assert limiter() is True
        assert limiter() is True
        assert limiter() is False
        assert limiter() is False

    def test_window_reset(self) -> None:
        """Test that window resets after window_seconds calls."""
        limiter = create_rate_limiter(2, 3)

        # First window - 3 calls allowed (but we only allow 2)
        assert limiter() is True   # Call 1 of window 1
        assert limiter() is True   # Call 2 of window 1
        assert limiter() is False  # Call 3 of window 1 - exceeded

        # After window_seconds (3) calls, window should reset
        # Call 4 starts a new window
        assert limiter() is True   # Call 1 of window 2
        assert limiter() is True   # Call 2 of window 2

    def test_single_call_window(self) -> None:
        """Test with window of 1 second."""
        limiter = create_rate_limiter(1, 1)

        assert limiter() is True   # Call 1 - allowed
        assert limiter() is True   # Window reset - allowed
        assert limiter() is True   # Window reset - allowed

    def test_high_limit(self) -> None:
        """Test with high call limit across multiple windows."""
        limiter = create_rate_limiter(10, 5)

        # First window: should allow 5 calls (window size is 5)
        for _ in range(5):
            assert limiter() is True

        # Next window: reset allows more calls
        for _ in range(5):
            assert limiter() is True

        # Now we're in a new window, 11th call should pass (new window)
        assert limiter() is True


class TestMakeMultiplierOf:
    """Tests for make_multiplier_of function."""

    def test_double(self) -> None:
        """Test creating a doubler."""
        double = make_multiplier_of(2)
        assert double(5) == 10
        assert double(0) == 0
        assert double(-3) == -6

    def test_triple(self) -> None:
        """Test creating a tripler."""
        triple = make_multiplier_of(3)
        assert triple(4) == 12
        assert triple(10) == 30

    def test_multiple_multipliers(self) -> None:
        """Test multiple independent multipliers."""
        double = make_multiplier_of(2)
        triple = make_multiplier_of(3)
        quadruple = make_multiplier_of(4)

        assert double(5) == 10
        assert triple(5) == 15
        assert quadruple(5) == 20

    def test_multiplier_by_zero(self) -> None:
        """Test multiplier of zero."""
        zero = make_multiplier_of(0)
        assert zero(100) == 0
        assert zero(-50) == 0

    def test_multiplier_by_one(self) -> None:
        """Test multiplier of one (identity)."""
        identity = make_multiplier_of(1)
        assert identity(42) == 42
        assert identity(-99) == -99

    def test_negative_multiplier(self) -> None:
        """Test negative multiplier."""
        neg = make_multiplier_of(-1)
        assert neg(5) == -5
        assert neg(-5) == 5
