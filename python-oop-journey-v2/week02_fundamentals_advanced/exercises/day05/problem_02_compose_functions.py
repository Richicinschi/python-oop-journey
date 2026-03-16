"""Problem 02: Compose Functions

Implement function composition utilities to combine multiple functions
into a single function where the output of one is the input of the next.

Hints:
    * Hint 1: Function composition means f(g(x)) - apply g first, then f.
      For compose_two(f, g), return a new function that takes x and calls
      f(g(x)). Use a lambda or nested function.
    
    * Hint 2: For compose(*functions) with multiple functions:
      - Functions are applied right-to-left (reverse of argument order)
      - reduce() from functools can help: reduce(lambda f, g: lambda x: f(g(x)), functions)
      - Or iterate in reverse, applying each function to the result
    
    * Hint 3: pipe() is like compose() but left-to-right:
      pipe(f, g, h)(x) == h(g(f(x)))
      This is often more intuitive - data flows left to right as you read it

Debugging Tips:
    - "Wrong order of operations": Double-check your direction!
      Compose applies right-to-left, pipe applies left-to-right
    - "Type errors": Ensure type hints match - output of inner function
      must match input of outer function
    - Empty functions list: Return the identity function (lambda x: x)
    - Single function: Just return that function (or equivalent lambda)
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
    raise NotImplementedError("Implement compose_functions")


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
    raise NotImplementedError("Implement compose_functions")


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
    raise NotImplementedError("Implement compose_functions")
