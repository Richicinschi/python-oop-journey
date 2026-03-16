"""Problem 02: Payment Methods

Topic: super().__init__() for shared attribute initialization
Difficulty: Easy

Create a payment method hierarchy where child classes use super().__init__()
to share common payment attributes while adding payment-specific details.

Classes to implement:
- PaymentMethod: Base class with amount, currency, and transaction_id
- CreditCard: Adds card_number (last 4 digits), expiry_date
- PayPal: Adds email, paypal_transaction_id
- Crypto: Adds wallet_address, crypto_currency

Example:
    >>> payment = PaymentMethod(100.0, "USD", "TXN12345")
    >>> payment.process()
    'Processing USD 100.00 [TXN12345]'
    
    >>> cc = CreditCard(50.0, "EUR", "TXN67890", "1234", "12/25")
    >>> cc.process()
    'Credit Card ****1234 processing EUR 50.00 [TXN67890]'
    
    >>> paypal = PayPal(75.0, "USD", "TXN11111", "user@example.com")
    >>> paypal.get_details()
    {'amount': 75.0, 'currency': 'USD', 'email': 'user@example.com'}

Requirements:
    - PaymentMethod: amount, currency, transaction_id, process(), get_details()
    - CreditCard: card_last_four, expiry_date, masked card display
    - PayPal: email, paypal-specific transaction tracking
    - Crypto: wallet_address, crypto_currency (BTC, ETH, etc.)
    - Use super().__init__() in all child classes
    - Override process() in each child with super().process() call
    - get_details() should extend parent's dict in children
"""

from __future__ import annotations


class PaymentMethod:
    """Base payment method class."""

    def __init__(self, amount: float, currency: str, transaction_id: str) -> None:
        """Initialize payment with common attributes.
        
        Args:
            amount: Payment amount (must be positive)
            currency: Currency code (e.g., "USD", "EUR")
            transaction_id: Unique transaction identifier
            
        Raises:
            ValueError: If amount <= 0 or currency is empty
        """
        raise NotImplementedError("Initialize all attributes with validation")

    def process(self) -> str:
        """Process the payment. Returns confirmation string.
        
        Format: 'Processing {currency} {amount:.2f} [{transaction_id}]'
        """
        raise NotImplementedError("Implement base process()")

    def get_details(self) -> dict[str, object]:
        """Return payment details as dictionary.
        
        Returns dict with: amount, currency, transaction_id
        """
        raise NotImplementedError("Return base payment details")


class CreditCard(PaymentMethod):
    """Credit card payment method."""

    def __init__(
        self,
        amount: float,
        currency: str,
        transaction_id: str,
        card_last_four: str,
        expiry_date: str
    ) -> None:
        """Initialize credit card payment.
        
        Args:
            amount: Payment amount
            currency: Currency code
            transaction_id: Transaction identifier
            card_last_four: Last 4 digits of card
            expiry_date: Card expiry in MM/YY format
            
        Raises:
            ValueError: If card_last_four is not exactly 4 digits
        """
        raise NotImplementedError("Use super().__init__() and add card attributes")

    def process(self) -> str:
        """Process credit card payment.
        
        Format: 'Credit Card ****{last4} processing {parent_process_result}'
        """
        raise NotImplementedError("Override with super().process()")

    def get_details(self) -> dict[str, object]:
        """Return credit card payment details.
        
        Extends parent dict with: card_last_four, expiry_date, method='credit_card'
        """
        raise NotImplementedError("Extend parent's get_details() with super()")


class PayPal(PaymentMethod):
    """PayPal payment method."""

    def __init__(
        self,
        amount: float,
        currency: str,
        transaction_id: str,
        email: str
    ) -> None:
        """Initialize PayPal payment.
        
        Args:
            amount: Payment amount
            currency: Currency code
            transaction_id: Transaction identifier
            email: PayPal account email
            
        Raises:
            ValueError: If email is empty or doesn't contain '@'
        """
        raise NotImplementedError("Use super().__init__() and add email")

    def process(self) -> str:
        """Process PayPal payment.
        
        Format: 'PayPal ({email}) processing {parent_process_result}'
        """
        raise NotImplementedError("Override with super().process()")

    def get_details(self) -> dict[str, object]:
        """Return PayPal payment details.
        
        Extends parent dict with: email, method='paypal'
        """
        raise NotImplementedError("Extend parent's get_details() with super()")


class Crypto(PaymentMethod):
    """Cryptocurrency payment method."""

    SUPPORTED_CURRENCIES = ("BTC", "ETH", "LTC", "USDC", "USDT")

    def __init__(
        self,
        amount: float,
        currency: str,
        transaction_id: str,
        wallet_address: str,
        crypto_currency: str
    ) -> None:
        """Initialize crypto payment.
        
        Args:
            amount: Payment amount
            currency: Fiat currency code
            transaction_id: Transaction identifier
            wallet_address: Crypto wallet address
            crypto_currency: Cryptocurrency type (BTC, ETH, etc.)
            
        Raises:
            ValueError: If crypto_currency not in SUPPORTED_CURRENCIES
        """
        raise NotImplementedError("Use super().__init__() and add crypto attributes")

    def process(self) -> str:
        """Process crypto payment.
        
        Format: 'Crypto ({crypto_currency}) to {wallet_short} processing {parent}'
        wallet_short: first 6 chars + '...' + last 4 chars
        """
        raise NotImplementedError("Override with super().process()")

    def get_details(self) -> dict[str, object]:
        """Return crypto payment details.
        
        Extends parent dict with: wallet_address, crypto_currency, method='crypto'
        """
        raise NotImplementedError("Extend parent's get_details() with super()")
