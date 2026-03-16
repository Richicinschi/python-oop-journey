"""Reference solution for Problem 01: Custom Range Iterator."""

from __future__ import annotations


class CustomRange:
    """A custom implementation of range-like iteration."""
    
    def __init__(self, start: int, stop: int | None = None, step: int = 1) -> None:
        if stop is None:
            stop = start
            start = 0
        
        if step == 0:
            raise ValueError("step cannot be zero")
        
        self.start = start
        self.stop = stop
        self.step = step
        self._current = start
    
    def __iter__(self) -> CustomRange:
        self._current = self.start
        return self
    
    def __next__(self) -> int:
        if self.step > 0 and self._current >= self.stop:
            raise StopIteration
        if self.step < 0 and self._current <= self.stop:
            raise StopIteration
        
        value = self._current
        self._current += self.step
        return value
    
    def __len__(self) -> int:
        if self.step > 0:
            if self.start >= self.stop:
                return 0
            return (self.stop - self.start - 1) // self.step + 1
        else:
            if self.start <= self.stop:
                return 0
            return (self.start - self.stop - 1) // (-self.step) + 1
