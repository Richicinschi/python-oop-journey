"""Reference solution for Problem 04: Debug Values."""

from __future__ import annotations


def debug_operations(start: int, operations: list) -> list:
    """Track value changes through a series of operations.

    Args:
        start: The starting value
        operations: List of operation strings

    Returns:
        List of (operation, value_after) tuples
    """
    results = []
    current = start
    
    for op in operations:
        parts = op.split("_")
        operation = parts[0]
        
        try:
            value = int(parts[1])
        except (IndexError, ValueError):
            continue
        
        if operation == "add":
            current = current + value
        elif operation == "sub":
            current = current - value
        elif operation == "mul":
            current = current * value
        elif operation == "div":
            if value == 0:
                break  # Stop on division by zero
            current = current // value
        
        results.append((op, current))
    
    return results
