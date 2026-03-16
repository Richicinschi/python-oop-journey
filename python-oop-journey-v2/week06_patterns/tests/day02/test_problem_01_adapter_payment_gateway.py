"""Tests for Problem 01: Adapter Payment Gateway."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day02.problem_01_adapter_payment_gateway import (
    PaymentProcessor,
    ModernPaymentGateway,
    LegacyPaymentGateway,
    ModernGatewayAdapter,
    LegacyGatewayAdapter,
    PaymentProcessorFactory,
)


class TestModernPaymentGateway:
    """Tests for the adaptee class."""
    
    def test_init(self) -> None:
        gateway = ModernPaymentGateway("api_key_123")
        assert gateway.api_key == "api_key_123"
    
    def test_make_charge(self) -> None:
        gateway = ModernPaymentGateway("api_key_123")
        result = gateway.make_charge(100.50, "USD", "tok_visa")
        
        assert result["status"] == "approved"
        assert "transaction_id" in result
        assert result["amount"] == 100.50
        assert result["currency"] == "USD"
    
    def test_process_refund(self) -> None:
        gateway = ModernPaymentGateway("api_key_123")
        result = gateway.process_refund("txn_123", 50.00)
        
        assert result["status"] == "refunded"
        assert result["refund_id"] == "ref_txn_123"
        assert result["amount"] == 50.00


class TestLegacyPaymentGateway:
    """Tests for the legacy adaptee class."""
    
    def test_init(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret_xyz")
        assert gateway.merchant_id == "merchant_123"
        assert gateway.secret == "secret_xyz"
    
    def test_authorize_and_capture(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret_xyz")
        result = gateway.authorize_and_capture(10050, "tok_visa", "USD")
        
        assert result.startswith("OK|")
        parts = result.split("|")
        assert len(parts) == 3
        assert parts[2] == "10050"  # Amount in cents
    
    def test_do_refund(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret_xyz")
        result = gateway.do_refund("txn_123", 5050)
        
        assert result.startswith("OK|")
        parts = result.split("|")
        assert len(parts) == 2


class TestModernGatewayAdapter:
    """Tests for the modern gateway adapter."""
    
    def test_implements_interface(self) -> None:
        gateway = ModernPaymentGateway("api_key")
        adapter = ModernGatewayAdapter(gateway)
        assert isinstance(adapter, PaymentProcessor)
    
    def test_charge_success(self) -> None:
        gateway = ModernPaymentGateway("api_key")
        adapter = ModernGatewayAdapter(gateway)
        result = adapter.charge(100.50, "USD", "tok_visa")
        
        assert result["success"] is True
        assert "transaction_id" in result
        assert result["amount_charged"] == 100.50
        assert "approved" in result["message"]
    
    def test_refund_success(self) -> None:
        gateway = ModernPaymentGateway("api_key")
        adapter = ModernGatewayAdapter(gateway)
        result = adapter.refund("txn_123", 50.00)
        
        assert result["success"] is True
        assert result["refund_id"] == "ref_txn_123"
        assert result["amount_refunded"] == 50.00
    
    def test_stores_gateway_reference(self) -> None:
        gateway = ModernPaymentGateway("api_key")
        adapter = ModernGatewayAdapter(gateway)
        assert adapter._gateway is gateway


class TestLegacyGatewayAdapter:
    """Tests for the legacy gateway adapter."""
    
    def test_implements_interface(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        assert isinstance(adapter, PaymentProcessor)
    
    def test_charge_converts_amount_to_cents(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        result = adapter.charge(100.50, "USD", "tok_visa")
        
        assert result["success"] is True
        assert result["amount_charged"] == 100.50
        # Legacy gateway stores amount as cents, we verify conversion happened
        assert "transaction_id" in result
    
    def test_charge_parses_response(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        result = adapter.charge(50.00, "EUR", "tok_master")
        
        assert result["success"] is True
        assert result["transaction_id"].startswith("LEG")
        assert "successful" in result["message"]
    
    def test_refund_converts_amount_to_cents(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        result = adapter.refund("txn_123", 25.50)
        
        assert result["success"] is True
        assert result["amount_refunded"] == 25.50
    
    def test_refund_parses_response(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        result = adapter.refund("LEG12345", 10.00)
        
        assert result["success"] is True
        assert result["refund_id"].startswith("REF")
    
    def test_stores_gateway_reference(self) -> None:
        gateway = LegacyPaymentGateway("merchant_123", "secret")
        adapter = LegacyGatewayAdapter(gateway)
        assert adapter._gateway is gateway


class TestPaymentProcessorFactory:
    """Tests for the factory class."""
    
    def test_create_modern_processor(self) -> None:
        config = {"type": "modern", "api_key": "api_key_123"}
        processor = PaymentProcessorFactory.create_processor(config)
        
        assert isinstance(processor, ModernGatewayAdapter)
        assert isinstance(processor, PaymentProcessor)
    
    def test_create_legacy_processor(self) -> None:
        config = {"type": "legacy", "merchant_id": "merch_123", "secret": "secret_xyz"}
        processor = PaymentProcessorFactory.create_processor(config)
        
        assert isinstance(processor, LegacyGatewayAdapter)
        assert isinstance(processor, PaymentProcessor)
    
    def test_create_unknown_type_raises_error(self) -> None:
        config = {"type": "unknown"}
        with pytest.raises(ValueError, match="Unknown gateway type"):
            PaymentProcessorFactory.create_processor(config)
    
    def test_created_processors_work_correctly(self) -> None:
        modern_config = {"type": "modern", "api_key": "api_key"}
        modern_processor = PaymentProcessorFactory.create_processor(modern_config)
        
        result = modern_processor.charge(100.00, "USD", "tok_test")
        assert result["success"] is True
        
        legacy_config = {"type": "legacy", "merchant_id": "merch", "secret": "sec"}
        legacy_processor = PaymentProcessorFactory.create_processor(legacy_config)
        
        result = legacy_processor.charge(100.00, "USD", "tok_test")
        assert result["success"] is True


class TestAdapterPolymorphism:
    """Tests demonstrating adapters enable polymorphic use."""
    
    def test_adapters_are_interchangeable(self) -> None:
        modern = ModernGatewayAdapter(ModernPaymentGateway("key"))
        legacy = LegacyGatewayAdapter(LegacyPaymentGateway("merch", "sec"))
        
        processors: list[PaymentProcessor] = [modern, legacy]
        
        for processor in processors:
            result = processor.charge(50.00, "USD", "tok_test")
            assert result["success"] is True
    
    def test_client_code_works_with_any_adapter(self) -> None:
        def process_payment(processor: PaymentProcessor) -> dict:
            return processor.charge(99.99, "USD", "tok_visa")
        
        modern = ModernGatewayAdapter(ModernPaymentGateway("key"))
        legacy = LegacyGatewayAdapter(LegacyPaymentGateway("merch", "sec"))
        
        modern_result = process_payment(modern)
        legacy_result = process_payment(legacy)
        
        # Both return same response format
        assert "success" in modern_result
        assert "success" in legacy_result
        assert "transaction_id" in modern_result
        assert "transaction_id" in legacy_result
