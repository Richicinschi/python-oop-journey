"""Reference solution for Problem 09: Timer Context Manager."""

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

    def __init__(self) -> None:
        """Initialize the timer."""
        self.elapsed: float = 0.0
        self._start_time: float = 0.0

    def __enter__(self) -> Timer:
        """Enter the context and start timing."""
        self._start_time = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and stop timing."""
        self.elapsed = time.perf_counter() - self._start_time
