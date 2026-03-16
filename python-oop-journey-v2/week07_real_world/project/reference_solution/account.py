"""Account management module.

Domain model for financial accounts (checking, savings, credit, investment).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional
import uuid


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
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    account_type: AccountType = AccountType.CHECKING
    balance: float = 0.0
    currency: str = "USD"
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __post_init__(self) -> None:
        """Validate account after creation."""
        if not self.name:
            raise ValueError("Account name cannot be empty")
        if self.balance < 0 and self.account_type != AccountType.CREDIT:
            raise ValueError(f"{self.account_type.name} account cannot have negative balance")
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Returns:
            True if deposit was successful, False otherwise
        """
        if amount <= 0:
            return False
        
        if self.account_type == AccountType.CREDIT:
            self.balance -= amount
        else:
            self.balance += amount
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account.
        
        For credit accounts, this increases the balance owed.
        For other accounts, this decreases the balance.
        
        Args:
            amount: Amount to withdraw (must be positive)
            
        Returns:
            True if withdrawal was successful, False if insufficient funds
        """
        if amount <= 0:
            return False
        
        if not self.can_withdraw(amount):
            return False
        
        if self.account_type == AccountType.CREDIT:
            self.balance += amount
        else:
            self.balance -= amount
        return True
    
    def can_withdraw(self, amount: float) -> bool:
        """Check if withdrawal is possible without executing it.
        
        Args:
            amount: Amount to check
            
        Returns:
            True if withdrawal would succeed
        """
        if amount <= 0:
            return False
        
        if self.account_type == AccountType.CREDIT:
            return True
        
        return self.balance >= amount
    
    def to_dict(self) -> dict:
        """Convert account to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "account_type": self.account_type.name,
            "balance": self.balance,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Account:
        """Create account from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            account_type=AccountType[data["account_type"]],
            balance=data["balance"],
            currency=data.get("currency", "USD"),
            created_at=datetime.fromisoformat(data["created_at"]),
            is_active=data.get("is_active", True)
        )


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
        ValueError: If initial_balance is negative (for non-credit accounts)
    """
    if not name:
        raise ValueError("Account name cannot be empty")
    
    return Account(
        name=name,
        account_type=account_type,
        balance=initial_balance,
        currency=currency
    )
