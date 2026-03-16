"""Decorators for the Task Management System.

Reference implementation of logging, validation, and timing decorators.
"""

from __future__ import annotations

import functools
import time
import warnings
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def log_operation(func: F) -> F:
    """Decorator that logs function calls with arguments and results."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"[LOG] {func.__name__}({signature})")
        
        try:
            result = func(*args, **kwargs)
            print(f"[LOG] {func.__name__} -> {result!r}")
            return result
        except Exception as e:
            print(f"[LOG] {func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper  # type: ignore[return-value]


def timing_decorator(func: F) -> F:
    """Decorator that measures and prints execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMING] {func.__name__} took {elapsed:.4f} seconds")
        return result
    
    return wrapper  # type: ignore[return-value]


def require_permission(permission: str) -> Callable[[F], F]:
    """Decorator factory requiring specific permission on first argument.
    
    Assumes the first argument (self) has a `has_permission` method.
    Raises PermissionError if permission is not granted.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not args:
                raise PermissionError("No self argument found")
            
            instance = args[0]
            if not hasattr(instance, 'has_permission'):
                raise PermissionError("Object has no has_permission method")
            
            # Convert string to Permission enum if needed
            from .user import Permission
            perm = Permission[permission] if isinstance(permission, str) else permission
            
            if not instance.has_permission(perm):
                raise PermissionError(
                    f"Permission denied: {permission} required for {func.__name__}"
                )
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore[return-value]
    
    return decorator


def validate_types(**expected_types: type) -> Callable[[F], F]:
    """Decorator factory for runtime type checking."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get function argument names (skip self if method)
            import inspect
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # Build arg dict
            bound_args: dict[str, Any] = {}
            for i, (name, arg) in enumerate(zip(param_names, args)):
                bound_args[name] = arg
            bound_args.update(kwargs)
            
            # Validate types
            for name, expected_type in expected_types.items():
                if name in bound_args:
                    value = bound_args[name]
                    if value is not None and not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore[return-value]
    
    return decorator


def singleton(cls: type) -> type:
    """Class decorator ensuring only one instance exists."""
    instances: dict[type, Any] = {}
    
    @functools.wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    wrapper.__name__ = cls.__name__
    wrapper.__doc__ = cls.__doc__
    return wrapper


def retry_on_error(max_attempts: int = 3, delay: float = 0.1) -> Callable[[F], F]:
    """Decorator factory for retrying operations on failure."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            
            if last_exception:
                raise last_exception
            return None  # Should not reach here
        
        return wrapper  # type: ignore[return-value]
    
    return decorator


def deprecated(message: str = "This function is deprecated") -> Callable[[F], F]:
    """Decorator factory marking functions as deprecated."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__} is deprecated: {message}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore[return-value]
    
    return decorator


def count_calls(func: F) -> F:
    """Decorator that counts how many times function is called."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.call_count += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)
    
    wrapper.call_count = 0  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]
