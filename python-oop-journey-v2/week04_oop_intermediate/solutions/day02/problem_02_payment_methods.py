"""Reference solution for Problem 02: Payment Methods."""

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
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not currency:
            raise ValueError("Currency cannot be empty")
        self.amount = amount
        self.currency = currency.upper()
        self.transaction_id = transaction_id

    def process(self) -> str:
        """Process the payment. Returns confirmation string."""
        return f"Processing {self.currency} {self.amount:.2f} [{self.transaction_id}]"

    def get_details(self) -> dict[str, object]:
        """Return payment details as dictionary."""
        return {
            "amount": self.amount,
            "currency": self.currency,
            "transaction_id": self.transaction_id,
        }


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
        super().__init__(amount, currency, transaction_id)
        if not card_last_four or len(card_last_four) != 4 or not card_last_four.isdigit():
            raise ValueError("Card last four must be exactly 4 digits")
        self.card_last_four = card_last_four
        self.expiry_date = expiry_date

    def process(self) -> str:
        """Process credit card payment."""
        base = super().process()
        return f"Credit Card ****{self.card_last_four} processing {base}"

    def get_details(self) -> dict[str, object]:
        """Return credit card payment details."""
        details = super().get_details()
        details.update({
            "card_last_four": self.card_last_four,
            "expiry_date": self.expiry_date,
            "method": "credit_card",
        })
        return details


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
        super().__init__(amount, currency, transaction_id)
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        self.email = email

    def process(self) -> str:
        """Process PayPal payment."""
        base = super().process()
        return f"PayPal ({self.email}) processing {base}"

    def get_details(self) -> dict[str, object]:
        """Return PayPal payment details."""
        details = super().get_details()
        details.update({
            "email": self.email,
            "method": "paypal",
        })
        return details


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
        super().__init__(amount, currency, transaction_id)
        crypto_upper = crypto_currency.upper()
        if crypto_upper not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported cryptocurrency: {crypto_currency}")
        self.wallet_address = wallet_address
        self.crypto_currency = crypto_upper

    def process(self) -> str:
        """Process crypto payment."""
        base = super().process()
        wallet_short = self.wallet_address
        if len(wallet_short) > 10:
            wallet_short = f"{wallet_short[:6]}...{wallet_short[-4:]}"
        return f"Crypto ({self.crypto_currency}) to {wallet_short} processing {base}"

    def get_details(self) -> dict[str, object]:
        """Return crypto payment details."""
        details = super().get_details()
        details.update({
            "wallet_address": self.wallet_address,
            "crypto_currency": self.crypto_currency,
            "method": "crypto",
        })
        return details
