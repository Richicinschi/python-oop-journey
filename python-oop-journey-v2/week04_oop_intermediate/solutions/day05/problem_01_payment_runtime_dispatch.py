"""Reference solution for Problem 01: Payment Runtime Dispatch."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import uuid


class PaymentMethod(ABC):
    """Abstract base class for payment methods."""

    def __init__(self, method_name: str) -> None:
        self.method_name = method_name

    @abstractmethod
    def validate(self) -> bool:
        """Validate payment method details."""
        pass

    @abstractmethod
    def process_payment(self, amount: float) -> dict[str, Any]:
        """Process a payment of the given amount."""
        pass


class CreditCardPayment(PaymentMethod):
    """Credit card payment implementation."""

    def __init__(self, card_number: str, expiry_date: str, cvv: str) -> None:
        super().__init__("Credit Card")
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv

    def validate(self) -> bool:
        """Validate credit card details."""
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            return False
        if len(self.expiry_date) != 5 or self.expiry_date[2] != "/":
            return False
        month, year = self.expiry_date[:2], self.expiry_date[3:]
        if not (month.isdigit() and year.isdigit()):
            return False
        if len(self.cvv) not in (3, 4) or not self.cvv.isdigit():
            return False
        return True

    def process_payment(self, amount: float) -> dict[str, Any]:
        """Process credit card payment."""
        if not self.validate():
            return {
                "success": False,
                "method": self.method_name,
                "amount": amount,
                "transaction_id": "",
                "message": "Invalid card details",
            }
        masked = "****" + self.card_number[-4:]
        return {
            "success": True,
            "method": self.method_name,
            "amount": amount,
            "transaction_id": str(uuid.uuid4())[:8],
            "message": f"Charged ${amount:.2f} to card {masked}",
        }


class PayPalPayment(PaymentMethod):
    """PayPal payment implementation."""

    def __init__(self, email: str, password_token: str) -> None:
        super().__init__("PayPal")
        self.email = email
        self.password_token = password_token

    def validate(self) -> bool:
        """Validate PayPal details."""
        if "@" not in self.email or "." not in self.email:
            return False
        if len(self.password_token) < 8:
            return False
        return True

    def process_payment(self, amount: float) -> dict[str, Any]:
        """Process PayPal payment."""
        if not self.validate():
            return {
                "success": False,
                "method": self.method_name,
                "amount": amount,
                "transaction_id": "",
                "message": "Invalid PayPal credentials",
            }
        return {
            "success": True,
            "method": self.method_name,
            "amount": amount,
            "transaction_id": str(uuid.uuid4())[:8],
            "message": f"PayPal payment of ${amount:.2f} from {self.email}",
        }


class CryptoPayment(PaymentMethod):
    """Cryptocurrency payment implementation."""

    SUPPORTED_CURRENCIES = {"BTC", "ETH", "LTC"}

    def __init__(self, wallet_address: str, currency_type: str) -> None:
        super().__init__("Cryptocurrency")
        self.wallet_address = wallet_address
        self.currency_type = currency_type.upper()

    def validate(self) -> bool:
        """Validate crypto details."""
        if len(self.wallet_address) < 26:
            return False
        if self.currency_type not in self.SUPPORTED_CURRENCIES:
            return False
        return True

    def process_payment(self, amount: float) -> dict[str, Any]:
        """Process crypto payment."""
        if not self.validate():
            return {
                "success": False,
                "method": self.method_name,
                "amount": amount,
                "transaction_id": "",
                "message": "Invalid crypto details",
            }
        return {
            "success": True,
            "method": self.method_name,
            "amount": amount,
            "transaction_id": str(uuid.uuid4())[:8],
            "message": f"{self.currency_type} payment of ${amount:.2f}",
        }


class PaymentProcessor:
    """Processor that handles any payment method polymorphically."""

    def __init__(self) -> None:
        self._transactions: list[dict[str, Any]] = []

    def process(self, payment_method: PaymentMethod, amount: float) -> dict[str, Any]:
        """Process payment using the given payment method."""
        if amount <= 0:
            result = {
                "success": False,
                "method": payment_method.method_name,
                "amount": amount,
                "transaction_id": "",
                "message": "Invalid amount",
            }
        else:
            result = payment_method.process_payment(amount)
        self._transactions.append(result)
        return result

    def get_transaction_history(self) -> list[dict[str, Any]]:
        """Return list of all processed transactions."""
        return self._transactions.copy()
