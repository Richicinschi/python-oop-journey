"""Reference solution for Problem 03: Command Dispatcher."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class CommandContext:
    """Context passed to command execution."""
    args: list[str] = field(default_factory=list)
    environment: dict[str, Any] = field(default_factory=dict)
    
    def get_arg(self, index: int, default: str = "") -> str:
        """Get argument at index with default value."""
        if 0 <= index < len(self.args):
            return self.args[index]
        return default
    
    def get_arg_count(self) -> int:
        """Get number of arguments."""
        return len(self.args)


class Command(ABC):
    """Abstract base class for commands."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the primary command name."""
        ...
    
    @property
    def aliases(self) -> list[str]:
        """Return list of command aliases. Default: empty list."""
        return []
    
    @abstractmethod
    def execute(self, context: CommandContext) -> str:
        """Execute the command with given context. Return result message."""
        ...


class Middleware(Protocol):
    """Protocol for command middleware/interceptors."""
    
    def process(self, command_name: str, context: CommandContext) -> bool:
        """
        Process a command before execution.
        
        Returns:
            True to allow command execution, False to block
        """
        ...


class CommandDispatcher:
    """Routes commands to their handlers."""
    
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}  # primary name -> command
        self._aliases: dict[str, str] = {}  # alias -> primary name
        self._middleware: list[Middleware] = []
    
    def register(self, command: Command) -> None:
        """Register a command and its aliases."""
        self._commands[command.name] = command
        for alias in command.aliases:
            self._aliases[alias] = command.name
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Add middleware to the chain."""
        self._middleware.append(middleware)
    
    def dispatch(self, name: str, context: CommandContext) -> str:
        """
        Dispatch a command by name.
        
        Args:
            name: Command name or alias
            context: Execution context
            
        Returns:
            Command result or error message
        """
        # Resolve alias if needed
        primary_name = self._aliases.get(name, name)
        
        # Check if command exists
        if command := self._commands.get(primary_name):
            # Run middleware
            for middleware in self._middleware:
                if not middleware.process(primary_name, context):
                    return f"Command '{name}' blocked by middleware"
            
            return command.execute(context)
        
        return f"Unknown command: {name}"
    
    def get_command_names(self) -> list[str]:
        """Get all registered primary command names."""
        return list(self._commands.keys())
    
    def is_registered(self, name: str) -> bool:
        """Check if a command or alias is registered."""
        return name in self._commands or name in self._aliases
    
    def get_aliases(self, command_name: str) -> list[str]:
        """Get all aliases for a command."""
        return [alias for alias, primary in self._aliases.items() if primary == command_name]


# Example command implementations

class HelpCommand(Command):
    """Command to list available commands."""
    
    def __init__(self, dispatcher: CommandDispatcher) -> None:
        self._dispatcher = dispatcher
    
    @property
    def name(self) -> str:
        return "help"
    
    @property
    def aliases(self) -> list[str]:
        return ["?", "h"]
    
    def execute(self, context: CommandContext) -> str:
        names = sorted(self._dispatcher.get_command_names())
        return "Available commands: " + ", ".join(names)


class EchoCommand(Command):
    """Command to echo arguments."""
    
    @property
    def name(self) -> str:
        return "echo"
    
    def execute(self, context: CommandContext) -> str:
        return " ".join(context.args) if context.args else ""


class MathCommand(Command):
    """Command for basic math operations."""
    
    @property
    def name(self) -> str:
        return "math"
    
    @property
    def aliases(self) -> list[str]:
        return ["calc", "calculate"]
    
    def execute(self, context: CommandContext) -> str:
        if context.get_arg_count() < 3:
            return "Usage: math <num1> <op> <num2>"
        
        try:
            num1 = float(context.get_arg(0))
            op = context.get_arg(1)
            num2 = float(context.get_arg(2))
            
            match op:
                case "+":
                    return str(num1 + num2)
                case "-":
                    return str(num1 - num2)
                case "*":
                    return str(num1 * num2)
                case "/":
                    if num2 == 0:
                        return "Error: Division by zero"
                    return str(num1 / num2)
                case _:
                    return f"Unknown operator: {op}"
        except ValueError:
            return "Error: Invalid numbers"


class GreetCommand(Command):
    """Command to greet a user."""
    
    @property
    def name(self) -> str:
        return "greet"
    
    @property
    def aliases(self) -> list[str]:
        return ["hello", "hi"]
    
    def execute(self, context: CommandContext) -> str:
        name = context.get_arg(0, "World")
        return f"Hello, {name}!"


# Example middleware implementations

class LoggingMiddleware:
    """Middleware that logs commands."""
    
    def __init__(self) -> None:
        self.logged_commands: list[tuple[str, CommandContext]] = []
    
    def process(self, command_name: str, context: CommandContext) -> bool:
        self.logged_commands.append((command_name, context))
        return True  # Always allow


class AuthMiddleware:
    """Middleware that checks authentication."""
    
    def __init__(self, protected_commands: list[str] | None = None) -> None:
        self.protected_commands = set(protected_commands or [])
    
    def process(self, command_name: str, context: CommandContext) -> bool:
        # Always allow if user is authenticated
        if context.environment.get("authenticated", False):
            return True
        # If protected_commands is defined and user is not authenticated, block all commands
        if self.protected_commands:
            return False
        # No protected commands defined, allow all
        return True


class RateLimitMiddleware:
    """Middleware that rate limits commands."""
    
    def __init__(self, max_calls: int = 3) -> None:
        self.max_calls = max_calls
        self.call_counts: dict[str, int] = {}
    
    def process(self, command_name: str, context: CommandContext) -> bool:
        count = self.call_counts.get(command_name, 0)
        if count >= self.max_calls:
            return False
        self.call_counts[command_name] = count + 1
        return True
