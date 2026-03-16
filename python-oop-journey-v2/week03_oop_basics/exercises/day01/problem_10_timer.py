"""Problem 10: Timer

Topic: Time tracking, state persistence
Difficulty: Medium

Create a Timer class that tracks elapsed time.

Examples:
    >>> import time
    >>> timer = Timer()
    >>> timer.start()
    >>> time.sleep(0.01)  # Sleep for 10ms
    >>> elapsed = timer.elapsed()
    >>> elapsed >= 0.01
    True
    >>> timer.stop()
    >>> paused_time = timer.elapsed()
    >>> time.sleep(0.01)
    >>> timer.elapsed() == paused_time  # Timer is stopped
    True
    >>> timer.start()  # Resume
    >>> time.sleep(0.01)
    >>> timer.elapsed() > paused_time
    True
    >>> timer.reset()
    >>> timer.elapsed()
    0.0
    >>> timer.is_running()
    False

Requirements:
    - Timer tracks elapsed time in seconds (float)
    - start() begins or resumes timing
    - stop() pauses timing
    - reset() clears elapsed time and stops timer
    - elapsed() returns total elapsed time
    - is_running() returns True if timer is currently running
    - Use time.perf_counter() for high precision

Hints:
    - Hint 1: Track _elapsed (accumulated time) and _start_time (when started)
    - Hint 2: elapsed() = _elapsed + (current - _start_time) if running, else _elapsed
    - Hint 3: Handle edge case: calling start() when already running shouldn't reset
"""

from __future__ import annotations

import time


class Timer:
    """A class for tracking elapsed time with start/stop functionality."""

    def __init__(self) -> None:
        """Initialize a new timer in stopped state with 0 elapsed time."""
        raise NotImplementedError("Initialize timer state")

    def start(self) -> None:
        """Start or resume the timer."""
        raise NotImplementedError("Implement start method")

    def stop(self) -> None:
        """Stop or pause the timer."""
        raise NotImplementedError("Implement stop method")

    def reset(self) -> None:
        """Reset elapsed time to 0 and stop the timer."""
        raise NotImplementedError("Implement reset method")

    def elapsed(self) -> float:
        """Return the total elapsed time in seconds."""
        raise NotImplementedError("Implement elapsed method")

    def is_running(self) -> bool:
        """Return True if the timer is currently running."""
        raise NotImplementedError("Implement is_running method")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        raise NotImplementedError("Implement __str__ method")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        raise NotImplementedError("Implement __repr__ method")
