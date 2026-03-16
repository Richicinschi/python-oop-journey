"""Solution for Problem 09: Transaction Guard."""

from __future__ import annotations

from typing import Any


class TransactionGuard:
    """A context manager that simulates database transactions.
    
    Usage:
        with TransactionGuard() as tx:
            tx.execute("operation")
            # If no exception: committed = True
            # If exception: rolled_back = True, exception propagates
    """

    def __init__(self) -> None:
        """Initialize the transaction guard."""
        self.operations: list[str] = []
        self.committed = False
        self.rolled_back = False

    def __enter__(self) -> "TransactionGuard":
        """Enter the transaction context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> bool:
        """Exit the transaction context.
        
        Returns:
            False to not suppress exceptions
        """
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True
        return False

    def execute(self, operation: str) -> None:
        """Record an operation in the transaction.
        
        Args:
            operation: The operation to record
        """
        self.operations.append(operation)
