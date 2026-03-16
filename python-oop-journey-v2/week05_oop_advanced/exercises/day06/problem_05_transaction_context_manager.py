"""Problem 05: Transaction Context Manager.

Topic: Context Managers, Rollback, Error Handling
Difficulty: Medium

Implement a transaction manager that supports rollback on failure.

This pattern is essential for:
- Database transactions
- File operations that must be atomic
- Multi-step operations that must succeed or fail together
- State changes that need undo capability

Example:
    >>> db = SimpleDatabase()
    >>> db.set("a", 1)
    >>> db.set("b", 2)
    
    >>> try:
    ...     with Transaction(db) as tx:
    ...         tx.set("a", 100)
    ...         tx.set("b", 200)
    ...         raise ValueError("Simulated error")
    ... except ValueError:
    ...     pass
    
    >>> db.get("a")  # Rolled back
    1
    >>> db.get("b")  # Rolled back
    2
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Protocol


class DatabaseInterface(Protocol):
    """Protocol for database-like objects that support transactions."""
    
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...


class SimpleDatabase:
    """A simple in-memory database for testing transactions.
    
    Attributes:
        _data: Internal dictionary storing key-value pairs.
    """
    
    def __init__(self) -> None:
        """Initialize an empty database."""
        raise NotImplementedError("Implement __init__")
    
    def get(self, key: str) -> Any:
        """Get a value by key.
        
        Args:
            key: The key to look up.
        
        Returns:
            The value associated with the key.
        
        Raises:
            KeyError: If the key doesn't exist.
        """
        raise NotImplementedError("Implement get")
    
    def set(self, key: str, value: Any) -> None:
        """Set a value for a key.
        
        Args:
            key: The key to set.
            value: The value to store.
        """
        raise NotImplementedError("Implement set")
    
    def delete(self, key: str) -> None:
        """Delete a key from the database.
        
        Args:
            key: The key to delete.
        
        Raises:
            KeyError: If the key doesn't exist.
        """
        raise NotImplementedError("Implement delete")
    
    def keys(self) -> list[str]:
        """Get all keys in the database.
        
        Returns:
            List of all keys.
        """
        raise NotImplementedError("Implement keys")
    
    def snapshot(self) -> dict[str, Any]:
        """Get a copy of all data.
        
        Returns:
            Dictionary copy of the database.
        """
        raise NotImplementedError("Implement snapshot")


class Transaction:
    """A context manager that provides transaction semantics.
    
    Changes made within the transaction are buffered until commit.
    If an exception occurs, all changes are rolled back automatically.
    
    Attributes:
        database: The database being modified.
        committed: True if the transaction was committed successfully.
    
    Example:
        >>> db = SimpleDatabase()
        >>> with Transaction(db) as tx:
        ...     tx.set("key", "value")
        ...     # Changes applied when block exits successfully
        
        >>> with Transaction(db) as tx:
        ...     tx.set("key", "new_value")
        ...     raise ValueError()  # Changes rolled back
    """
    
    def __init__(self, database: DatabaseInterface) -> None:
        """Initialize the transaction.
        
        Args:
            database: The database to manage within the transaction.
        """
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> Transaction:
        """Enter the transaction context.
        
        Returns:
            The Transaction instance for use in the with block.
        """
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the transaction context.
        
        If no exception occurred, commits the transaction.
        If an exception occurred, rolls back all changes.
        
        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.
        
        Returns:
            None to propagate exceptions, or True to suppress.
        """
        raise NotImplementedError("Implement __exit__")
    
    def get(self, key: str) -> Any:
        """Get a value, considering pending transaction changes.
        
        Args:
            key: The key to look up.
        
        Returns:
            The value (from transaction buffer or database).
        """
        raise NotImplementedError("Implement get")
    
    def set(self, key: str, value: Any) -> None:
        """Set a value within the transaction.
        
        The change is not applied to the database until commit.
        
        Args:
            key: The key to set.
            value: The value to store.
        """
        raise NotImplementedError("Implement set")
    
    def delete(self, key: str) -> None:
        """Delete a key within the transaction.
        
        Args:
            key: The key to delete.
        """
        raise NotImplementedError("Implement delete")
    
    def commit(self) -> None:
        """Commit all buffered changes to the database.
        
        This is called automatically on successful exit from the context.
        """
        raise NotImplementedError("Implement commit")
    
    def rollback(self) -> None:
        """Rollback all buffered changes.
        
        This is called automatically when an exception occurs.
        """
        raise NotImplementedError("Implement rollback")


class MultiResourceTransaction:
    """A transaction that spans multiple databases/resources.
    
    All resources are committed together, or all are rolled back if any fails.
    
    Example:
        >>> db1 = SimpleDatabase()
        >>> db2 = SimpleDatabase()
        >>> with MultiResourceTransaction(db1, db2) as tx:
        ...     tx.on(db1).set("key1", "value1")
        ...     tx.on(db2).set("key2", "value2")
    """
    
    def __init__(self, *databases: DatabaseInterface) -> None:
        """Initialize the multi-resource transaction.
        
        Args:
            databases: The databases/resources to include in the transaction.
        """
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> MultiResourceTransaction:
        """Enter the transaction context."""
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Exit the transaction context."""
        raise NotImplementedError("Implement __exit__")
    
    def on(self, database: DatabaseInterface) -> Transaction:
        """Get a transaction interface for a specific database.
        
        Args:
            database: One of the databases passed to __init__.
        
        Returns:
            Transaction interface for that database.
        """
        raise NotImplementedError("Implement on")


# Hints for Transaction Context Manager (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to buffer changes and only apply them on successful exit. If an
# exception occurs, discard the buffer.
#
# Hint 2 - Structural plan:
# - __init__ stores the database reference
# - __enter__ returns self
# - set/delete buffer changes in a local dict, not the database
# - __exit__ commits if no exception, rolls back if exception
# - get checks buffer first, then database
#
# Hint 3 - Edge-case warning:
# What happens if someone deletes a key that exists in the database, then tries
# to get it? You need a way to mark "deleted in transaction" vs "not touched".
# Consider using a sentinel value or separate tracking set.
