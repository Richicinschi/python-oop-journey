"""Reference solution for Problem 01: Adapter Payment Gateway."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Target interface - the interface our client code expects."""
    
    @abstractmethod
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Process a charge transaction."""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Process a refund."""
        pass


class ModernPaymentGateway:
    """Adaptee - a modern payment gateway with its own interface."""
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    def make_charge(self, charge_amount: float, currency_code: str, token: str) -> dict:
        """Make a charge using modern gateway format."""
        # Simulate API call
        return {
            "status": "approved",
            "transaction_id": f"mod_{hash(token) % 1000000:06d}",
            "amount": charge_amount,
            "currency": currency_code
        }
    
    def process_refund(self, txn_id: str, refund_amount: float) -> dict:
        """Process refund using modern gateway format."""
        return {
            "status": "refunded",
            "refund_id": f"ref_{txn_id}",
            "amount": refund_amount
        }


class LegacyPaymentGateway:
    """Adaptee - a legacy payment gateway with an old interface."""
    
    def __init__(self, merchant_id: str, secret: str) -> None:
        self.merchant_id = merchant_id
        self.secret = secret
    
    def authorize_and_capture(self, amt_in_cents: int, cc_token: str, curr: str) -> str:
        """Legacy charge method - returns pipe-delimited string."""
        txn_id = f"LEG{hash(cc_token) % 100000:05d}"
        return f"OK|{txn_id}|{amt_in_cents}"
    
    def do_refund(self, original_txn: str, cents_to_refund: int) -> str:
        """Legacy refund method - returns pipe-delimited string."""
        refund_id = f"REF{hash(original_txn) % 100000:05d}"
        return f"OK|{refund_id}"


class ModernGatewayAdapter(PaymentProcessor):
    """Adapter for ModernPaymentGateway."""
    
    def __init__(self, gateway: ModernPaymentGateway) -> None:
        self._gateway = gateway
    
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Adapt charge call to modern gateway format."""
        response = self._gateway.make_charge(amount, currency, card_token)
        
        return {
            "success": response["status"] == "approved",
            "transaction_id": response["transaction_id"],
            "amount_charged": response["amount"],
            "message": f"Payment {response['status']}"
        }
    
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Adapt refund call to modern gateway format."""
        response = self._gateway.process_refund(transaction_id, amount)
        
        return {
            "success": response["status"] == "refunded",
            "refund_id": response["refund_id"],
            "amount_refunded": response["amount"],
            "message": f"Refund {response['status']}"
        }


class LegacyGatewayAdapter(PaymentProcessor):
    """Adapter for LegacyPaymentGateway."""
    
    def __init__(self, gateway: LegacyPaymentGateway) -> None:
        self._gateway = gateway
    
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Adapt charge call to legacy gateway format."""
        # Convert amount to cents for legacy API
        amt_in_cents = int(amount * 100)
        response = self._gateway.authorize_and_capture(amt_in_cents, card_token, currency)
        
        # Parse pipe-delimited response: "OK|txn_id|amount" or "ERR|code|msg"
        parts = response.split("|")
        success = parts[0] == "OK"
        
        return {
            "success": success,
            "transaction_id": parts[1] if success else "",
            "amount_charged": amount if success else 0.0,
            "message": "Payment successful" if success else f"Error: {parts[2]}"
        }
    
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Adapt refund call to legacy gateway format."""
        cents_to_refund = int(amount * 100)
        response = self._gateway.do_refund(transaction_id, cents_to_refund)
        
        parts = response.split("|")
        success = parts[0] == "OK"
        
        return {
            "success": success,
            "refund_id": parts[1] if success else "",
            "amount_refunded": amount if success else 0.0,
            "message": "Refund successful" if success else f"Error: {parts[1]}"
        }


class PaymentProcessorFactory:
    """Factory for creating the appropriate payment processor."""
    
    @staticmethod
    def create_processor(config: dict) -> PaymentProcessor:
        """Create appropriate processor based on config."""
        gateway_type = config.get("type")
        
        if gateway_type == "modern":
            gateway = ModernPaymentGateway(config["api_key"])
            return ModernGatewayAdapter(gateway)
        elif gateway_type == "legacy":
            gateway = LegacyPaymentGateway(config["merchant_id"], config["secret"])
            return LegacyGatewayAdapter(gateway)
        else:
            raise ValueError(f"Unknown gateway type: {gateway_type}")
