"""Tests for Problem 02: Payment Methods."""

from __future__ import annotations

import pytest

from week04_oop_intermediate.solutions.day02.problem_02_payment_methods import (
    CreditCard,
    Crypto,
    PaymentMethod,
    PayPal,
)


class TestPaymentMethod:
    """Tests for PaymentMethod base class."""

    def test_init_sets_attributes(self) -> None:
        """Test that all attributes are set correctly."""
        payment = PaymentMethod(100.0, "USD", "TXN12345")
        assert payment.amount == 100.0
        assert payment.currency == "USD"
        assert payment.transaction_id == "TXN12345"

    def test_init_validates_amount(self) -> None:
        """Test that non-positive amount raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            PaymentMethod(0, "USD", "TXN123")

    def test_init_validates_currency(self) -> None:
        """Test that empty currency raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            PaymentMethod(100, "", "TXN123")

    def test_init_uppercases_currency(self) -> None:
        """Test that currency is converted to uppercase."""
        payment = PaymentMethod(100, "eur", "TXN123")
        assert payment.currency == "EUR"

    def test_process_returns_expected_format(self) -> None:
        """Test process() returns correct format."""
        payment = PaymentMethod(100.0, "USD", "TXN12345")
        result = payment.process()
        assert result == "Processing USD 100.00 [TXN12345]"

    def test_process_formats_amount(self) -> None:
        """Test that amount is formatted with 2 decimal places."""
        payment = PaymentMethod(99.994, "USD", "TXN123")
        result = payment.process()
        assert "99.99" in result

    def test_get_details_returns_dict(self) -> None:
        """Test get_details() returns expected dictionary."""
        payment = PaymentMethod(100.0, "USD", "TXN12345")
        details = payment.get_details()
        assert details == {
            "amount": 100.0,
            "currency": "USD",
            "transaction_id": "TXN12345",
        }


class TestCreditCard:
    """Tests for CreditCard class."""

    def test_init_sets_all_attributes(self) -> None:
        """Test that all attributes are set."""
        cc = CreditCard(50.0, "EUR", "TXN67890", "1234", "12/25")
        assert cc.amount == 50.0
        assert cc.currency == "EUR"
        assert cc.card_last_four == "1234"
        assert cc.expiry_date == "12/25"

    def test_init_validates_card_last_four(self) -> None:
        """Test that invalid card_last_four raises ValueError."""
        with pytest.raises(ValueError, match="4 digits"):
            CreditCard(50.0, "USD", "TXN123", "123", "12/25")

    def test_init_validates_non_digit_card(self) -> None:
        """Test that non-digit card_last_four raises ValueError."""
        with pytest.raises(ValueError, match="4 digits"):
            CreditCard(50.0, "USD", "TXN123", "12ab", "12/25")

    def test_process_returns_expected_format(self) -> None:
        """Test process() includes masked card info."""
        cc = CreditCard(50.0, "EUR", "TXN67890", "1234", "12/25")
        result = cc.process()
        assert result == "Credit Card ****1234 processing Processing EUR 50.00 [TXN67890]"

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        cc = CreditCard(50.0, "EUR", "TXN67890", "1234", "12/25")
        details = cc.get_details()
        assert details["amount"] == 50.0
        assert details["card_last_four"] == "1234"
        assert details["expiry_date"] == "12/25"
        assert details["method"] == "credit_card"

    def test_inheritance_from_payment_method(self) -> None:
        """Test that CreditCard inherits from PaymentMethod."""
        assert issubclass(CreditCard, PaymentMethod)


class TestPayPal:
    """Tests for PayPal class."""

    def test_init_sets_email(self) -> None:
        """Test that email is set."""
        paypal = PayPal(75.0, "USD", "TXN11111", "user@example.com")
        assert paypal.email == "user@example.com"

    def test_init_validates_email_no_at(self) -> None:
        """Test that email without @ raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            PayPal(75.0, "USD", "TXN123", "invalid-email")

    def test_init_validates_empty_email(self) -> None:
        """Test that empty email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            PayPal(75.0, "USD", "TXN123", "")

    def test_process_returns_expected_format(self) -> None:
        """Test process() includes email."""
        paypal = PayPal(75.0, "USD", "TXN11111", "user@example.com")
        result = paypal.process()
        assert result == "PayPal (user@example.com) processing Processing USD 75.00 [TXN11111]"

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        paypal = PayPal(75.0, "USD", "TXN11111", "user@example.com")
        details = paypal.get_details()
        assert details["amount"] == 75.0
        assert details["email"] == "user@example.com"
        assert details["method"] == "paypal"

    def test_inheritance_from_payment_method(self) -> None:
        """Test that PayPal inherits from PaymentMethod."""
        assert issubclass(PayPal, PaymentMethod)


class TestCrypto:
    """Tests for Crypto class."""

    def test_init_sets_crypto_attributes(self) -> None:
        """Test that crypto attributes are set."""
        crypto = Crypto(1.5, "USD", "TXN22222", "1A2B3C4D", "BTC")
        assert crypto.crypto_currency == "BTC"
        assert crypto.wallet_address == "1A2B3C4D"

    def test_init_uppercases_crypto_currency(self) -> None:
        """Test that crypto_currency is uppercased."""
        crypto = Crypto(1.5, "USD", "TXN22222", "wallet", "btc")
        assert crypto.crypto_currency == "BTC"

    def test_init_validates_unsupported_currency(self) -> None:
        """Test that unsupported crypto raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported"):
            Crypto(1.5, "USD", "TXN123", "wallet", "XYZ")

    def test_process_shortens_long_wallet(self) -> None:
        """Test that long wallet addresses are shortened."""
        crypto = Crypto(1.5, "USD", "TXN22222", "1234567890ABCDEF", "BTC")
        result = crypto.process()
        assert "123456...CDEF" in result

    def test_process_keeps_short_wallet(self) -> None:
        """Test that short wallet addresses are kept as is."""
        crypto = Crypto(1.5, "USD", "TXN22222", "1A2B3C", "BTC")
        result = crypto.process()
        assert "to 1A2B3C" in result

    def test_get_details_extends_parent(self) -> None:
        """Test get_details() extends parent's dict."""
        crypto = Crypto(1.5, "USD", "TXN22222", "wallet123", "ETH")
        details = crypto.get_details()
        assert details["amount"] == 1.5
        assert details["wallet_address"] == "wallet123"
        assert details["crypto_currency"] == "ETH"
        assert details["method"] == "crypto"

    def test_supported_currencies_constant(self) -> None:
        """Test that SUPPORTED_CURRENCIES exists."""
        expected = ("BTC", "ETH", "LTC", "USDC", "USDT")
        assert Crypto.SUPPORTED_CURRENCIES == expected

    def test_inheritance_from_payment_method(self) -> None:
        """Test that Crypto inherits from PaymentMethod."""
        assert issubclass(Crypto, PaymentMethod)
