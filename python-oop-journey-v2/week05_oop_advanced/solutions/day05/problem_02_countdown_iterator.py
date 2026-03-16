"""Reference solution for Problem 02: Countdown Iterator."""

from __future__ import annotations


class Countdown:
    """An iterator that counts down from start to 0."""
    
    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("start must be non-negative")
        self._start = start
        self._current = start
    
    def __iter__(self) -> Countdown:
        self._current = self._start
        return self
    
    def __next__(self) -> int:
        if self._current < 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


class CountdownWithMessage:
    """A countdown iterator that yields messages instead of numbers."""
    
    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("start must be non-negative")
        self._start = start
        self._current = start
        self._liftoff_shown = False
    
    def __iter__(self) -> CountdownWithMessage:
        self._current = self._start
        self._liftoff_shown = False
        return self
    
    def __next__(self) -> str:
        if self._liftoff_shown:
            raise StopIteration
        
        if self._current > 0:
            message = f"T-minus {self._current}"
            self._current -= 1
            return message
        else:
            self._liftoff_shown = True
            return "Liftoff!"
