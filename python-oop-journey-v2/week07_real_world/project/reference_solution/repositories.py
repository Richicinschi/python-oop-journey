"""Repository layer for data persistence.

Implements the Repository pattern to abstract data storage operations.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import Any, Generic, TypeVar

from week07_real_world.project.reference_solution.account import Account, AccountType
from week07_real_world.project.reference_solution.category import Category, CategoryType
from week07_real_world.project.reference_solution.transaction import Transaction, TransactionType
from week07_real_world.project.reference_solution.budget import Budget, BudgetPeriod


T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract base class for repositories.
    
    The Repository pattern abstracts the data layer, providing a
    collection-like interface for accessing domain objects.
    """
    
    @abstractmethod
    def add(self, item: T) -> T:
        """Add an item to the repository.
        
        Args:
            item: Item to add
            
        Returns:
            The added item (possibly with generated ID)
        """
        pass
    
    @abstractmethod
    def get(self, id: str) -> T | None:
        """Get an item by ID.
        
        Args:
            id: Item identifier
            
        Returns:
            The item if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all items in the repository.
        
        Returns:
            List of all items
        """
        pass
    
    @abstractmethod
    def update(self, item: T) -> T:
        """Update an existing item.
        
        Args:
            item: Item to update
            
        Returns:
            The updated item
        """
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete an item by ID.
        
        Args:
            id: Item identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass


class InMemoryRepository(Repository[T], Generic[T]):
    """In-memory repository implementation.
    
    Stores items in memory. Data is lost when the process exits.
    Good for testing and prototyping.
    """
    
    def __init__(self) -> None:
        """Initialize the repository."""
        self._items: dict[str, T] = {}
    
    def add(self, item: Any) -> Any:
        """Add an item to the repository."""
        if hasattr(item, 'id'):
            self._items[item.id] = item
        return item
    
    def get(self, id: str) -> Any | None:
        """Get an item by ID."""
        return self._items.get(id)
    
    def get_all(self) -> list[Any]:
        """Get all items."""
        return list(self._items.values())
    
    def update(self, item: Any) -> Any:
        """Update an existing item."""
        if hasattr(item, 'id') and item.id in self._items:
            self._items[item.id] = item
            return item
        raise KeyError(f"Item with id {getattr(item, 'id', 'unknown')} not found")
    
    def delete(self, id: str) -> bool:
        """Delete an item by ID."""
        if id in self._items:
            del self._items[id]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()
    
    def count(self) -> int:
        """Get the number of items in the repository."""
        return len(self._items)


class AccountRepository(InMemoryRepository[Account]):
    """Repository for Account entities."""
    
    def get_by_type(self, account_type: AccountType) -> list[Account]:
        """Get all accounts of a specific type.
        
        Args:
            account_type: Type of accounts to retrieve
            
        Returns:
            List of matching accounts
        """
        return [
            account for account in self._items.values()
            if account.account_type == account_type
        ]
    
    def get_active(self) -> list[Account]:
        """Get all active accounts.
        
        Returns:
            List of active accounts
        """
        return [
            account for account in self._items.values()
            if account.is_active
        ]
    
    def get_total_balance(self) -> float:
        """Get total balance across all accounts.
        
        Note: Credit account balances are treated as negative.
        
        Returns:
            Total balance sum
        """
        total = 0.0
        for account in self._items.values():
            if account.account_type == AccountType.CREDIT:
                total -= account.balance
            else:
                total += account.balance
        return total
    
    def save_to_file(self, filepath: str | Path) -> None:
        """Save all accounts to a JSON file.
        
        Args:
            filepath: Path to the output file
        """
        data = [account.to_dict() for account in self._items.values()]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str | Path) -> None:
        """Load accounts from a JSON file.
        
        Args:
            filepath: Path to the input file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        self._items.clear()
        for item_data in data:
            account = Account.from_dict(item_data)
            self._items[account.id] = account


class TransactionRepository(InMemoryRepository[Transaction]):
    """Repository for Transaction entities."""
    
    def get_by_account(self, account_id: str) -> list[Transaction]:
        """Get all transactions for a specific account.
        
        Args:
            account_id: Account ID to filter by
            
        Returns:
            List of matching transactions
        """
        return [
            tx for tx in self._items.values()
            if tx.account_id == account_id or tx.to_account_id == account_id
        ]
    
    def get_by_category(self, category_id: str) -> list[Transaction]:
        """Get all transactions for a specific category.
        
        Args:
            category_id: Category ID to filter by
            
        Returns:
            List of matching transactions
        """
        return [
            tx for tx in self._items.values()
            if tx.category_id == category_id
        ]
    
    def get_by_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> list[Transaction]:
        """Get all transactions within a date range.
        
        Args:
            start_date: Start of date range (inclusive)
            end_date: End of date range (inclusive)
            
        Returns:
            List of transactions in the date range
        """
        return [
            tx for tx in self._items.values()
            if start_date <= tx.date <= end_date
        ]
    
    def get_by_type(self, tx_type: TransactionType) -> list[Transaction]:
        """Get all transactions of a specific type.
        
        Args:
            tx_type: Transaction type to filter by
            
        Returns:
            List of matching transactions
        """
        return [
            tx for tx in self._items.values()
            if tx.type == tx_type
        ]
    
    def get_total_by_category(self, category_id: str) -> float:
        """Get total amount for a category.
        
        Args:
            category_id: Category ID to sum
            
        Returns:
            Total transaction amount
        """
        return sum(
            tx.amount for tx in self._items.values()
            if tx.category_id == category_id
        )
    
    def save_to_file(self, filepath: str | Path) -> None:
        """Save all transactions to a JSON file.
        
        Args:
            filepath: Path to the output file
        """
        data = [tx.to_dict() for tx in self._items.values()]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filepath: str | Path) -> None:
        """Load transactions from a JSON file.
        
        Args:
            filepath: Path to the input file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        self._items.clear()
        for item_data in data:
            transaction = Transaction.from_dict(item_data)
            self._items[transaction.id] = transaction


