"""Reference solution for Problem 05: Transaction Context Manager."""

from __future__ import annotations

from copy import deepcopy
from types import TracebackType
from typing import Any, Protocol


class DatabaseInterface(Protocol):
    """Protocol for database-like objects that support transactions."""
    
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...


class SimpleDatabase:
    """A simple in-memory database for testing transactions."""
    
    def __init__(self) -> None:
        """Initialize an empty database."""
        self._data: dict[str, Any] = {}
    
    def get(self, key: str) -> Any:
        """Get a value by key.
        
        Args:
            key: The key to look up.
        
        Returns:
            The value associated with the key.
        
        Raises:
            KeyError: If the key doesn't exist.
        """
        return self._data[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set a value for a key.
        
        Args:
            key: The key to set.
            value: The value to store.
        """
        self._data[key] = value
    
    def delete(self, key: str) -> None:
        """Delete a key from the database.
        
        Args:
            key: The key to delete.
        
        Raises:
            KeyError: If the key doesn't exist.
        """
        del self._data[key]
    
    def keys(self) -> list[str]:
        """Get all keys in the database."""
        return list(self._data.keys())
    
    def snapshot(self) -> dict[str, Any]:
        """Get a copy of all data."""
        return deepcopy(self._data)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data


class Transaction:
    """A context manager that provides transaction semantics."""
    
    def __init__(self, database: DatabaseInterface) -> None:
        """Initialize the transaction.
        
        Args:
            database: The database to manage within the transaction.
        """
        self.database = database
        self.committed = False
        self._buffer: dict[str, Any] = {}  # Pending changes
        self._deletions: set[str] = set()  # Pending deletions
        self._snapshot: dict[str, Any] = {}
    
    def __enter__(self) -> Transaction:
        """Enter the transaction context."""
        # Capture initial state for rollback
        if hasattr(self.database, 'snapshot'):
            self._snapshot = self.database.snapshot()
        self.committed = False
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the transaction context."""
        if exc_type is None:
            # No exception - commit
            self.commit()
            return None
        else:
            # Exception occurred - rollback
            self.rollback()
            return None  # Don't suppress the exception
    
    def get(self, key: str) -> Any:
        """Get a value, considering pending transaction changes.
        
        Args:
            key: The key to look up.
        
        Returns:
            The value (from transaction buffer or database).
        
        Raises:
            KeyError: If key not found.
        """
        # Check if key is pending deletion
        if key in self._deletions:
            raise KeyError(key)
        
        # Check buffer first
        if key in self._buffer:
            return self._buffer[key]
        
        # Fall back to database
        return self.database.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value within the transaction.
        
        Args:
            key: The key to set.
            value: The value to store.
        """
        # Remove from deletions if it was pending deletion
        self._deletions.discard(key)
        # Buffer the change
        self._buffer[key] = value
    
    def delete(self, key: str) -> None:
        """Delete a key within the transaction.
        
        Args:
            key: The key to delete.
        """
        # Remove from buffer if it was pending addition/modification
        self._buffer.pop(key, None)
        # Mark for deletion
        self._deletions.add(key)
    
    def commit(self) -> None:
        """Commit all buffered changes to the database."""
        # Apply buffered changes
        for key, value in self._buffer.items():
            self.database.set(key, value)
        
        # Apply deletions
        for key in self._deletions:
            try:
                self.database.delete(key)
            except KeyError:
                pass  # Already doesn't exist
        
        # Clear buffer
        self._buffer.clear()
        self._deletions.clear()
        self.committed = True
    
    def rollback(self) -> None:
        """Rollback all buffered changes."""
        # Simply clear the buffers - no changes applied
        self._buffer.clear()
        self._deletions.clear()
        self.committed = False


class MultiResourceTransaction:
    """A transaction that spans multiple databases/resources."""
    
    def __init__(self, *databases: DatabaseInterface) -> None:
        """Initialize the multi-resource transaction.
        
        Args:
            databases: The databases/resources to include in the transaction.
        """
        self._databases = list(databases)
        self._transactions: dict[int, Transaction] = {}
        self._committed = False
    
    def __enter__(self) -> MultiResourceTransaction:
        """Enter the transaction context."""
        # Create sub-transactions for each database
        self._transactions = {
            id(db): Transaction(db) for db in self._databases
        }
        # Enter all sub-transactions
        for tx in self._transactions.values():
            tx.__enter__()
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the transaction context."""
        if exc_type is None:
            # No exception - commit all
            self._commit_all()
            return None
        else:
            # Exception - rollback all
            self._rollback_all()
            return None
    
    def _commit_all(self) -> None:
        """Commit all sub-transactions."""
        for tx in self._transactions.values():
            tx.commit()
        self._committed = True
    
    def _rollback_all(self) -> None:
        """Rollback all sub-transactions."""
        for tx in self._transactions.values():
            tx.rollback()
        self._committed = False
    
    def on(self, database: DatabaseInterface) -> Transaction:
        """Get a transaction interface for a specific database.
        
        Args:
            database: One of the databases passed to __init__.
        
        Returns:
            Transaction interface for that database.
        
        Raises:
            ValueError: If database not part of this transaction.
        """
        db_id = id(database)
        if db_id not in self._transactions:
            raise ValueError("Database not part of this transaction")
        return self._transactions[db_id]
    
    @property
    def committed(self) -> bool:
        """Check if transaction was committed."""
        return self._committed
