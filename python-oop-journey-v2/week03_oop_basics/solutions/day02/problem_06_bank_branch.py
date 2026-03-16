"""Solution for Problem 06: Bank Branch."""

from __future__ import annotations
import re


class BankAccount:
    """Bank account with class-level interest rate and utility methods."""
    
    _interest_rate: float = 0.0
    
    def __init__(self, owner: str, balance: float) -> None:
        """Initialize a bank account.
        
        Args:
            owner: Account owner's name
            balance: Initial balance
        """
        self.owner = owner
        self.balance = balance
    
    @classmethod
    def set_interest_rate(cls, rate: float) -> None:
        """Set the class-level interest rate.
        
        Args:
            rate: Interest rate as decimal (e.g., 0.05 for 5%)
        """
        cls._interest_rate = rate
    
    @classmethod
    def get_interest_rate(cls) -> float:
        """Get the current interest rate.
        
        Returns:
            Current interest rate
        """
        return cls._interest_rate
    
    def apply_interest(self) -> None:
        """Apply interest to the account balance."""
        interest = self.balance * self._interest_rate
        self.balance += interest
    
    @staticmethod
    def is_valid_account_number(number: str) -> bool:
        """Check if account number is valid.
        
        Valid format: "ACC-" followed by exactly 5 digits
        
        Args:
            number: Account number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(number, str):
            return False
        pattern = r"^ACC-\d{5}$"
        return bool(re.match(pattern, number))
    
    @staticmethod
    def calculate_fee(amount: float, rate: float) -> float:
        """Calculate a fee based on amount and rate.
        
        Args:
            amount: Base amount
            rate: Fee rate as decimal
            
        Returns:
            Calculated fee
        """
        return amount * rate
