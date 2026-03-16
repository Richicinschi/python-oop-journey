"""Problem 10: Fallback Value Resolver

Topic: Multiple Exception Handling
Difficulty: Medium

Try multiple value sources and return the first valid one.

Examples:
    >>> def source1(): raise ValueError("fail")
    >>> def source2(): return "success"
    >>> def source3(): return "also success"
    >>> fallback_value_resolver([source1, source2, source3])
    'success'
    
    >>> fallback_value_resolver([lambda: 42])
    42
    
    >>> fallback_value_resolver([])
    Traceback (most recent call last):
        ...
    ValueError: No sources provided

Requirements:
    - Try each source function in order until one succeeds
    - Return the first successful result
    - Raise ValueError if no sources provided
    - Raise the last exception if all sources fail
    - Handle any exception type from source functions
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def fallback_value_resolver(sources: list[Callable[[], T]]) -> T:
    """Try multiple sources and return the first valid result.

    Args:
        sources: List of callable functions that return a value

    Returns:
        The first successful result from the sources

    Raises:
        ValueError: If sources list is empty
        Exception: The last exception if all sources fail
    """
    raise NotImplementedError("Implement fallback_value_resolver")
