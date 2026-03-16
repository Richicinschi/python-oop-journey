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
    
    account_id: str
    category_id: str
    amount: float
    type: TransactionType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    date: date = field(default_factory=date.today)
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
    to_account_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate transaction after creation."""
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if not self.account_id:
            raise ValueError("Account ID is required")
        if not self.category_id:
            raise ValueError("Category ID is required")
    
    def is_income(self) -> bool:
        """Check if this is an income transaction."""
        return self.type == TransactionType.INCOME
    
    def is_expense(self) -> bool:
        """Check if this is an expense transaction."""
        return self.type == TransactionType.EXPENSE
    
    def is_transfer(self) -> bool:
        """Check if this is a transfer between accounts."""
        return self.type == TransactionType.TRANSFER
    
    def signed_amount(self) -> float:
        """Get the signed amount based on transaction type.
        
        Income: positive amount
        Expense: negative amount
        Transfer: negative (from source account perspective)
        
        Returns:
            Amount with appropriate sign
        """
        if self.type == TransactionType.INCOME:
            return self.amount
        else:
            return -self.amount
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for serialization."""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "category_id": self.category_id,
            "amount": self.amount,
            "type": self.type.name,
            "description": self.description,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "to_account_id": self.to_account_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Transaction:
        """Create transaction from dictionary."""
        return cls(
            id=data["id"],
            account_id=data["account_id"],
            category_id=data["category_id"],
            amount=data["amount"],
            type=TransactionType[data["type"]],
            description=data.get("description", ""),
            date=date.fromisoformat(data["date"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            tags=data.get("tags", []),
            to_account_id=data.get("to_account_id")
        )


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
    
    from_account_id: str
    to_account_id: str
    amount: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    date: date = field(default_factory=date.today)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validate transfer after creation."""
        if self.amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if not self.from_account_id or not self.to_account_id:
            raise ValueError("Both account IDs are required")
        if self.from_account_id == self.to_account_id:
            raise ValueError("Cannot transfer to the same account")
    
    def create_transactions(
        self,
        transfer_category_id: str
    ) -> tuple[Transaction, Transaction]:
        """Create the two transaction records for this transfer.
        
        Args:
            transfer_category_id: Category ID for transfer transactions
            
        Returns:
            Tuple of (outgoing_transaction, incoming_transaction)
        """
        outgoing = Transaction(
            account_id=self.from_account_id,
            category_id=transfer_category_id,
            amount=self.amount,
            type=TransactionType.TRANSFER,
            description=f"Transfer to {self.to_account_id}: {self.description}".strip(),
            date=self.date,
            to_account_id=self.to_account_id
        )
        
        incoming = Transaction(
            account_id=self.to_account_id,
            category_id=transfer_category_id,
            amount=self.amount,
            type=TransactionType.TRANSFER,
            description=f"Transfer from {self.from_account_id}: {self.description}".strip(),
            date=self.date,
            to_account_id=self.from_account_id
        )
        
        return outgoing, incoming


def create_transaction(
    account_id: str,
    category_id: str,
    amount: float,
    type: TransactionType,
    description: str = "",
    tx_date: Optional[date] = None,
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
        tx_date: Optional date (defaults to today)
        tags: Optional list of tags
        to_account_id: For transfers, destination account
        
    Returns:
        New Transaction instance
        
    Raises:
        ValueError: If amount is not positive
    """
    if amount <= 0:
        raise ValueError("Transaction amount must be positive")
    if not account_id:
        raise ValueError("Account ID is required")
    if not category_id:
        raise ValueError("Category ID is required")
    
    return Transaction(
        account_id=account_id,
        category_id=category_id,
        amount=amount,
        type=type,
        description=description,
        date=tx_date or date.today(),
        tags=tags or [],
        to_account_id=to_account_id
    )


def create_transfer(
    from_account_id: str,
    to_account_id: str,
    amount: float,
    description: str = "",
    tx_date: Optional[date] = None
) -> Transfer:
    """Factory function to create a new transfer.
    
    Args:
        from_account_id: Source account ID
        to_account_id: Destination account ID
        amount: Transfer amount (must be positive)
        description: Optional description
        tx_date: Optional date (defaults to today)
        
    Returns:
        New Transfer instance
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    if from_account_id == to_account_id:
        raise ValueError("Cannot transfer to the same account")
    
    return Transfer(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        amount=amount,
        description=description,
        date=tx_date or date.today()
    )
