"""Tests for Problem 04: Bounded Withdrawal."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_04_bounded_withdrawal import (
    InsufficientFundsError,
    LimitExceededError,
    bounded_withdrawal,
)


def test_bounded_withdrawal_success() -> None:
    """Test successful withdrawal."""
    assert bounded_withdrawal(100, 50, 200) == 50
    assert bounded_withdrawal(1000, 100, 500) == 900
    assert bounded_withdrawal(50, 25, 100) == 25


def test_bounded_withdrawal_exact_balance() -> None:
    """Test withdrawal of exact balance."""
    assert bounded_withdrawal(100, 100, 200) == 0


def test_bounded_withdrawal_exact_limit() -> None:
    """Test withdrawal at exact limit."""
    assert bounded_withdrawal(1000, 200, 200) == 800


def test_bounded_withdrawal_insufficient_funds() -> None:
    """Test withdrawal exceeding balance raises InsufficientFundsError."""
    with pytest.raises(InsufficientFundsError) as exc_info:
        bounded_withdrawal(100, 150, 200)
    assert "Cannot withdraw 150" in str(exc_info.value)
    assert "balance is 100" in str(exc_info.value)


def test_bounded_withdrawal_exceeds_limit() -> None:
    """Test withdrawal exceeding limit raises LimitExceededError."""
    with pytest.raises(LimitExceededError) as exc_info:
        bounded_withdrawal(1000, 50, 40)
    assert "Cannot withdraw 50" in str(exc_info.value)
    assert "limit is 40" in str(exc_info.value)


def test_bounded_withdrawal_zero_amount() -> None:
    """Test zero withdrawal amount raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        bounded_withdrawal(100, 0, 200)
    assert "must be positive" in str(exc_info.value)


def test_bounded_withdrawal_negative_amount() -> None:
    """Test negative withdrawal amount raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        bounded_withdrawal(100, -10, 200)
    assert "must be positive" in str(exc_info.value)


def test_exception_types() -> None:
    """Test that custom exceptions are proper Exception subclasses."""
    assert issubclass(InsufficientFundsError, Exception)
    assert issubclass(LimitExceededError, Exception)
