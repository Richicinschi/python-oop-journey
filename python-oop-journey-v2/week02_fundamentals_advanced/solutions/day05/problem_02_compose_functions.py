"""Problem 02: Compose Functions - Solution

Implement function composition utilities to combine multiple functions
into a single function where the output of one is the input of the next.
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


def compose_two(f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    """Compose two functions: compose_two(f, g)(x) == f(g(x)).

    Args:
        f: The outer function.
        g: The inner function.

    Returns:
        A new function that is the composition of f and g.

    Example:
        >>> def add_one(x: int) -> int:
        ...     return x + 1
        >>> def double(x: int) -> int:
        ...     return x * 2
        >>> h = compose_two(double, add_one)
        >>> h(3)  # double(add_one(3)) = double(4) = 8
        8
    """
    return lambda x: f(g(x))


def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """Compose multiple functions right to left.

    compose(f, g, h)(x) == f(g(h(x)))

    Args:
        *functions: Functions to compose, applied right to left.

    Returns:
        A new function that is the composition of all functions.

    Example:
        >>> def add_one(x: int) -> int:
        ...     return x + 1
        >>> def double(x: int) -> int:
        ...     return x * 2
        >>> h = compose(add_one, double, add_one)
        >>> h(3)  # add_one(double(add_one(3))) = add_one(double(4)) = add_one(8) = 9
        9
    """
    def composed(x: T) -> T:
        result = x
        # Apply functions from right to left
        for f in reversed(functions):
            result = f(result)
        return result
    return composed


def pipe(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """Pipe multiple functions left to right (opposite of compose).

    pipe(f, g, h)(x) == h(g(f(x)))

    Args:
        *functions: Functions to pipe, applied left to right.

    Returns:
        A new function that pipes through all functions.

    Example:
        >>> def add_one(x: int) -> int:
        ...     return x + 1
        >>> def double(x: int) -> int:
        ...     return x * 2
        >>> h = pipe(add_one, double, add_one)
        >>> h(3)  # add_one(double(add_one(3))) = add_one(double(4)) = add_one(8) = 9
        9
    """
    def piped(x: T) -> T:
        result = x
        # Apply functions from left to right
        for f in functions:
            result = f(result)
        return result
    return piped
