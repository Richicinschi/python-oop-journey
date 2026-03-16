"""Problem 09: Transaction Guard

Topic: Context Managers
Difficulty: Medium

Implement a context manager for database-like transactions.

Examples:
    >>> tx = TransactionGuard()
    >>> with tx:
    ...     tx.execute("INSERT")
    ...     tx.execute("UPDATE")
    >>> tx.committed
    True
    >>> tx = TransactionGuard()
    >>> try:
    ...     with tx:
    ...         tx.execute("INSERT")
    ...         raise ValueError("Error!")
    ... except ValueError:
    ...     pass
    >>> tx.rolled_back
    True

Requirements:
    - Create TransactionGuard class as a context manager
    - Track executed operations in a list
    - Set committed=True if block completes without exception
    - Set rolled_back=True if exception occurs
    - Don't suppress exceptions (let them propagate)

Hints:
    * Hint 1: Context managers need __enter__ and __exit__ methods.
      __enter__ runs when entering the 'with' block and returns self.
      __exit__ runs when exiting, whether normally or via exception.
    
    * Hint 2: The __exit__ method receives exc_type, exc_val, exc_tb
      which are None if no exception occurred. Use these to decide:
      - If all None: transaction committed
      - If any not None: transaction rolled_back
      - Return False to NOT suppress the exception
    
    * Hint 3: Track state in __init__:
      - self.operations = [] (list to store executed operations)
      - self.committed = False
      - self.rolled_back = False
      execute() appends to operations list

Debugging Tips:
    - "Exception not propagating": __exit__ must return False/None
      to let exceptions propagate. Returning True suppresses them.
    - "committed always True": Check that you're checking exc_type
      in __exit__, not just setting committed unconditionally
    - "operations empty": Make sure execute() actually appends to
      the list and that you're calling tx.execute(), not just execute()
    - Context manager not working: Ensure __enter__ returns self
      so 'tx' in 'with tx:' is the actual instance
"""

from __future__ import annotations


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
        raise NotImplementedError("Implement __init__")

    def __enter__(self) -> "TransactionGuard":
        """Enter the transaction context."""
        raise NotImplementedError("Implement __enter__")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        """Exit the transaction context.
        
        Returns:
            False to not suppress exceptions
        """
        raise NotImplementedError("Implement __exit__")

    def execute(self, operation: str) -> None:
        """Record an operation in the transaction.
        
        Args:
            operation: The operation to record
        """
        raise NotImplementedError("Implement execute")
