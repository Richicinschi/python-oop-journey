"""Problem 02: ATM Machine.

Topic: Class Design Principles
Difficulty: Medium

Design an ATM system with the following classes:
- Card: Represents ATM card with PIN and linked account
- Account: Bank account with balance and transaction history
- Transaction: Base class for different transaction types
- Deposit, Withdrawal: Transaction subclasses
- ATM: Manages card sessions and processes transactions

Requirements:
- Card authentication with PIN validation
- Account balance tracking and updates
- Transaction history recording
- Withdrawal limits and balance checks
- Deposit and withdrawal operations

Hints:
    - Hint 1: ATM tracks session state: _inserted_card, _authenticated (bool), _current_account
    - Hint 2: Transaction.process receives Account object and modifies its balance
    - Hint 3: ATM methods check session state first: if not self._authenticated: return None or False
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto


class TransactionType(Enum):
    """Types of transactions."""
    DEPOSIT = auto()
    WITHDRAWAL = auto()


class Transaction(ABC):
    """Base class for bank transactions.
    
    Attributes:
        transaction_id: Unique transaction identifier
        account_id: Account this transaction affects
        amount: Transaction amount
        timestamp: When transaction occurred
    """
    
    def __init__(self, transaction_id: str, account_id: str, amount: float) -> None:
        raise NotImplementedError("Implement Transaction.__init__")
    
    @abstractmethod
    def process(self, account: Account) -> bool:
        """Process the transaction on the given account.
        
        Args:
            account: Account to process transaction on
            
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement")
    
    @abstractmethod
    def get_transaction_type(self) -> TransactionType:
        """Return the type of transaction."""
        raise NotImplementedError("Subclasses must implement")


class Deposit(Transaction):
    """Deposit transaction."""
    
    def __init__(self, transaction_id: str, account_id: str, amount: float) -> None:
        raise NotImplementedError("Implement Deposit.__init__")
    
    def process(self, account: Account) -> bool:
        """Process deposit by adding to account balance."""
        raise NotImplementedError("Implement Deposit.process")
    
    def get_transaction_type(self) -> TransactionType:
        """Return transaction type."""
        raise NotImplementedError("Implement Deposit.get_transaction_type")


class Withdrawal(Transaction):
    """Withdrawal transaction."""
    
    def __init__(self, transaction_id: str, account_id: str, amount: float) -> None:
        raise NotImplementedError("Implement Withdrawal.__init__")
    
    def process(self, account: Account) -> bool:
        """Process withdrawal by subtracting from balance."""
        raise NotImplementedError("Implement Withdrawal.process")
    
    def get_transaction_type(self) -> TransactionType:
        """Return transaction type."""
        raise NotImplementedError("Implement Withdrawal.get_transaction_type")


class Account:
    """Bank account with balance and transaction history.
    
    Attributes:
        account_id: Unique account identifier
        owner_name: Name of account owner
        balance: Current account balance
    """
    
    def __init__(self, account_id: str, owner_name: str, initial_balance: float = 0.0) -> None:
        raise NotImplementedError("Implement Account.__init__")
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful, False if invalid amount
        """
        raise NotImplementedError("Implement Account.deposit")
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful, False if insufficient funds
        """
        raise NotImplementedError("Implement Account.withdraw")
    
    def get_transaction_history(self) -> list[Transaction]:
        """Get list of all transactions."""
        raise NotImplementedError("Implement Account.get_transaction_history")
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Record a transaction in history."""
        raise NotImplementedError("Implement Account.add_transaction")


class Card:
    """ATM card linked to an account.
    
    Attributes:
        card_number: Unique card identifier
        pin: Card PIN for authentication
        account_id: Linked account ID
        is_blocked: Whether card is blocked
    """
    
    def __init__(self, card_number: str, pin: str, account_id: str) -> None:
        raise NotImplementedError("Implement Card.__init__")
    
    def validate_pin(self, pin: str) -> bool:
        """Validate PIN.
        
        Args:
            pin: PIN to validate
            
        Returns:
            True if PIN matches and card not blocked
        """
        raise NotImplementedError("Implement Card.validate_pin")
    
    def block(self) -> None:
        """Block the card."""
        raise NotImplementedError("Implement Card.block")


class ATM:
    """ATM machine managing card sessions and transactions.
    
    Coordinates card authentication, account access, and transactions.
    Single Responsibility: ATM session and transaction management.
    
    Attributes:
        atm_id: Unique ATM identifier
        location: ATM location description
    """
    
    def __init__(self, atm_id: str, location: str) -> None:
        raise NotImplementedError("Implement ATM.__init__")
    
    def insert_card(self, card: Card) -> bool:
        """Insert card into ATM.
        
        Args:
            card: Card to insert
            
        Returns:
            True if card accepted
        """
        raise NotImplementedError("Implement ATM.insert_card")
    
    def enter_pin(self, pin: str) -> bool:
        """Enter PIN for authentication.
        
        Args:
            pin: PIN entered by user
            
        Returns:
            True if authenticated, False otherwise
        """
        raise NotImplementedError("Implement ATM.enter_pin")
    
    def check_balance(self) -> float | None:
        """Check balance of current session account.
        
        Returns:
            Balance if authenticated, None otherwise
        """
        raise NotImplementedError("Implement ATM.check_balance")
    
    def deposit_cash(self, amount: float) -> bool:
        """Deposit cash into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Implement ATM.deposit_cash")
    
    def withdraw_cash(self, amount: float) -> bool:
        """Withdraw cash from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Implement ATM.withdraw_cash")
    
    def eject_card(self) -> Card | None:
        """Eject card and end session.
        
        Returns:
            The ejected card, or None if no card inserted
        """
        raise NotImplementedError("Implement ATM.eject_card")


# Forward reference resolution
Account.__class_getitem__ = classmethod(lambda cls, item: item)  # type: ignore
