"""Problem 07: Logged Attribute

Topic: Logs all get/set operations
Difficulty: Medium

Create a descriptor that logs all access and modification operations.
"""

from __future__ import annotations

from typing import Any, Callable
from dataclasses import dataclass
from enum import Enum, auto


class Operation(Enum):
    """Types of attribute operations."""
    GET = auto()
    SET = auto()
    DELETE = auto()


@dataclass
class LogEntry:
    """A log entry for an attribute operation.
    
    Attributes:
        operation: The type of operation (GET, SET, DELETE)
        instance_id: ID of the instance
        attribute_name: Name of the attribute
        old_value: Previous value (for SET/DELETE)
        new_value: New value (for SET)
    """
    operation: Operation
    instance_id: int
    attribute_name: str
    old_value: Any = None
    new_value: Any = None


class LoggedAttribute:
    """A descriptor that logs all access operations.
    
    The descriptor should:
    - Log all GET, SET, and DELETE operations
    - Store logs in a shared class-level list
    - Include operation type, instance id, and values
    - Support custom log callbacks
    
    Attributes:
        logs: Class-level list of LogEntry objects
        log_callback: Optional callback for real-time logging
    """
    
    # Class-level storage for all logs
    logs: list[LogEntry] = []
    
    def __init__(
        self, 
        default: Any = None,
        log_callback: Callable[[LogEntry], None] | None = None
    ) -> None:
        """Initialize with optional default and callback.
        
        Args:
            default: Default value for new instances
            log_callback: Optional function to call on each log entry
        """
        raise NotImplementedError("Implement LoggedAttribute.__init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Called when descriptor is assigned to class.
        
        Args:
            owner: The class
            name: The attribute name
        """
        raise NotImplementedError("Implement LoggedAttribute.__set_name__")
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        """Get value and log the operation.
        
        Args:
            instance: The instance, or None for class access
            owner: The owner class
            
        Returns:
            The stored value, or self if class access
        """
        raise NotImplementedError("Implement LoggedAttribute.__get__")
    
    def __set__(self, instance: object, value: Any) -> None:
        """Set value and log the operation.
        
        Args:
            instance: The instance
            value: The new value
        """
        raise NotImplementedError("Implement LoggedAttribute.__set__")
    
    def __delete__(self, instance: object) -> None:
        """Delete value and log the operation.
        
        Args:
            instance: The instance
        """
        raise NotImplementedError("Implement LoggedAttribute.__delete__")
    
    @classmethod
    def clear_logs(cls) -> None:
        """Clear all logged entries."""
        raise NotImplementedError("Implement LoggedAttribute.clear_logs")
    
    @classmethod
    def get_logs_for_instance(cls, instance: object) -> list[LogEntry]:
        """Get all logs for a specific instance.
        
        Args:
            instance: The instance to filter by
            
        Returns:
            List of log entries for the instance
        """
        raise NotImplementedError("Implement LoggedAttribute.get_logs_for_instance")


class User:
    """A user with logged attributes.
    
    Attributes (logged):
        username: User's username
        email: User's email
        active: Whether account is active
    """
    
    username = LoggedAttribute("")
    email = LoggedAttribute("")
    active = LoggedAttribute(True)
    
    def __init__(self, username: str, email: str) -> None:
        """Initialize user.
        
        Args:
            username: Username
            email: Email address
        """
        raise NotImplementedError("Implement User.__init__")
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        raise NotImplementedError("Implement User.deactivate")
    
    def get_activity_log(self) -> list[LogEntry]:
        """Get all log entries for this user.
        
        Returns:
            List of log entries
        """
        raise NotImplementedError("Implement User.get_activity_log")


class BankAccount:
    """A bank account with logged balance changes.
    
    Attributes (logged):
        balance: Account balance
        account_type: Type of account
    """
    
    balance = LoggedAttribute(0.0)
    account_type = LoggedAttribute("checking")
    
    def __init__(self, account_type: str = "checking", initial_balance: float = 0.0) -> None:
        """Initialize account.
        
        Args:
            account_type: Type of account
            initial_balance: Starting balance
        """
        raise NotImplementedError("Implement BankAccount.__init__")
    
    def deposit(self, amount: float) -> None:
        """Deposit money into the account.
        
        Args:
            amount: Amount to deposit
            
        Raises:
            ValueError: If amount is negative
        """
        raise NotImplementedError("Implement BankAccount.deposit")
    
    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw
            
        Raises:
            ValueError: If amount is negative or exceeds balance
        """
        raise NotImplementedError("Implement BankAccount.withdraw")
    
    def get_transaction_history(self) -> list[LogEntry]:
        """Get all balance change logs.
        
        Returns:
            List of log entries for balance changes
        """
        raise NotImplementedError("Implement BankAccount.get_transaction_history")


# Hints for Logged Attribute (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to log every access and modification. Think about using Python's logging
# module and where to inject the log calls (in __get__ and __set__).
#
# Hint 2 - Structural plan:
# - Accept a logger or logger name in __init__
# - In __get__, log at DEBUG level before returning the value
# - In __set__, log at INFO level with old and new values
# - Store the actual value in instance.__dict__ or a private storage
# - Make sure to handle AttributeError when value hasn't been set yet
#
# Hint 3 - Edge-case warning:
# For the access log in __get__, you'll need to handle the case where the attribute
# hasn't been set yet (AttributeError). Don't let your logging crash the getter!
