"""Problem 03: Command Dispatcher

Topic: Command Pattern, Router
Difficulty: Hard

Implement a command dispatcher using the Command pattern.

HINTS:
- Hint 1 (Conceptual): Dispatcher is a router. Commands are registered by name/alias. 
  Middleware can intercept, modify, or block commands before execution.
- Hint 2 (Structural): Command has: name, aliases, execute(context). Dispatcher 
  has: register(command), dispatch(name, context). Middleware is a callable that 
  returns (modified_context, should_continue).
- Hint 3 (Edge Case): Unknown commands return error message. Aliases resolve to 
  same command. Middleware runs in registration order; if any returns 
  should_continue=False, stop processing.

PATTERN EXPLANATION:
The Command Dispatcher pattern extends the Command pattern with routing
capabilities. Commands are registered with names/aliases, and the dispatcher
routes incoming requests to the appropriate command handler.

STRUCTURE:
- Command: Encapsulates a request as an object
- CommandContext: Holds execution context (args, environment)
- Dispatcher: Routes command names to handlers
- Middleware: Intercepts commands for validation/logging

WHEN TO USE:
- For CLI applications
- For action routing in games
- When commands need preprocessing/postprocessing

EXAMPLE USAGE:
    dispatcher = CommandDispatcher()
    dispatcher.register(HelpCommand())
    dispatcher.register(EchoCommand())  # Has alias "say"
    
    # Dispatch by name
    result = dispatcher.dispatch("help", CommandContext())
    
    # Dispatch by alias
    result = dispatcher.dispatch("say", CommandContext(args=["Hello"]))

Your task:
1. Create a Command base class/interface
2. Create a CommandContext to hold execution context
3. Create a CommandDispatcher that routes commands to handlers
4. Support command aliases
5. Support middleware/interceptors that can modify or block commands

Requirements:
- Commands have a name property and execute(context) method
- CommandContext contains args list and environment dict
- Dispatcher routes by command name
- Aliases allow multiple names for the same command
- Middleware can intercept and modify/block commands
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class CommandContext:
    """Context passed to command execution."""
    # TODO: Define fields for args and environment
    pass
    
    def get_arg(self, index: int, default: str = "") -> str:
        """Get argument at index with default value."""
        raise NotImplementedError("Implement get_arg")


class Command(ABC):
    """Abstract base class for commands."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the primary command name."""
        raise NotImplementedError("Implement name property")
    
    @property
    def aliases(self) -> list[str]:
        """Return list of command aliases. Default: empty list."""
        raise NotImplementedError("Implement aliases property")
    
    @abstractmethod
    def execute(self, context: CommandContext) -> str:
        """Execute the command with given context. Return result message."""
        raise NotImplementedError("Implement execute")


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
        # TODO: Initialize data structures
        pass
    
    def register(self, command: Command) -> None:
        """Register a command and its aliases."""
        raise NotImplementedError("Implement register")
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Add middleware to the chain."""
        raise NotImplementedError("Implement add_middleware")
    
    def dispatch(self, name: str, context: CommandContext) -> str:
        """
        Dispatch a command by name.
        
        Args:
            name: Command name or alias
            context: Execution context
            
        Returns:
            Command result or error message
        """
        raise NotImplementedError("Implement dispatch")
    
    def get_command_names(self) -> list[str]:
        """Get all registered primary command names."""
        raise NotImplementedError("Implement get_command_names")
    
    def is_registered(self, name: str) -> bool:
        """Check if a command or alias is registered."""
        raise NotImplementedError("Implement is_registered")


# TODO: Implement example commands
# Example: HelpCommand, EchoCommand, MathCommand
