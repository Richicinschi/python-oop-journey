"""Transaction management module.

Domain model for financial transactions (income, expenses, transfers).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, auto
from typing import Optional
import uuid


class TransactionType(Enum):
    """Types of financial transactions."""
    INCOME = auto()
    EXPENSE = auto()
    TRANSFER = auto()


@dataclass
class Transaction:
    """Represents a financial transaction.
    
    A transaction records the movement of money between accounts or
    from/to external sources.
    
    Attributes:
        id: Unique transaction identifier
        account_id: ID of the primary account
        category_id: ID of the transaction category
        amount: Transaction amount (always positive)
        type: INCOME, EXPENSE, or TRANSFER
        description: Human-readable description
        date: Transaction date
        created_at: Timestamp when transaction was recorded
        tags: Optional list of tags for organization
        to_account_id: For transfers, the destination account ID
    """
    
    # TODO: Implement the Transaction dataclass
    # - Define all attributes with proper types
    # - Set appropriate default values
    # - Auto-generate id and timestamps
    
    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        raise NotImplementedError("Implement is_income method")
    
    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        raise NotImplementedError("Implement is_expense method")
    
    def is_transfer(self) -> bool:
        """Check if this is a transfer between accounts."""
        raise NotImplementedError("Implement is_transfer method")
    
    def signed_amount(self) -> float:
        """Get the signed amount based on transaction type.
        
        Income: positive amount
        Expense: negative amount
        Transfer: depends on perspective (this implementation returns negative)
        
        Returns:
            Amount with appropriate sign
        """
        raise NotImplementedError("Implement signed_amount method")
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for serialization."""
        raise NotImplementedError("Implement to_dict method")
    
    @classmethod
    def from_dict(cls, data: dict) -> Transaction:
        """Create transaction from dictionary."""
        raise NotImplementedError("Implement from_dict method")


@dataclass
class Transfer:
    """Represents a transfer between two accounts.
    
    A transfer creates two transaction records - one outgoing from
    the source account and one incoming to the destination account.
    
    Attributes:
        id: Unique transfer identifier
        from_account_id: Source account ID
        to_account_id: Destination account ID
        amount: Transfer amount
        description: Transfer description
        date: Transfer date
        created_at: Timestamp when transfer was created
    """
    
    # TODO: Implement the Transfer dataclass
    
    def create_transactions(self) -> tuple[Transaction, Transaction]:
        """Create the two transaction records for this transfer.
        
        Returns:
            Tuple of (outgoing_transaction, incoming_transaction)
        """
        raise NotImplementedError("Implement create_transactions method")


def create_transaction(
    account_id: str,
    category_id: str,
    amount: float,
    type: TransactionType,
    description: str = "",
    date: Optional[date] = None,
    tags: Optional[list[str]] = None,
    to_account_id: Optional[str] = None
) -> Transaction:
    """Factory function to create a new transaction.
    
    Args:
        account_id: Primary account ID
        category_id: Category ID
        amount: Transaction amount (must be positive)
        type: Transaction type
        description: Optional description
        date: Optional date (defaults to today)
        tags: Optional list of tags
        to_account_id: For transfers, destination account
        
    Returns:
        New Transaction instance
        
    Raises:
        ValueError: If amount is not positive
    """
    raise NotImplementedError("Implement create_transaction function")


def create_transfer(
    from_account_id: str,
    to_account_id: str,
    amount: float,
    description: str = "",
    date: Optional[date] = None
) -> Transfer:
    """Factory function to create a new transfer.
    
    Args:
        from_account_id: Source account ID
        to_account_id: Destination account ID
        amount: Transfer amount (must be positive)
        description: Optional description
        date: Optional date (defaults to today)
        
    Returns:
        New Transfer instance
    """
    raise NotImplementedError("Implement create_transfer function")
