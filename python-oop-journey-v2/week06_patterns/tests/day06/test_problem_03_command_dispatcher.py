"""Tests for Problem 03: Command Dispatcher."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day06.problem_03_command_dispatcher import (
    CommandContext,
    CommandDispatcher,
    HelpCommand,
    EchoCommand,
    MathCommand,
    GreetCommand,
    LoggingMiddleware,
    AuthMiddleware,
    RateLimitMiddleware,
)


class TestCommandContext:
    """Test command context."""
    
    def test_default_construction(self) -> None:
        ctx = CommandContext()
        
        assert ctx.args == []
        assert ctx.environment == {}
    
    def test_get_arg_with_values(self) -> None:
        ctx = CommandContext(args=["hello", "world"])
        
        assert ctx.get_arg(0) == "hello"
        assert ctx.get_arg(1) == "world"
    
    def test_get_arg_out_of_range(self) -> None:
        ctx = CommandContext(args=["hello"])
        
        assert ctx.get_arg(1) == ""
        assert ctx.get_arg(5) == ""
    
    def test_get_arg_with_default(self) -> None:
        ctx = CommandContext(args=[])
        
        assert ctx.get_arg(0, "default") == "default"
    
    def test_get_arg_count(self) -> None:
        ctx = CommandContext(args=["a", "b", "c"])
        
        assert ctx.get_arg_count() == 3


class TestCommandDispatcher:
    """Test command dispatcher."""
    
    def test_register_command(self) -> None:
        dispatcher = CommandDispatcher()
        cmd = EchoCommand()
        
        dispatcher.register(cmd)
        
        assert "echo" in dispatcher.get_command_names()
    
    def test_dispatch_command(self) -> None:
        dispatcher = CommandDispatcher()
        dispatcher.register(EchoCommand())
        ctx = CommandContext(args=["hello", "world"])
        
        result = dispatcher.dispatch("echo", ctx)
        
        assert result == "hello world"
    
    def test_dispatch_unknown_command(self) -> None:
        dispatcher = CommandDispatcher()
        ctx = CommandContext()
        
        result = dispatcher.dispatch("unknown", ctx)
        
        assert "Unknown command" in result
    
    def test_is_registered_primary(self) -> None:
        dispatcher = CommandDispatcher()
        dispatcher.register(EchoCommand())
        
        assert dispatcher.is_registered("echo") is True
    
    def test_is_registered_alias(self) -> None:
        dispatcher = CommandDispatcher()
        dispatcher.register(GreetCommand())
        
        assert dispatcher.is_registered("hello") is True
        assert dispatcher.is_registered("hi") is True
    
    def test_is_not_registered(self) -> None:
        dispatcher = CommandDispatcher()
        
        assert dispatcher.is_registered("unknown") is False
    
    def test_dispatch_via_alias(self) -> None:
        dispatcher = CommandDispatcher()
        dispatcher.register(GreetCommand())
        ctx = CommandContext(args=["Alice"])
        
        result = dispatcher.dispatch("hello", ctx)
        
        assert result == "Hello, Alice!"


class TestEchoCommand:
    """Test echo command."""
    
    def test_name(self) -> None:
        cmd = EchoCommand()
        
        assert cmd.name == "echo"
    
    def test_execute_with_args(self) -> None:
        cmd = EchoCommand()
        ctx = CommandContext(args=["one", "two", "three"])
        
        result = cmd.execute(ctx)
        
        assert result == "one two three"
    
    def test_execute_empty(self) -> None:
        cmd = EchoCommand()
        ctx = CommandContext(args=[])
        
        result = cmd.execute(ctx)
        
        assert result == ""


class TestGreetCommand:
    """Test greet command."""
    
    def test_name(self) -> None:
        cmd = GreetCommand()
        
        assert cmd.name == "greet"
    
    def test_aliases(self) -> None:
        cmd = GreetCommand()
        
        assert "hello" in cmd.aliases
        assert "hi" in cmd.aliases
    
    def test_execute_with_name(self) -> None:
        cmd = GreetCommand()
        ctx = CommandContext(args=["Bob"])
        
        result = cmd.execute(ctx)
        
        assert result == "Hello, Bob!"
    
    def test_execute_default(self) -> None:
        cmd = GreetCommand()
        ctx = CommandContext(args=[])
        
        result = cmd.execute(ctx)
        
        assert result == "Hello, World!"


class TestMathCommand:
    """Test math command."""
    
    def test_name(self) -> None:
        cmd = MathCommand()
        
        assert cmd.name == "math"
    
    def test_aliases(self) -> None:
        cmd = MathCommand()
        
        assert "calc" in cmd.aliases
        assert "calculate" in cmd.aliases
    
    def test_addition(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["5", "+", "3"])
        
        result = cmd.execute(ctx)
        
        assert result == "8.0"
    
    def test_subtraction(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["10", "-", "4"])
        
        result = cmd.execute(ctx)
        
        assert result == "6.0"
    
    def test_multiplication(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["6", "*", "7"])
        
        result = cmd.execute(ctx)
        
        assert result == "42.0"
    
    def test_division(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["15", "/", "3"])
        
        result = cmd.execute(ctx)
        
        assert result == "5.0"
    
    def test_division_by_zero(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["10", "/", "0"])
        
        result = cmd.execute(ctx)
        
        assert "Division by zero" in result
    
    def test_unknown_operator(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["5", "^", "2"])
        
        result = cmd.execute(ctx)
        
        assert "Unknown operator" in result
    
    def test_insufficient_args(self) -> None:
        cmd = MathCommand()
        ctx = CommandContext(args=["5", "+"])
        
        result = cmd.execute(ctx)
        
        assert "Usage:" in result


class TestHelpCommand:
    """Test help command."""
    
    def test_shows_registered_commands(self) -> None:
        dispatcher = CommandDispatcher()
        dispatcher.register(EchoCommand())
        dispatcher.register(GreetCommand())
        help_cmd = HelpCommand(dispatcher)
        dispatcher.register(help_cmd)
        
        result = help_cmd.execute(CommandContext())
        
        assert "echo" in result
        assert "greet" in result
        assert "help" in result


class TestLoggingMiddleware:
    """Test logging middleware."""
    
    def test_logs_commands(self) -> None:
        middleware = LoggingMiddleware()
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(middleware)
        dispatcher.register(EchoCommand())
        
        dispatcher.dispatch("echo", CommandContext(args=["test"]))
        
        assert len(middleware.logged_commands) == 1
        assert middleware.logged_commands[0][0] == "echo"
    
    def test_allows_execution(self) -> None:
        middleware = LoggingMiddleware()
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(middleware)
        dispatcher.register(EchoCommand())
        
        result = dispatcher.dispatch("echo", CommandContext(args=["hello"]))
        
        assert result == "hello"


class TestAuthMiddleware:
    """Test authentication middleware."""
    
    def test_blocks_unauthenticated(self) -> None:
        auth = AuthMiddleware(protected_commands=["secret"])
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(auth)
        dispatcher.register(EchoCommand())
        
        result = dispatcher.dispatch("echo", CommandContext(args=[], environment={}))
        
        assert "blocked by middleware" in result
    
    def test_allows_authenticated(self) -> None:
        auth = AuthMiddleware(protected_commands=["echo"])
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(auth)
        dispatcher.register(EchoCommand())
        
        ctx = CommandContext(args=["hello"], environment={"authenticated": True})
        result = dispatcher.dispatch("echo", ctx)
        
        assert result == "hello"
    
    def test_allows_unprotected_when_no_protection_defined(self) -> None:
        """When no protected commands defined, all commands are allowed."""
        auth = AuthMiddleware(protected_commands=[])
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(auth)
        dispatcher.register(EchoCommand())
        
        result = dispatcher.dispatch("echo", CommandContext(args=["hello"]))
        
        assert result == "hello"


class TestRateLimitMiddleware:
    """Test rate limiting middleware."""
    
    def test_allows_within_limit(self) -> None:
        limiter = RateLimitMiddleware(max_calls=2)
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(limiter)
        dispatcher.register(EchoCommand())
        
        dispatcher.dispatch("echo", CommandContext())
        result = dispatcher.dispatch("echo", CommandContext())
        
        assert "blocked" not in result
    
    def test_blocks_over_limit(self) -> None:
        limiter = RateLimitMiddleware(max_calls=2)
        dispatcher = CommandDispatcher()
        dispatcher.add_middleware(limiter)
        dispatcher.register(EchoCommand())
        
        dispatcher.dispatch("echo", CommandContext())
        dispatcher.dispatch("echo", CommandContext())
        result = dispatcher.dispatch("echo", CommandContext())  # Third call
        
        assert "blocked" in result


class TestIntegration:
    """Integration tests."""
    
    def test_full_command_system(self) -> None:
        """Test dispatcher with commands, aliases, and middleware."""
        dispatcher = CommandDispatcher()
        
        # Register commands
        dispatcher.register(EchoCommand())
        dispatcher.register(GreetCommand())
        dispatcher.register(MathCommand())
        dispatcher.register(HelpCommand(dispatcher))
        
        # Add middleware
        dispatcher.add_middleware(LoggingMiddleware())
        
        # Test via primary name
        assert dispatcher.dispatch("echo", CommandContext(args=["test"])) == "test"
        
        # Test via alias
        assert dispatcher.dispatch("hello", CommandContext(args=["World"])) == "Hello, World!"
        assert dispatcher.dispatch("calc", CommandContext(args=["2", "+", "3"])) == "5.0"
        
        # Test help
        result = dispatcher.dispatch("help", CommandContext())
        assert "echo" in result
        assert "greet" in result
