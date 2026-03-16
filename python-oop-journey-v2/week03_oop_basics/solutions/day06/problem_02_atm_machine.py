"""Solution for Problem 02: ATM Machine.

Demonstrates class design principles:
- Encapsulation: Account protects balance, Card protects PIN
- Cohesion: Each class has focused responsibilities
- Abstraction: Transaction base class defines interface
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
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.timestamp = datetime.now()
    
    @abstractmethod
    def process(self, account: Account) -> bool:
        """Process the transaction on the given account.
        
        Args:
            account: Account to process transaction on
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_transaction_type(self) -> TransactionType:
        """Return the type of transaction."""
        pass


class Deposit(Transaction):
    """Deposit transaction."""
    
    def __init__(self, transaction_id: str, account_id: str, amount: float) -> None:
        super().__init__(transaction_id, account_id, amount)
    
    def process(self, account: Account) -> bool:
        """Process deposit by adding to account balance."""
        return account.deposit(self.amount)
    
    def get_transaction_type(self) -> TransactionType:
        """Return transaction type."""
        return TransactionType.DEPOSIT


class Withdrawal(Transaction):
    """Withdrawal transaction."""
    
    def __init__(self, transaction_id: str, account_id: str, amount: float) -> None:
        super().__init__(transaction_id, account_id, amount)
    
    def process(self, account: Account) -> bool:
        """Process withdrawal by subtracting from balance."""
        return account.withdraw(self.amount)
    
    def get_transaction_type(self) -> TransactionType:
        """Return transaction type."""
        return TransactionType.WITHDRAWAL


class Account:
    """Bank account with balance and transaction history.
    
    Attributes:
        account_id: Unique account identifier
        owner_name: Name of account owner
        balance: Current account balance
    """
    
    def __init__(self, account_id: str, owner_name: str, initial_balance: float = 0.0) -> None:
        self._account_id = account_id
        self._owner_name = owner_name
        self._balance = initial_balance
        self._transactions: list[Transaction] = []
    
    @property
    def account_id(self) -> str:
        return self._account_id
    
    @property
    def owner_name(self) -> str:
        return self._owner_name
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful, False if invalid amount
        """
        if amount <= 0:
            return False
        self._balance += amount
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful, False if insufficient funds
        """
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        return True
    
    def get_transaction_history(self) -> list[Transaction]:
        """Get list of all transactions."""
        return self._transactions.copy()
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Record a transaction in history."""
        self._transactions.append(transaction)


class Card:
    """ATM card linked to an account.
    
    Attributes:
        card_number: Unique card identifier
        pin: Card PIN for authentication
        account_id: Linked account ID
        is_blocked: Whether card is blocked
    """
    
    def __init__(self, card_number: str, pin: str, account_id: str) -> None:
        self._card_number = card_number
        self._pin = pin
        self._account_id = account_id
        self._is_blocked = False
    
    @property
    def card_number(self) -> str:
        return self._card_number
    
    @property
    def account_id(self) -> str:
        return self._account_id
    
    @property
    def is_blocked(self) -> bool:
        return self._is_blocked
    
    def validate_pin(self, pin: str) -> bool:
        """Validate PIN.
        
        Args:
            pin: PIN to validate
            
        Returns:
            True if PIN matches and card not blocked
        """
        if self._is_blocked:
            return False
        return self._pin == pin
    
    def block(self) -> None:
        """Block the card."""
        self._is_blocked = True


class ATM:
    """ATM machine managing card sessions and transactions.
    
    Coordinates card authentication, account access, and transactions.
    Single Responsibility: ATM session and transaction management.
    
    Attributes:
        atm_id: Unique ATM identifier
        location: ATM location description
    """
    
    def __init__(self, atm_id: str, location: str) -> None:
        self._atm_id = atm_id
        self._location = location
        self._current_card: Card | None = None
        self._is_authenticated = False
        self._accounts: dict[str, Account] = {}
        self._transaction_counter = 0
    
    def add_account(self, account: Account) -> None:
        """Add an account to this ATM's network (for demo purposes)."""
        self._accounts[account.account_id] = account
    
    def insert_card(self, card: Card) -> bool:
        """Insert card into ATM.
        
        Args:
            card: Card to insert
            
        Returns:
            True if card accepted
        """
        if self._current_card is not None:
            return False
        if card.is_blocked:
            return False
        self._current_card = card
        self._is_authenticated = False
        return True
    
    def enter_pin(self, pin: str) -> bool:
        """Enter PIN for authentication.
        
        Args:
            pin: PIN entered by user
            
        Returns:
            True if authenticated, False otherwise
        """
        if self._current_card is None:
            return False
        self._is_authenticated = self._current_card.validate_pin(pin)
        return self._is_authenticated
    
    def check_balance(self) -> float | None:
        """Check balance of current session account.
        
        Returns:
            Balance if authenticated, None otherwise
        """
        if not self._is_authenticated or self._current_card is None:
            return None
        account = self._accounts.get(self._current_card.account_id)
        if account is None:
            return None
        return account.balance
    
    def deposit_cash(self, amount: float) -> bool:
        """Deposit cash into account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            True if successful
        """
        if not self._is_authenticated or self._current_card is None:
            return False
        account = self._accounts.get(self._current_card.account_id)
        if account is None:
            return False
        
        self._transaction_counter += 1
        transaction = Deposit(
            f"TXN{self._transaction_counter:06d}",
            account.account_id,
            amount
        )
        
        if transaction.process(account):
            account.add_transaction(transaction)
            return True
        return False
    
    def withdraw_cash(self, amount: float) -> bool:
        """Withdraw cash from account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            True if successful
        """
        if not self._is_authenticated or self._current_card is None:
            return False
        account = self._accounts.get(self._current_card.account_id)
        if account is None:
            return False
        
        self._transaction_counter += 1
        transaction = Withdrawal(
            f"TXN{self._transaction_counter:06d}",
            account.account_id,
            amount
        )
        
        if transaction.process(account):
            account.add_transaction(transaction)
            return True
        return False
    
    def eject_card(self) -> Card | None:
        """Eject card and end session.
        
        Returns:
            The ejected card, or None if no card inserted
        """
        card = self._current_card
        self._current_card = None
        self._is_authenticated = False
        return card
