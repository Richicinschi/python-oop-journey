"""Solution for Problem 10: Fallback Value Resolver."""

from __future__ import annotations

from typing import Callable, List, TypeVar

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
    if not sources:
        raise ValueError("No sources provided")
    
    last_exception: Exception | None = None
    
    for source in sources:
        try:
            return source()
        except Exception as e:
            last_exception = e
    
    if last_exception is not None:
        raise last_exception
    
    raise RuntimeError("Unexpected: no exception but also no result")
