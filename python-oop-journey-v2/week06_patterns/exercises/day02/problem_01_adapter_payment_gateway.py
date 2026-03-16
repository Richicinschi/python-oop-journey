"""Problem 01: Adapter Payment Gateway

Topic: Adapter Pattern
Difficulty: Medium

Create an adapter to make different payment gateways compatible with a unified interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Target interface - the interface our client code expects.
    
    This is the unified interface that all payment processors should implement.
    """
    
    @abstractmethod
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Process a charge transaction.
        
        Args:
            amount: The amount to charge
            currency: The currency code (e.g., 'USD', 'EUR')
            card_token: The payment card token
            
        Returns:
            Dictionary with transaction details:
            - success: bool
            - transaction_id: str
            - amount_charged: float
            - message: str
        """
        raise NotImplementedError("Implement charge method")
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Process a refund.
        
        Args:
            transaction_id: The original transaction ID
            amount: The amount to refund
            
        Returns:
            Dictionary with refund details
        """
        raise NotImplementedError("Implement refund method")


class ModernPaymentGateway:
    """Adaptee - a modern payment gateway with its own interface.
    
    This is a third-party class we cannot modify but need to adapt.
    """
    
    def __init__(self, api_key: str) -> None:
        """Initialize with API key.
        
        Args:
            api_key: The API key for authentication
        """
        self.api_key = api_key
    
    def make_charge(self, charge_amount: float, currency_code: str, token: str) -> dict:
        """Make a charge using modern gateway format.
        
        Args:
            charge_amount: Amount in decimal format
            currency_code: 3-letter currency code
            token: Card token
            
        Returns:
            Response dict with status and transaction info
        """
        raise NotImplementedError("Implement make_charge")
    
    def process_refund(self, txn_id: str, refund_amount: float) -> dict:
        """Process refund using modern gateway format.
        
        Args:
            txn_id: Transaction ID
            refund_amount: Amount to refund
            
        Returns:
            Response dict with status
        """
        raise NotImplementedError("Implement process_refund")


class LegacyPaymentGateway:
    """Adaptee - a legacy payment gateway with an old interface.
    
    This legacy system uses different parameter names and formats.
    """
    
    def __init__(self, merchant_id: str, secret: str) -> None:
        """Initialize with merchant credentials.
        
        Args:
            merchant_id: Merchant identifier
            secret: Secret key for signing
        """
        self.merchant_id = merchant_id
        self.secret = secret
    
    def authorize_and_capture(self, amt_in_cents: int, cc_token: str, curr: str) -> str:
        """Legacy charge method.
        
        Args:
            amt_in_cents: Amount in cents (integer)
            cc_token: Credit card token
            curr: Currency code
            
        Returns:
            String response format: "OK|txn_id|amount" or "ERR|error_code|message"
        """
        raise NotImplementedError("Implement authorize_and_capture")
    
    def do_refund(self, original_txn: str, cents_to_refund: int) -> str:
        """Legacy refund method.
        
        Args:
            original_txn: Original transaction reference
            cents_to_refund: Amount to refund in cents
            
        Returns:
            String response format: "OK|refund_id" or "ERR|error_code"
        """
        raise NotImplementedError("Implement do_refund")


class ModernGatewayAdapter(PaymentProcessor):
    """Adapter for ModernPaymentGateway to work with PaymentProcessor interface.
    
    Converts the target interface (PaymentProcessor) calls to adaptee 
    (ModernPaymentGateway) calls.
    """
    
    def __init__(self, gateway: ModernPaymentGateway) -> None:
        """Initialize with the modern gateway to adapt.
        
        Args:
            gateway: The ModernPaymentGateway instance to wrap
        """
        raise NotImplementedError("Implement __init__")
    
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Adapt charge call to modern gateway format.
        
        Args:
            amount: Amount in decimal
            currency: Currency code
            card_token: Card token
            
        Returns:
            Standardized response dict
        """
        raise NotImplementedError("Implement charge")
    
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Adapt refund call to modern gateway format.
        
        Args:
            transaction_id: Transaction ID
            amount: Amount to refund
            
        Returns:
            Standardized response dict
        """
        raise NotImplementedError("Implement refund")


class LegacyGatewayAdapter(PaymentProcessor):
    """Adapter for LegacyPaymentGateway to work with PaymentProcessor interface.
    
    Converts PaymentProcessor calls to legacy format and parses legacy responses.
    Handles conversion between cents and decimal amounts.
    """
    
    def __init__(self, gateway: LegacyPaymentGateway) -> None:
        """Initialize with the legacy gateway to adapt.
        
        Args:
            gateway: The LegacyPaymentGateway instance to wrap
        """
        raise NotImplementedError("Implement __init__")
    
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Adapt charge call to legacy gateway format.
        
        Converts amount to cents and parses pipe-delimited response.
        
        Args:
            amount: Amount in decimal
            currency: Currency code
            card_token: Card token
            
        Returns:
            Standardized response dict
        """
        raise NotImplementedError("Implement charge")
    
    def refund(self, transaction_id: str, amount: float) -> dict:
        """Adapt refund call to legacy gateway format.
        
        Converts amount to cents and parses pipe-delimited response.
        
        Args:
            transaction_id: Transaction ID
            amount: Amount to refund
            
        Returns:
            Standardized response dict
        """
        raise NotImplementedError("Implement refund")


class PaymentProcessorFactory:
    """Factory for creating the appropriate payment processor.
    
    Demonstrates how adapters enable polymorphic use of different gateways.
    """
    
    @staticmethod
    def create_processor(config: dict) -> PaymentProcessor:
        """Create appropriate processor based on config.
        
        Args:
            config: Dictionary with 'type' and gateway-specific settings
            - type: 'modern' or 'legacy'
            - For modern: 'api_key'
            - For legacy: 'merchant_id', 'secret'
            
        Returns:
            Configured PaymentProcessor (via appropriate adapter)
        """
        raise NotImplementedError("Implement create_processor")