class CategoryRepository(InMemoryRepository[Category]):
    """Repository for Category entities."""
    
    def get_by_type(self, category_type: CategoryType) -> list[Category]:
        """Get all categories of a specific type.
        
        Args:
            category_type: Type of categories to retrieve
            
        Returns:
            List of matching categories
        """
        return [
            cat for cat in self._items.values()
            if cat.type == category_type
        ]
    
    def get_income_categories(self) -> list[Category]:
        """Get all income categories.
        
        Returns:
            List of income categories
        """
        return self.get_by_type(CategoryType.INCOME)
    
    def get_expense_categories(self) -> list[Category]:
        """Get all expense categories.
        
        Returns:
            List of expense categories
        """
        return self.get_by_type(CategoryType.EXPENSE)
    
    def find_by_name(self, name: str) -> Category | None:
        """Find a category by name (case-insensitive).
        
        Args:
            name: Category name to search for
            
        Returns:
            Category if found, None otherwise
        """
        name_lower = name.lower()
        for cat in self._items.values():
            if cat.name.lower() == name_lower:
                return cat
        return None
    
    def save_to_file(self, filepath: str | Path) -> None:
        """Save all categories to a JSON file.
        
        Args:
            filepath: Path to the output file
        """
        data = [cat.to_dict() for cat in self._items.values()]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str | Path) -> None:
        """Load categories from a JSON file.
        
        Args:
            filepath: Path to the input file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        self._items.clear()
        for item_data in data:
            category = Category.from_dict(item_data)
            self._items[category.id] = category


class BudgetRepository(InMemoryRepository[Budget]):
    """Repository for Budget entities."""
    
    def get_by_category(self, category_id: str) -> Budget | None:
        """Get the budget for a specific category.
        
        Args:
            category_id: Category ID to look up
            
        Returns:
            Budget if found, None otherwise
        """
        for budget in self._items.values():
            if budget.category_id == category_id and budget.is_active:
                return budget
        return None
    
    def get_active_budgets(self) -> list[Budget]:
        """Get all active budgets.
        
        Returns:
            List of active budgets
        """
        return [
            budget for budget in self._items.values()
            if budget.is_active
        ]
    
    def get_by_period(self, period: BudgetPeriod) -> list[Budget]:
        """Get all budgets with a specific period.
        
        Args:
            period: Budget period to filter by
            
        Returns:
            List of matching budgets
        """
        return [
            budget for budget in self._items.values()
            if budget.period == period
        ]
    
    def save_to_file(self, filepath: str | Path) -> None:
        """Save all budgets to a JSON file.
        
        Args:
            filepath: Path to the output file
        """
        data = [budget.to_dict() for budget in self._items.values()]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str | Path) -> None:
        """Load budgets from a JSON file.
        
        Args:
            filepath: Path to the input file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        self._items.clear()
        for item_data in data:
            budget = Budget.from_dict(item_data)
            self._items[budget.id] = budget
