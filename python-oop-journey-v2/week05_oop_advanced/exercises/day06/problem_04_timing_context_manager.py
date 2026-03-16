"""Problem 04: Timing Context Manager.

Topic: Context Managers, __enter__, __exit__
Difficulty: Medium

Implement context managers for timing code execution with various features.

Example:
    >>> with Timer() as timer:
    ...     time.sleep(0.1)
    >>> timer.elapsed >= 0.1
    True
    
    >>> with Timer(name="slow_operation", verbose=True) as timer:
    ...     time.sleep(0.1)
    slow_operation: 0.102s
    
    >>> with Timer(threshold=0.05, callback=on_slow) as timer:
    ...     time.sleep(0.1)  # Triggers callback
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Callable


class Timer:
    """A context manager that times code execution.
    
    Features:
    - Measures elapsed time
    - Optional name for identification
    - Optional verbose output
    - Optional threshold warning
    - Optional callback when threshold exceeded
    
    Attributes:
        elapsed: The elapsed time in seconds (available after exit).
        name: The timer name.
    """
    
    def __init__(
        self,
        name: str | None = None,
        verbose: bool = False,
        threshold: float | None = None,
        callback: Callable[[str, float], None] | None = None,
    ) -> None:
        """Initialize the timer.
        
        Args:
            name: Optional name for this timer (used in output).
            verbose: If True, print timing information on exit.
            threshold: If set, call callback when elapsed exceeds this value.
            callback: Function called with (name, elapsed) when threshold exceeded.
        """
        raise NotImplementedError("Implement __init__")
    
    def __enter__(self) -> Timer:
        """Enter the context and start timing.
        
        Returns:
            The Timer instance for access during timing.
        """
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and stop timing.
        
        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.
        """
        raise NotImplementedError("Implement __exit__")
    
    def __str__(self) -> str:
        """Return string representation of the timer result."""
        raise NotImplementedError("Implement __str__")


class TimedBlock:
    """A reusable context manager that accumulates timing statistics.
    
    Unlike Timer which is single-use, TimedBlock can be used multiple
    times to accumulate statistics across multiple timed sections.
    
    Example:
        >>> block = TimedBlock("database_operations")
        >>> with block:
        ...     query1()
        >>> with block:
        ...     query2()
        >>> print(f"Total: {block.total:.3f}s, Count: {block.count}")
        Total: 0.234s, Count: 2
    """
    
    def __init__(self, name: str | None = None) -> None:
        """Initialize the timed block.
        
        Args:
            name: Optional name for identification.
        """
        raise NotImplementedError("Implement __init__")
    
    @property
    def total(self) -> float:
        """Total elapsed time across all uses."""
        raise NotImplementedError("Implement total property")
    
    @property
    def count(self) -> int:
        """Number of times the block has been used."""
        raise NotImplementedError("Implement count property")
    
    @property
    def average(self) -> float:
        """Average elapsed time per use."""
        raise NotImplementedError("Implement average property")
    
    def __enter__(self) -> TimedBlock:
        """Enter the context and start timing."""
        raise NotImplementedError("Implement __enter__")
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and record timing."""
        raise NotImplementedError("Implement __exit__")
    
    def reset(self) -> None:
        """Reset all accumulated statistics."""
        raise NotImplementedError("Implement reset")


# Hints for Timing Context Manager (Medium):
# 
# Hint 1 - Conceptual nudge:
# You need to track time spent in the context. Use time.perf_counter() for
# high-precision timing.
#
# Hint 2 - Structural plan:
# - __enter__ records start time using time.perf_counter()
# - __exit__ calculates elapsed time, stores it
# - elapsed property returns the last measured duration
# - TimerRegistry tracks multiple named timers using a dict
#
# Hint 3 - Edge-case warning:
# What if someone accesses elapsed before using the context? Return 0 or raise?
# Handle nested contexts carefully - don't overwrite start time incorrectly.
    
    def report(self) -> str:
        """Generate a timing report.
        
        Returns:
            Formatted report string with statistics.
        """
        raise NotImplementedError("Implement report")


class TimerGroup:
    """Manages multiple named timers for profiling different sections.
    
    Example:
        >>> group = TimerGroup()
        >>> with group.timer("database"):
        ...     db_query()
        >>> with group.timer("api"):
        ...     api_call()
        >>> print(group.report())
    """
    
    def __init__(self) -> None:
        """Initialize the timer group."""
        raise NotImplementedError("Implement __init__")
    
    def timer(self, name: str) -> Timer:
        """Get or create a named timer.
        
        Args:
            name: The timer name.
        
        Returns:
            A Timer context manager for the named section.
        """
        raise NotImplementedError("Implement timer")
    
    def report(self) -> dict[str, dict[str, float]]:
        """Generate a report of all timer statistics.
        
        Returns:
            Dictionary mapping timer names to their statistics.
        """
        raise NotImplementedError("Implement report")
    
    def reset(self) -> None:
        """Reset all timers."""
        raise NotImplementedError("Implement reset")
