"""Tests for Problem 02: Import Tracker."""

from __future__ import annotations

from week02_fundamentals_advanced.solutions.day03.problem_02_import_tracker import (
    track_calls,
    get_call_count,
    get_all_call_counts,
    reset_call_counts,
)


def test_track_single_call() -> None:
    """Test tracking a single function call."""
    reset_call_counts()
    
    @track_calls
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    greet("Alice")
    assert get_call_count(greet) == 1


def test_track_multiple_calls() -> None:
    """Test tracking multiple function calls."""
    reset_call_counts()
    
    @track_calls
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    greet("Alice")
    greet("Bob")
    greet("Charlie")
    
    assert get_call_count(greet) == 3


def test_track_multiple_functions() -> None:
    """Test tracking multiple different functions."""
    reset_call_counts()
    
    @track_calls
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    @track_calls
    def farewell(name: str) -> str:
        return f"Goodbye, {name}!"
    
    greet("Alice")
    greet("Bob")
    farewell("Charlie")
    
    assert get_call_count(greet) == 2
    assert get_call_count(farewell) == 1


def test_get_all_call_counts() -> None:
    """Test getting all call counts."""
    reset_call_counts()
    
    @track_calls
    def func1() -> None:
        pass
    
    @track_calls
    def func2() -> None:
        pass
    
    func1()
    func2()
    func2()
    
    counts = get_all_call_counts()
    assert len(counts) == 2
    # Keys should include module and function name
    assert any("func1" in key for key in counts)
    assert any("func2" in key for key in counts)


def test_reset_call_counts() -> None:
    """Test resetting call counts."""
    reset_call_counts()
    
    @track_calls
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    greet("Alice")
    greet("Bob")
    assert get_call_count(greet) == 2
    
    reset_call_counts()
    assert get_call_count(greet) == 0


def test_decorator_preserves_function() -> None:
    """Test that decorator preserves function behavior."""
    reset_call_counts()
    
    @track_calls
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    result = add(2, 3)
    assert result == 5
    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."


def test_get_call_count_unknown_function() -> None:
    """Test getting call count for untracked function."""
    reset_call_counts()
    
    def untracked() -> None:
        pass
    
    assert get_call_count(untracked) == 0
