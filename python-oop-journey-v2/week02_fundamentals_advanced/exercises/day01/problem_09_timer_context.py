"""Problem 09: Timer Context Manager

Topic: Context managers
Difficulty: Medium

Create a context manager class that times the execution of a code block.
The timer should record elapsed time and allow querying it after exit.

Examples:
    >>> with Timer() as timer:
    ...     time.sleep(0.1)
    >>> timer.elapsed >= 0.1
    True
    >>> timer.elapsed  # Time in seconds
    0.102...

Requirements:
    - Implement as a class with __enter__ and __exit__ methods
    - Store elapsed time in seconds as 'elapsed' attribute
    - The elapsed attribute should be available after exiting the context
    - Handle exceptions gracefully (still record time even if exception occurs)
    - Use time.perf_counter() for high precision timing
"""

from __future__ import annotations

import time
from types import TracebackType
from typing import Any


class Timer:
    """Context manager that times code execution.
    
    Usage:
        with Timer() as t:
            # code to time
            pass
        print(f"Elapsed: {t.elapsed} seconds")
    """

    def __enter__(self) -> Timer:
        """Enter the context and start timing."""
        raise NotImplementedError("Implement __enter__")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and stop timing."""
        raise NotImplementedError("Implement __exit__")
