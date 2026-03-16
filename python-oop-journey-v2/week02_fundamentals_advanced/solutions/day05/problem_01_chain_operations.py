"""Problem 01: Chain Operations - Solution

Implement a function that chains multiple operations on data.
Each operation transforms the data and passes it to the next.
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def chain_operations(initial: T, *operations: Callable[[T], T]) -> T:
    """Chain multiple operations on an initial value.

    Each operation receives the result of the previous operation.

    Args:
        initial: The starting value.
        *operations: A sequence of functions to apply in order.

    Returns:
        The result after applying all operations.

    Example:
        >>> def add_one(x: int) -> int:
        ...     return x + 1
        >>> def double(x: int) -> int:
        ...     return x * 2
        >>> chain_operations(5, add_one, double)
        12
    """
    result = initial
    for operation in operations:
        result = operation(result)
    return result


def create_pipeline(*operations: Callable[[str], str]) -> Callable[[str], str]:
    """Create a reusable pipeline of string operations.

    Args:
        *operations: String transformation functions to compose.

    Returns:
        A function that applies all operations in sequence.

    Example:
        >>> pipeline = create_pipeline(str.strip, str.upper)
        >>> pipeline("  hello  ")
        'HELLO'
    """
    def pipeline(text: str) -> str:
        return chain_operations(text, *operations)
    return pipeline


def apply_transformations(data: list[int], *transforms: Callable[[list[int]], list[int]]) -> list[int]:
    """Apply a series of transformations to a list of integers.

    Args:
        data: The initial list of integers.
        *transforms: Transformation functions to apply.

    Returns:
        The transformed list after all operations.
    """
    result = data.copy()
    for transform in transforms:
        result = transform(result)
    return result
