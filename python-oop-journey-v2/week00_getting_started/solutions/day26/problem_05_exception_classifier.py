"""Reference solution for Problem 05: Exception Classifier."""

from __future__ import annotations


def classify_exception(operation: str, *args) -> str:
    """Classify what exception would occur for an operation.

    Args:
        operation: The operation type ("divide", "index", "key", "convert_int", "concat")
        *args: Arguments for the operation

    Returns:
        Exception type name or "None" if no error
    """
    try:
        if operation == "divide":
            if len(args) >= 2:
                args[0] / args[1]
        elif operation == "index":
            if len(args) >= 2:
                args[0][args[1]]
        elif operation == "key":
            if len(args) >= 2 and isinstance(args[0], dict):
                args[0][args[1]]
        elif operation == "convert_int":
            if len(args) >= 1:
                int(args[0])
        elif operation == "concat":
            if len(args) >= 2:
                args[0] + args[1]
        return "None"
    except ZeroDivisionError:
        return "ZeroDivisionError"
    except IndexError:
        return "IndexError"
    except KeyError:
        return "KeyError"
    except ValueError:
        return "ValueError"
    except TypeError:
        return "TypeError"
