"""Reference solution for Problem 04: Timing Context Manager."""

from __future__ import annotations

import time
from types import TracebackType
from typing import Callable


class Timer:
    """A context manager that times code execution.
    
    Features:
    - Measures elapsed time
    - Optional name for identification
    - Optional verbose output
    - Optional threshold warning
    - Optional callback when threshold exceeded
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
        self.name = name or "Timer"
        self.verbose = verbose
        self.threshold = threshold
        self.callback = callback
        self.elapsed: float = 0.0
        self._start_time: float | None = None
    
    def __enter__(self) -> Timer:
        """Enter the context and start timing.
        
        Returns:
            The Timer instance for access during timing.
        """
        self._start_time = time.perf_counter()
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and stop timing."""
        if self._start_time is not None:
            self.elapsed = time.perf_counter() - self._start_time
        
        # Check threshold
        if self.threshold is not None and self.elapsed > self.threshold:
            if self.callback is not None:
                self.callback(self.name, self.elapsed)
        
        # Verbose output
        if self.verbose:
            print(f"{self.name}: {self.elapsed:.3f}s")
    
    def __str__(self) -> str:
        """Return string representation of the timer result."""
        return f"{self.name}: {self.elapsed:.6f}s"


class TimedBlock:
    """A reusable context manager that accumulates timing statistics.
    
    Unlike Timer which is single-use, TimedBlock can be used multiple
    times to accumulate statistics across multiple timed sections.
    """
    
    def __init__(self, name: str | None = None) -> None:
        """Initialize the timed block.
        
        Args:
            name: Optional name for identification.
        """
        self.name = name or "TimedBlock"
        self._total: float = 0.0
        self._count: int = 0
        self._start_time: float | None = None
        self._current_elapsed: float = 0.0
    
    @property
    def total(self) -> float:
        """Total elapsed time across all uses."""
        return self._total
    
    @property
    def count(self) -> int:
        """Number of times the block has been used."""
        return self._count
    
    @property
    def average(self) -> float:
        """Average elapsed time per use."""
        if self._count == 0:
            return 0.0
        return self._total / self._count
    
    @property
    def last(self) -> float:
        """Elapsed time from the most recent use."""
        return self._current_elapsed
    
    def __enter__(self) -> TimedBlock:
        """Enter the context and start timing."""
        self._start_time = time.perf_counter()
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context and record timing."""
        if self._start_time is not None:
            self._current_elapsed = time.perf_counter() - self._start_time
            self._total += self._current_elapsed
            self._count += 1
    
    def reset(self) -> None:
        """Reset all accumulated statistics."""
        self._total = 0.0
        self._count = 0
        self._current_elapsed = 0.0
        self._start_time = None
    
    def report(self) -> str:
        """Generate a timing report.
        
        Returns:
            Formatted report string with statistics.
        """
        lines = [
            f"TimedBlock: {self.name}",
            f"  Count:   {self._count}",
            f"  Total:   {self._total:.6f}s",
            f"  Average: {self.average:.6f}s",
        ]
        if self._count > 0:
            lines.append(f"  Last:    {self._current_elapsed:.6f}s")
        return "\n".join(lines)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.name}: {self._count} calls, {self._total:.6f}s total"


class TimerGroup:
    """Manages multiple named timers for profiling different sections."""
    
    def __init__(self) -> None:
        """Initialize the timer group."""
        self._blocks: dict[str, TimedBlock] = {}
    
    def timer(self, name: str) -> Timer:
        """Get or create a named timer.
        
        Args:
            name: The timer name.
        
        Returns:
            A Timer context manager for the named section.
        """
        if name not in self._blocks:
            self._blocks[name] = TimedBlock(name)
        
        block = self._blocks[name]
        # Return a proxy that updates the block on exit
        return self._TimerProxy(block)
    
    class _TimerProxy:
        """A proxy that wraps a TimedBlock as a single-use Timer."""
        
        def __init__(self, block: TimedBlock) -> None:
            self._block = block
            self._inner_timer: Timer | None = None
        
        def __enter__(self) -> TimerGroup._TimerProxy:
            self._inner_timer = Timer(self._block.name)
            self._inner_timer.__enter__()
            self._block._start_time = time.perf_counter()
            return self
        
        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ) -> None:
            if self._inner_timer is not None:
                self._inner_timer.__exit__(exc_type, exc_val, exc_tb)
            # Update the block stats
            if self._block._start_time is not None:
                elapsed = time.perf_counter() - self._block._start_time
                self._block._total += elapsed
                self._block._count += 1
                self._block._current_elapsed = elapsed
                self._block._start_time = None
        
        @property
        def elapsed(self) -> float:
            """Get the elapsed time."""
            return self._inner_timer.elapsed if self._inner_timer else 0.0
    
    def report(self) -> dict[str, dict[str, float]]:
        """Generate a report of all timer statistics.
        
        Returns:
            Dictionary mapping timer names to their statistics.
        """
        return {
            name: {
                'count': float(block.count),
                'total': block.total,
                'average': block.average,
                'last': block.last,
            }
            for name, block in self._blocks.items()
        }
    
    def reset(self) -> None:
        """Reset all timers."""
        for block in self._blocks.values():
            block.reset()
    
    def __str__(self) -> str:
        """String representation with summary."""
        lines = ["TimerGroup Report:"]
        for name, block in self._blocks.items():
            lines.append(f"  {name}: {block.count} calls, {block.total:.6f}s total")
        return "\n".join(lines)
