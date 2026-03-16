"""Tests for Problem 02: Payment Processor with Fakes."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

import pytest

from week07_real_world.solutions.day02.problem_02_payment_processor_with_fakes import (
    InMemoryPaymentGateway,
    PaymentDetails,
    PaymentProcessor,
    PaymentResult,
    PaymentStatus,
)


class TestInMemoryPaymentGateway:
    """Tests for the fake payment gateway."""
    
    def test_process_payment_approved_by_default(self) -> None:
        """Should approve payment when default_approve is True."""
        gateway = InMemoryPaymentGateway(default_approve=True)
        details = PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        result = gateway.process_payment(details)
        
        assert result.status == PaymentStatus.APPROVED
        assert result.amount_charged == Decimal("100.00")
        assert result.is_success is True
    
    def test_process_payment_declined_when_default_false(self) -> None:
        """Should decline when default_approve is False."""
        gateway = InMemoryPaymentGateway(default_approve=False)
        details = PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        result = gateway.process_payment(details)
        
        assert result.status == PaymentStatus.DECLINED
        assert result.is_success is False
    
    def test_process_payment_declines_for_decline_tokens(self) -> None:
        """Should decline for tokens in decline_tokens set."""
        gateway = InMemoryPaymentGateway(
            default_approve=True,
            decline_tokens={"tok_bad"}
        )
        details = PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_bad"
        )
        
        result = gateway.process_payment(details)
        
        assert result.status == PaymentStatus.DECLINED
    
    def test_process_payment_validates_positive_amount(self) -> None:
        """Should decline for non-positive amounts."""
        gateway = InMemoryPaymentGateway()
        
        result = gateway.process_payment(PaymentDetails(
            amount=Decimal("0"),
            currency="USD",
            card_token="tok_visa"
        ))
        
        assert result.status == PaymentStatus.DECLINED
        assert "zero" in result.error_message.lower()
    
    def test_process_payment_validates_currency_format(self) -> None:
        """Should decline for invalid currency codes."""
        gateway = InMemoryPaymentGateway()
        
        result = gateway.process_payment(PaymentDetails(
            amount=Decimal("100.00"),
            currency="US",  # Too short
            card_token="tok_visa"
        ))
        
        assert result.status == PaymentStatus.DECLINED
    
    def test_transaction_stored_after_processing(self) -> None:
        """Should store transaction for later retrieval."""
        gateway = InMemoryPaymentGateway()
        details = PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        result = gateway.process_payment(details)
        stored = gateway.get_transaction(result.transaction_id)
        
        assert stored is not None
        assert stored.transaction_id == result.transaction_id
    
    def test_get_transaction_returns_none_for_unknown(self) -> None:
        """Should return None for unknown transaction ID."""
        gateway = InMemoryPaymentGateway()
        
        result = gateway.get_transaction(UUID("12345678-1234-5678-1234-567812345678"))
        
        assert result is None


class TestInMemoryPaymentGatewayRefunds:
    """Tests for refund functionality."""
    
    @pytest.fixture
    def approved_payment(self) -> tuple[InMemoryPaymentGateway, PaymentResult]:
        """Fixture providing gateway with an approved payment."""
        gateway = InMemoryPaymentGateway()
        details = PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        payment = gateway.process_payment(details)
        return gateway, payment
    
    def test_full_refund(self, approved_payment: tuple[InMemoryPaymentGateway, PaymentResult]) -> None:
        """Should process full refund when amount is None."""
        gateway, payment = approved_payment
        
        result = gateway.refund_payment(payment.transaction_id)
        
        assert result.status == PaymentStatus.REFUNDED
        assert result.amount_charged == Decimal("100.00")
    
    def test_partial_refund(self, approved_payment: tuple[InMemoryPaymentGateway, PaymentResult]) -> None:
        """Should process partial refund."""
        gateway, payment = approved_payment
        
        result = gateway.refund_payment(payment.transaction_id, Decimal("30.00"))
        
        assert result.status == PaymentStatus.REFUNDED
        assert result.amount_charged == Decimal("30.00")
    
    def test_multiple_partial_refunds(self, approved_payment: tuple[InMemoryPaymentGateway, PaymentResult]) -> None:
        """Should allow multiple partial refunds."""
        gateway, payment = approved_payment
        
        refund1 = gateway.refund_payment(payment.transaction_id, Decimal("30.00"))
        refund2 = gateway.refund_payment(payment.transaction_id, Decimal("40.00"))
        
        assert refund1.amount_charged == Decimal("30.00")
        assert refund2.amount_charged == Decimal("40.00")
        
        # Payment should only transition to REFUNDED when fully refunded
        updated = gateway.get_transaction(payment.transaction_id)
        assert updated.status == PaymentStatus.APPROVED  # Not fully refunded yet
    
    def test_refund_exceeding_balance_fails(self, approved_payment: tuple[InMemoryPaymentGateway, PaymentResult]) -> None:
        """Should decline refund exceeding original amount."""
        gateway, payment = approved_payment
        
        # First refund $60
        gateway.refund_payment(payment.transaction_id, Decimal("60.00"))
        
        # Try to refund another $60 (exceeds remaining $40)
        result = gateway.refund_payment(payment.transaction_id, Decimal("60.00"))
        
        assert result.status == PaymentStatus.DECLINED
        assert "exceeds" in result.error_message.lower()
    
    def test_refund_unknown_transaction_fails(self) -> None:
        """Should decline refund for unknown transaction."""
        gateway = InMemoryPaymentGateway()
        
        result = gateway.refund_payment(UUID("12345678-1234-5678-1234-567812345678"))
        
        assert result.status == PaymentStatus.DECLINED
        assert "not found" in result.error_message.lower()


class TestPaymentProcessor:
    """Tests for PaymentProcessor service."""
    
    @pytest.fixture
    def processor(self) -> PaymentProcessor:
        """Fixture providing configured payment processor."""
        gateway = InMemoryPaymentGateway(default_approve=True)
        return PaymentProcessor(gateway)
    
    def test_charge_success(self, processor: PaymentProcessor) -> None:
        """Should successfully charge card."""
        result = processor.charge(
            amount=Decimal("99.99"),
            currency="USD",
            card_token="tok_visa"
        )
        
        assert result.is_success is True
        assert result.status == PaymentStatus.APPROVED
    
    def test_charge_validates_positive_amount(self, processor: PaymentProcessor) -> None:
        """Should raise ValueError for non-positive amount."""
        with pytest.raises(ValueError, match="greater than zero"):
            processor.charge(
                amount=Decimal("0"),
                currency="USD",
                card_token="tok_visa"
            )
    
    def test_charge_validates_currency_format(self, processor: PaymentProcessor) -> None:
        """Should raise ValueError for invalid currency."""
        with pytest.raises(ValueError, match="3-letter"):
            processor.charge(
                amount=Decimal("100.00"),
                currency="US",
                card_token="tok_visa"
            )
    
    def test_charge_normalizes_currency_to_uppercase(self, processor: PaymentProcessor) -> None:
        """Should convert currency to uppercase."""
        result = processor.charge(
            amount=Decimal("100.00"),
            currency="usd",  # lowercase
            card_token="tok_visa"
        )
        
        assert result.is_success is True
    
    def test_refund_full_amount(self, processor: PaymentProcessor) -> None:
        """Should refund full amount when amount not specified."""
        charge_result = processor.charge(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        refund_result = processor.refund(charge_result.transaction_id)
        
        assert refund_result.status == PaymentStatus.REFUNDED
        assert refund_result.amount_charged == Decimal("100.00")
    
    def test_refund_partial_amount(self, processor: PaymentProcessor) -> None:
        """Should refund specified amount."""
        charge_result = processor.charge(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        refund_result = processor.refund(charge_result.transaction_id, Decimal("50.00"))
        
        assert refund_result.amount_charged == Decimal("50.00")
    
    def test_get_payment_status_found(self, processor: PaymentProcessor) -> None:
        """Should return status for existing payment."""
        charge_result = processor.charge(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        )
        
        status = processor.get_payment_status(charge_result.transaction_id)
        
        assert status == PaymentStatus.APPROVED
    
    def test_get_payment_status_not_found(self, processor: PaymentProcessor) -> None:
        """Should return None for unknown payment."""
        status = processor.get_payment_status(UUID("12345678-1234-5678-1234-567812345678"))
        
        assert status is None


class TestPaymentProcessorWithDeclines:
    """Tests for processor behavior with declined payments."""
    
    def test_declined_charge_returns_result_not_raises(self) -> None:
        """Should return declined result rather than raising exception."""
        gateway = InMemoryPaymentGateway(
            default_approve=True,
            decline_tokens={"tok_decline"}
        )
        processor = PaymentProcessor(gateway)
        
        result = processor.charge(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_decline"
        )
        
        assert result.is_success is False
        assert result.status == PaymentStatus.DECLINED


class TestFakeGatewayIsolation:
    """Tests demonstrating test isolation with fake."""
    
    def test_one_test_does_not_affect_another(self) -> None:
        """Each test gets fresh gateway state."""
        gateway1 = InMemoryPaymentGateway()
        gateway2 = InMemoryPaymentGateway()
        
        # Add transaction to gateway1
        result1 = gateway1.process_payment(PaymentDetails(
            amount=Decimal("100.00"),
            currency="USD",
            card_token="tok_visa"
        ))
        
        # gateway2 should not see gateway1's transactions
        assert gateway2.get_transaction(result1.transaction_id) is None
    
    def test_decline_tokens_configurable_per_instance(self) -> None:
        """Each gateway instance can have different decline behavior."""
        gateway1 = InMemoryPaymentGateway(decline_tokens={"tok_1"})
        gateway2 = InMemoryPaymentGateway(decline_tokens={"tok_2"})
        
        result1 = gateway1.process_payment(PaymentDetails(
            amount=Decimal("100.00"), currency="USD", card_token="tok_1"
        ))
        result2 = gateway2.process_payment(PaymentDetails(
            amount=Decimal("100.00"), currency="USD", card_token="tok_1"
        ))
        
        assert result1.status == PaymentStatus.DECLINED
        assert result2.status == PaymentStatus.APPROVED
