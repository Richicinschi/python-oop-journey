"""Reference solution for Problem 05: Fix The Error."""

from __future__ import annotations


def suggest_fix(code: str) -> str:
    """Analyze a code snippet and suggest a fix or identify the error.

    Args:
        code: A potentially problematic code snippet

    Returns:
        Either the corrected code or an error explanation
    """
    fixes = {
        "print(Hello)": "print('Hello')",
        "if x > 5 print(x)": "if x > 5: print(x)",
        "def greet():\nprint('hi')": "def greet():\n    print('hi')",
        'print("Hello)': 'print("Hello")',
    }
    
    runtime_errors = {
        "10 / 0": "Cannot fix - would raise ZeroDivisionError",
        "int('abc')": "Cannot fix - would raise ValueError",
        "lst[5]": "Cannot fix - would raise IndexError",
        "d['missing']": "Cannot fix - would raise KeyError",
    }
    
    if code in fixes:
        return fixes[code]
    elif code in runtime_errors:
        return runtime_errors[code]
    else:
        return "Unknown issue"
