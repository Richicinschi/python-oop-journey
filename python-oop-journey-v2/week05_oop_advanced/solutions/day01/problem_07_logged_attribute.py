"""Reference solution for Problem 07: Logged Attribute."""

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
    """A log entry for an attribute operation."""
    operation: Operation
    instance_id: int
    attribute_name: str
    old_value: Any = None
    new_value: Any = None


class LoggedAttribute:
    """A descriptor that logs all access operations."""
    
    logs: list[LogEntry] = []
    
    def __init__(
        self, 
        default: Any = None,
        log_callback: Callable[[LogEntry], None] | None = None
    ) -> None:
        self.default = default
        self.log_callback = log_callback
        self.name = ""
        self.storage_name = ""
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"
    
    def _log(self, entry: LogEntry) -> None:
        LoggedAttribute.logs.append(entry)
        if self.log_callback:
            self.log_callback(entry)
    
    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        
        value = getattr(instance, self.storage_name, self.default)
        self._log(LogEntry(
            operation=Operation.GET,
            instance_id=id(instance),
            attribute_name=self.name,
            old_value=None,
            new_value=value
        ))
        return value
    
    def __set__(self, instance: object, value: Any) -> None:
        old_value = getattr(instance, self.storage_name, self.default)
        setattr(instance, self.storage_name, value)
        self._log(LogEntry(
            operation=Operation.SET,
            instance_id=id(instance),
            attribute_name=self.name,
            old_value=old_value,
            new_value=value
        ))
    
    def __delete__(self, instance: object) -> None:
        old_value = getattr(instance, self.storage_name, None)
        delattr(instance, self.storage_name)
        self._log(LogEntry(
            operation=Operation.DELETE,
            instance_id=id(instance),
            attribute_name=self.name,
            old_value=old_value,
            new_value=None
        ))
    
    @classmethod
    def clear_logs(cls) -> None:
        cls.logs.clear()
    
    @classmethod
    def get_logs_for_instance(cls, instance: object) -> list[LogEntry]:
        instance_id = id(instance)
        return [log for log in cls.logs if log.instance_id == instance_id]


class User:
    """A user with logged attributes."""
    
    username = LoggedAttribute("")
    email = LoggedAttribute("")
    active = LoggedAttribute(True)
    
    def __init__(self, username: str, email: str) -> None:
        self.username = username
        self.email = email
        self.active = True
    
    def deactivate(self) -> None:
        self.active = False
    
    def get_activity_log(self) -> list[LogEntry]:
        return LoggedAttribute.get_logs_for_instance(self)


class BankAccount:
    """A bank account with logged balance changes."""
    
    balance = LoggedAttribute(0.0)
    account_type = LoggedAttribute("checking")
    
    def __init__(self, account_type: str = "checking", initial_balance: float = 0.0) -> None:
        self.account_type = account_type
        self.balance = initial_balance
    
    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Cannot deposit negative amount")
        self.balance += amount
    
    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Cannot withdraw negative amount")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_transaction_history(self) -> list[LogEntry]:
        return [
            log for log in LoggedAttribute.get_logs_for_instance(self)
            if log.attribute_name == "balance" and log.operation == Operation.SET
        ]
