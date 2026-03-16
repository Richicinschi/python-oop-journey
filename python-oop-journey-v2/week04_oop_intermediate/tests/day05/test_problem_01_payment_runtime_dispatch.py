"""Tests for Problem 01: Payment Runtime Dispatch."""

from __future__ import annotations

import pytest
from week04_oop_intermediate.solutions.day05.problem_01_payment_runtime_dispatch import (
    CreditCardPayment,
    CryptoPayment,
    PayPalPayment,
    PaymentMethod,
    PaymentProcessor,
)


class TestCreditCardPayment:
    """Tests for CreditCardPayment class."""

    def test_valid_card(self) -> None:
        payment = CreditCardPayment("1234567890123456", "12/25", "123")
        assert payment.validate() is True

    def test_invalid_card_number_too_short(self) -> None:
        payment = CreditCardPayment("123456789012345", "12/25", "123")
        assert payment.validate() is False

    def test_invalid_card_number_non_numeric(self) -> None:
        payment = CreditCardPayment("123456789012345a", "12/25", "123")
        assert payment.validate() is False

    def test_invalid_expiry_format(self) -> None:
        payment = CreditCardPayment("1234567890123456", "12-25", "123")
        assert payment.validate() is False

    def test_invalid_cvv(self) -> None:
        payment = CreditCardPayment("1234567890123456", "12/25", "12")
        assert payment.validate() is False

    def test_process_payment_success(self) -> None:
        payment = CreditCardPayment("1234567890123456", "12/25", "123")
        result = payment.process_payment(100.0)
        assert result["success"] is True
        assert result["method"] == "Credit Card"
        assert result["amount"] == 100.0
        assert "transaction_id" in result
        assert "****3456" in result["message"]

    def test_process_payment_invalid_card(self) -> None:
        payment = CreditCardPayment("123", "12/25", "123")
        result = payment.process_payment(100.0)
        assert result["success"] is False
        assert "Invalid card details" in result["message"]

    def test_is_payment_method(self) -> None:
        payment = CreditCardPayment("1234567890123456", "12/25", "123")
        assert isinstance(payment, PaymentMethod)


class TestPayPalPayment:
    """Tests for PayPalPayment class."""

    def test_valid_paypal(self) -> None:
        payment = PayPalPayment("user@example.com", "password123")
        assert payment.validate() is True

    def test_invalid_email_no_at(self) -> None:
        payment = PayPalPayment("userexample.com", "password123")
        assert payment.validate() is False

    def test_invalid_email_no_dot(self) -> None:
        payment = PayPalPayment("user@examplecom", "password123")
        assert payment.validate() is False

    def test_invalid_token_too_short(self) -> None:
        payment = PayPalPayment("user@example.com", "short")
        assert payment.validate() is False

    def test_process_payment_success(self) -> None:
        payment = PayPalPayment("user@example.com", "password123")
        result = payment.process_payment(50.0)
        assert result["success"] is True
        assert result["method"] == "PayPal"
        assert "user@example.com" in result["message"]

    def test_is_payment_method(self) -> None:
        payment = PayPalPayment("user@example.com", "password123")
        assert isinstance(payment, PaymentMethod)


class TestCryptoPayment:
    """Tests for CryptoPayment class."""

    def test_valid_btc(self) -> None:
        payment = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC")
        assert payment.validate() is True

    def test_valid_eth(self) -> None:
        payment = CryptoPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "ETH")
        assert payment.validate() is True

    def test_invalid_wallet_too_short(self) -> None:
        payment = CryptoPayment("short", "BTC")
        assert payment.validate() is False

    def test_invalid_currency(self) -> None:
        payment = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "XYZ")
        assert payment.validate() is False

    def test_currency_case_insensitive(self) -> None:
        payment = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "btc")
        assert payment.validate() is True

    def test_supported_currencies(self) -> None:
        assert "BTC" in CryptoPayment.SUPPORTED_CURRENCIES
        assert "ETH" in CryptoPayment.SUPPORTED_CURRENCIES
        assert "LTC" in CryptoPayment.SUPPORTED_CURRENCIES

    def test_is_payment_method(self) -> None:
        payment = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC")
        assert isinstance(payment, PaymentMethod)


class TestPaymentProcessor:
    """Tests for PaymentProcessor class."""

    def test_process_credit_card(self) -> None:
        processor = PaymentProcessor()
        payment = CreditCardPayment("1234567890123456", "12/25", "123")
        result = processor.process(payment, 100.0)
        assert result["success"] is True
        assert len(processor.get_transaction_history()) == 1

    def test_process_paypal(self) -> None:
        processor = PaymentProcessor()
        payment = PayPalPayment("user@example.com", "password123")
        result = processor.process(payment, 50.0)
        assert result["success"] is True

    def test_process_crypto(self) -> None:
        processor = PaymentProcessor()
        payment = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC")
        result = processor.process(payment, 1.5)
        assert result["success"] is True

    def test_invalid_amount(self) -> None:
        processor = PaymentProcessor()
        payment = CreditCardPayment("1234567890123456", "12/25", "123")
        result = processor.process(payment, -10.0)
        assert result["success"] is False

    def test_transaction_history(self) -> None:
        processor = PaymentProcessor()
        processor.process(CreditCardPayment("1234567890123456", "12/25", "123"), 100.0)
        processor.process(PayPalPayment("user@example.com", "password123"), 50.0)
        history = processor.get_transaction_history()
        assert len(history) == 2

    def test_polymorphic_processing(self) -> None:
        """Test that processor works polymorphically with all payment types."""
        processor = PaymentProcessor()
        payments = [
            CreditCardPayment("1234567890123456", "12/25", "123"),
            PayPalPayment("user@example.com", "password123"),
            CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC"),
        ]
        for payment in payments:
            result = processor.process(payment, 10.0)
            assert result["success"] is True
            assert "method" in result
            assert "transaction_id" in result
