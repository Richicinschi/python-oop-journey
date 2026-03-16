"""Reference solution for Problem 10: Timer."""

from __future__ import annotations

import time


class Timer:
    """A class for tracking elapsed time with start/stop functionality."""

    def __init__(self) -> None:
        """Initialize a new timer in stopped state with 0 elapsed time."""
        self._elapsed: float = 0.0
        self._start_time: float | None = None
        self._running: bool = False

    def start(self) -> None:
        """Start or resume the timer."""
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True

    def stop(self) -> None:
        """Stop or pause the timer."""
        if self._running:
            self._elapsed += time.perf_counter() - self._start_time
            self._running = False
            self._start_time = None

    def reset(self) -> None:
        """Reset elapsed time to 0 and stop the timer."""
        self._elapsed = 0.0
        self._start_time = None
        self._running = False

    def elapsed(self) -> float:
        """Return the total elapsed time in seconds."""
        if self._running:
            return self._elapsed + (time.perf_counter() - self._start_time)
        return self._elapsed

    def is_running(self) -> bool:
        """Return True if the timer is currently running."""
        return self._running

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        status = "running" if self._running else "stopped"
        return f"Timer({self.elapsed():.4f}s, {status})"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"Timer(elapsed={self.elapsed():.4f}, running={self._running})"
