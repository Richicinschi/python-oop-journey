"""Problem 06: Bank Branch

Topic: @classmethod and @staticmethod mix
Difficulty: Medium

Create a BankAccount class that uses both class methods and static methods.

Example:
    >>> # Set class-level interest rate
    >>> BankAccount.set_interest_rate(0.05)
    >>> BankAccount.get_interest_rate()
    0.05
    >>> 
    >>> acc = BankAccount("Alice", 1000)
    >>> acc.apply_interest()
    >>> acc.balance
    1050.0
    >>> 
    >>> # Validate account number format
    >>> BankAccount.is_valid_account_number("ACC-12345")
    True
    >>> BankAccount.is_valid_account_number("INVALID")
    False
    >>> 
    >>> # Calculate fee using static method
    >>> BankAccount.calculate_fee(500, 0.02)
    10.0

Requirements:
    - _interest_rate: class-level variable (default 0.0)
    - __init__(self, owner: str, balance: float)
    - set_interest_rate(cls, rate: float): classmethod to set interest rate
    - get_interest_rate(cls) -> float: classmethod to get interest rate
    - apply_interest(self): instance method to add interest to balance
    - is_valid_account_number(number: str) -> bool: static method
      Valid format: "ACC-" followed by 5 digits
    - calculate_fee(amount: float, rate: float) -> float: static method
"""

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
        raise NotImplementedError("Implement __init__")
    
    @classmethod
    def set_interest_rate(cls, rate: float) -> None:
        """Set the class-level interest rate.
        
        Args:
            rate: Interest rate as decimal (e.g., 0.05 for 5%)
        """
        raise NotImplementedError("Implement set_interest_rate")
    
    @classmethod
    def get_interest_rate(cls) -> float:
        """Get the current interest rate.
        
        Returns:
            Current interest rate
        """
        raise NotImplementedError("Implement get_interest_rate")
    
    def apply_interest(self) -> None:
        """Apply interest to the account balance."""
        raise NotImplementedError("Implement apply_interest")
    
    @staticmethod
    def is_valid_account_number(number: str) -> bool:
        """Check if account number is valid.
        
        Valid format: "ACC-" followed by exactly 5 digits
        
        Args:
            number: Account number to validate
            
        Returns:
            True if valid, False otherwise
        """
        raise NotImplementedError("Implement is_valid_account_number")
    
    @staticmethod
    def calculate_fee(amount: float, rate: float) -> float:
        """Calculate a fee based on amount and rate.
        
        Args:
            amount: Base amount
            rate: Fee rate as decimal
            
        Returns:
            Calculated fee
        """
        raise NotImplementedError("Implement calculate_fee")
