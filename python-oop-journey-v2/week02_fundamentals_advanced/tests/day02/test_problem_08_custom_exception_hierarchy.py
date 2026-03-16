"""Tests for Problem 08: Custom Exception Hierarchy."""

from __future__ import annotations

import pytest

from week02_fundamentals_advanced.solutions.day02.problem_08_custom_exception_hierarchy import (
    InvalidCardError,
    NetworkError,
    PaymentDeclinedError,
    PaymentError,
    process_payment,
)


def test_payment_error_inheritance() -> None:
    """Test exception hierarchy."""
    assert issubclass(PaymentDeclinedError, PaymentError)
    assert issubclass(InvalidCardError, PaymentError)
    assert issubclass(NetworkError, PaymentError)
    assert issubclass(PaymentError, Exception)


def test_payment_error_with_message() -> None:
    """Test exceptions accept message parameter."""
    error = PaymentError("Something went wrong")
    assert "Something went wrong" in str(error)


def test_payment_error_with_code() -> None:
    """Test exceptions accept code parameter."""
    error = PaymentError("Declined", code="DECLINED_001")
    assert error.code == "DECLINED_001"
    assert error.message == "Declined"


def test_process_payment_success() -> None:
    """Test successful payment processing."""
    result = process_payment("1234-5678", 100.0)
    assert "Payment of 100.0 processed successfully" == result


def test_process_payment_empty_card() -> None:
    """Test empty card number raises InvalidCardError."""
    with pytest.raises(InvalidCardError) as exc_info:
        process_payment("", 100.0)
    assert "Invalid card number" in str(exc_info.value)


def test_process_payment_none_card() -> None:
    """Test None card number raises InvalidCardError."""
    with pytest.raises(InvalidCardError):
        process_payment(None, 100.0)  # type: ignore[arg-type]


def test_process_payment_exceeds_limit() -> None:
    """Test amount over 1000 raises PaymentDeclinedError."""
    with pytest.raises(PaymentDeclinedError) as exc_info:
        process_payment("1234-5678", 1001.0)
    assert "exceeds limit" in str(exc_info.value)


def test_process_payment_network_error() -> None:
    """Test card containing 'network_error' raises NetworkError."""
    with pytest.raises(NetworkError) as exc_info:
        process_payment("network_error_card", 50.0)
    assert "Network connection failed" in str(exc_info.value)


def test_catch_with_base_class() -> None:
    """Test that child exceptions can be caught with base class."""
    for error_class in [PaymentDeclinedError, InvalidCardError, NetworkError]:
        try:
            raise error_class("test")
        except PaymentError:
            pass  # Should be caught


def test_payment_declined_not_invalid_card() -> None:
    """Test PaymentDeclinedError is not an InvalidCardError."""
    assert not issubclass(PaymentDeclinedError, InvalidCardError)
    assert not issubclass(InvalidCardError, PaymentDeclinedError)
