"""Account management module.

Domain model for financial accounts (checking, savings, credit, investment).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class AccountType(Enum):
    """Types of financial accounts."""
    CHECKING = auto()
    SAVINGS = auto()
    CREDIT = auto()
    INVESTMENT = auto()


@dataclass
class Account:
    """Represents a financial account.
    
    Attributes:
        id: Unique identifier for the account
        name: Human-readable account name
        account_type: Type of account (checking, savings, etc.)
        balance: Current account balance
        currency: ISO currency code (default: USD)
        created_at: Timestamp when account was created
        is_active: Whether the account is active
    """
    
    # TODO: Implement the Account dataclass
    # - Define all attributes with proper types
    # - Set appropriate default values
    # - Consider which fields should be frozen vs mutable
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Returns:
            True if deposit was successful, False otherwise
        """
        raise NotImplementedError("Implement deposit method")
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account.
        
        For credit accounts, this increases the balance owed.
        For other accounts, this decreases the balance.
        
        Args:
            amount: Amount to withdraw (must be positive)
            
        Returns:
            True if withdrawal was successful, False if insufficient funds
        """
        raise NotImplementedError("Implement withdraw method")
    
    def can_withdraw(self, amount: float) -> bool:
        """Check if withdrawal is possible without executing it.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if withdrawal would succeed
        """
        raise NotImplementedError("Implement can_withdraw method")
    
    def to_dict(self) -> dict:
        """Convert account to dictionary for serialization."""
        raise NotImplementedError("Implement to_dict method")
    
    @classmethod
    def from_dict(cls, data: dict) -> Account:
        """Create account from dictionary."""
        raise NotImplementedError("Implement from_dict method")


def create_account(
    name: str,
    account_type: AccountType,
    initial_balance: float = 0.0,
    currency: str = "USD"
) -> Account:
    """Factory function to create a new account.
    
    Args:
        name: Account name
        account_type: Type of account
        initial_balance: Starting balance (default: 0.0)
        currency: Currency code (default: USD)
        
    Returns:
        New Account instance
        
    Raises:
        ValueError: If initial_balance is negative
    """
    raise NotImplementedError("Implement create_account function")
