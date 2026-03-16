"""Tests for Problem 01: Payment Processor ABC."""

from __future__ import annotations

import pytest
from abc import ABC

from week04_oop_intermediate.solutions.day03.problem_01_payment_processor_abc import (
    PaymentProcessor,
    CreditCardProcessor,
    PayPalProcessor,
)


class TestPaymentProcessorABC:
    """Test suite for PaymentProcessor abstract base class."""
    
    def test_payment_processor_is_abstract(self) -> None:
        """Test that PaymentProcessor cannot be instantiated."""
        assert issubclass(PaymentProcessor, ABC)
        with pytest.raises(TypeError, match="abstract"):
            PaymentProcessor("merch_123")
    
    def test_payment_processor_has_abstract_methods(self) -> None:
        """Test that PaymentProcessor defines abstract methods."""
        assert hasattr(PaymentProcessor, 'process_payment')
        assert hasattr(PaymentProcessor, 'refund')
    
    def test_payment_processor_init_sets_merchant_id(self) -> None:
        """Test that __init__ sets merchant_id attribute."""
        # This tests the concrete init through a concrete subclass
        processor = CreditCardProcessor("merch_123")
        assert processor.merchant_id == "merch_123"


class TestCreditCardProcessor:
    """Test suite for CreditCardProcessor."""
    
    def test_initialization(self) -> None:
        """Test credit card processor initialization."""
        processor = CreditCardProcessor("merch_123", "stripe")
        assert processor.merchant_id == "merch_123"
        assert processor.gateway == "stripe"
    
    def test_initialization_default_gateway(self) -> None:
        """Test credit card processor with default gateway."""
        processor = CreditCardProcessor("merch_123")
        assert processor.gateway == "stripe"
    
    def test_process_payment_returns_dict(self) -> None:
        """Test process_payment returns transaction dict."""
        processor = CreditCardProcessor("merch_123")
        result = processor.process_payment(100.0, "USD")
        
        assert isinstance(result, dict)
        assert "transaction_id" in result
        assert "amount" in result
        assert "currency" in result
        assert "status" in result
    
    def test_process_payment_transaction_id_prefix(self) -> None:
        """Test transaction_id has 'cc_' prefix."""
        processor = CreditCardProcessor("merch_123")
        result = processor.process_payment(100.0, "USD")
        
        assert result["transaction_id"].startswith("cc_")
    
    def test_process_payment_amount_and_currency(self) -> None:
        """Test process_payment returns correct amount and currency."""
        processor = CreditCardProcessor("merch_123")
        result = processor.process_payment(250.5, "EUR")
        
        assert result["amount"] == 250.5
        assert result["currency"] == "EUR"
    
    def test_process_payment_includes_gateway(self) -> None:
        """Test process_payment includes gateway in result."""
        processor = CreditCardProcessor("merch_123", "braintree")
        result = processor.process_payment(100.0, "USD")
        
        assert result["gateway"] == "braintree"
    
    def test_refund_with_cc_transaction(self) -> None:
        """Test refund succeeds for cc_ prefixed transaction."""
        processor = CreditCardProcessor("merch_123")
        assert processor.refund("cc_abc123") is True
    
    def test_refund_with_non_cc_transaction(self) -> None:
        """Test refund fails for non-cc transaction."""
        processor = CreditCardProcessor("merch_123")
        assert processor.refund("pp_abc123") is False
        assert processor.refund("abc123") is False


class TestPayPalProcessor:
    """Test suite for PayPalProcessor."""
    
    def test_initialization(self) -> None:
        """Test PayPal processor initialization."""
        processor = PayPalProcessor("merch_123", "client_456")
        assert processor.merchant_id == "merch_123"
        assert processor.client_id == "client_456"
    
    def test_process_payment_returns_dict(self) -> None:
        """Test process_payment returns transaction dict."""
        processor = PayPalProcessor("merch_123", "client_456")
        result = processor.process_payment(100.0, "USD")
        
        assert isinstance(result, dict)
        assert "transaction_id" in result
        assert "amount" in result
        assert "currency" in result
        assert "status" in result
    
    def test_process_payment_transaction_id_prefix(self) -> None:
        """Test transaction_id has 'pp_' prefix."""
        processor = PayPalProcessor("merch_123", "client_456")
        result = processor.process_payment(100.0, "USD")
        
        assert result["transaction_id"].startswith("pp_")
    
    def test_process_payment_includes_client_id(self) -> None:
        """Test process_payment includes client_id in result."""
        processor = PayPalProcessor("merch_123", "client_456")
        result = processor.process_payment(100.0, "USD")
        
        assert result["client_id"] == "client_456"
    
    def test_refund_with_pp_transaction(self) -> None:
        """Test refund succeeds for pp_ prefixed transaction."""
        processor = PayPalProcessor("merch_123", "client_456")
        assert processor.refund("pp_abc123") is True
    
    def test_refund_with_non_pp_transaction(self) -> None:
        """Test refund fails for non-pp transaction."""
        processor = PayPalProcessor("merch_123", "client_456")
        assert processor.refund("cc_abc123") is False
        assert processor.refund("abc123") is False
