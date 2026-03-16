"""Reference solution for Problem 04: Validate Types Decorator."""

from __future__ import annotations

from functools import wraps
from typing import Callable, Any, get_type_hints


def validate_types(func: Callable) -> Callable:
    """A decorator that validates function arguments against type hints.
    
    Checks each argument against its type hint before calling the function.
    Raises TypeError if any argument doesn't match its expected type.
    
    Args:
        func: The function to decorate
        
    Returns:
        The wrapper function with type validation
    """
    type_hints = get_type_hints(func)
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Get function parameter names
        import inspect
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # Validate each argument
        for name, value in bound_args.arguments.items():
            if name in type_hints:
                expected_type = type_hints[name]
                # Handle Optional[X] which is Union[X, None]
                origin = getattr(expected_type, '__origin__', None)
                
                if origin is not None:
                    # It's a generic type like Union, List, etc.
                    import typing
                    if origin is typing.Union:
                        # Check if value matches any of the union types
                        args_types = getattr(expected_type, '__args__', ())
                        if not any(isinstance(value, t) for t in args_types if t is not type(None)):
                            if value is not None:
                                raise TypeError(
                                    f"Argument '{name}' must be one of {args_types}, "
                                    f"got {type(value).__name__}"
                                )
                    else:
                        # For other generic types, just check basic type
                        if not isinstance(value, (list, tuple, dict, set) if origin in (list, tuple, dict, set) else (origin,)):
                            raise TypeError(
                                f"Argument '{name}' must be {expected_type}, "
                                f"got {type(value).__name__}"
                            )
                else:
                    # Simple type check
                    if expected_type is not Any and not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
        
        return func(*args, **kwargs)
    
    return wrapper


# Example usage for testing
@validate_types
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@validate_types
def greet(name: str, age: int) -> str:
    """Greet a person."""
    return f"Hello {name}, you are {age} years old"


@validate_types
def optional_value(x: int | None) -> str:
    """Handle optional value."""
    return str(x) if x is not None else "None"
