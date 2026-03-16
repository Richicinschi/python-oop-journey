"""Reference solution for Problem 01: Trace Debug."""

from __future__ import annotations


def trace_calculation(value: int) -> list:
    """Trace a calculation and return debug information.

    Args:
        value: The starting value

    Returns:
        A list of trace strings
    """
    traces = []
    
    # Step 1: Initial value
    current = value
    traces.append(f"start: {current}")
    
    # Step 2: Add 5
    current = current + 5
    traces.append(f"after_add: {current}")
    
    # Step 3: Multiply by 2
    current = current * 2
    traces.append(f"after_multiply: {current}")
    
    # Step 4: Final result
    traces.append(f"final: {current}")
    
    return traces
