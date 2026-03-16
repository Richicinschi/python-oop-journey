"""Solution for Problem 05: Retry Operation."""

from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_operation(func: Callable[[], T], max_attempts: int) -> T:
    """Retry a function multiple times on failure.

    Args:
        func: The function to execute (takes no arguments)
        max_attempts: Maximum number of attempts to make

    Returns:
        The result of the function call

    Raises:
        ValueError: If max_attempts is less than 1
        Exception: The last exception raised if all attempts fail
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    
    last_exception: Exception | None = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                time.sleep(0.1)
    
    if last_exception is not None:
        raise last_exception
    
    raise RuntimeError("Unexpected: no exception but also no result")
