"""Problem 05: Exception Classifier

Topic: Common Exceptions
Difficulty: Medium

Write a function that classifies what exception would occur
when performing an operation on given data.

Operations:
- "divide": division (a / b)
- "index": list indexing (data[index])
- "key": dictionary access (data[key])
- "convert_int": int conversion (int(data))
- "concat": string concatenation (a + b)

Return the exception type name that would occur, or "None" if no error.

Examples:
    >>> classify_exception("divide", 10, 0)
    'ZeroDivisionError'
    >>> classify_exception("key", {"a": 1}, "b")
    'KeyError'
    >>> classify_exception("divide", 10, 2)
    'None'

Requirements:
    - Return the exception type name as string
    - Return "None" if operation would succeed
    - Handle all five operation types

HINTS:
    Hint 1 (Conceptual): You need to simulate each operation and catch exceptions.
        Use a try/except block to attempt the operation.
        If an exception occurs, return its class name.
        If no exception, return "None".

    Hint 2 (Structural):
        - Use if/elif to handle different operation types
        - Inside each branch, use try/except
        - For "divide": try args[0] / args[1], catch ZeroDivisionError
        - For "index": try args[0][args[1]], catch IndexError
        - For "key": try args[0][args[1]], catch KeyError
        - For "convert_int": try int(args[0]), catch ValueError
        - For "concat": try args[0] + args[1], catch TypeError

    Hint 3 (Edge Cases):
        - Division by zero: ZeroDivisionError
        - Index out of range: IndexError
        - Missing key: KeyError
        - Invalid int conversion: ValueError
        - Adding incompatible types: TypeError
        - Watch out for other exceptions that might occur!

DEBUGGING TIPS:
    - Use a broad except Exception as e to catch any exception, then check type(e).__name__
    - Print the operation and args to see what you're handling: print(f"{operation}: {args}")
    - Remember that "None" is a string return value, not Python's None
    - For concat operation, both TypeError can occur with incompatible types
"""

from __future__ import annotations


def classify_exception(operation: str, *args) -> str:
    """Classify what exception would occur for an operation.

    Args:
        operation: The operation type ("divide", "index", "key", "convert_int", "concat")
        *args: Arguments for the operation

    Returns:
        Exception type name or "None" if no error
    """
    raise NotImplementedError("Implement classify_exception")
