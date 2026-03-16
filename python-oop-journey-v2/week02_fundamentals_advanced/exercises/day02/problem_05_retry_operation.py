"""Problem 05: Retry Operation

Topic: Exception Handling in Loops
Difficulty: Medium

Implement a function that retries an operation multiple times on failure.

Examples:
    >>> def fail_twice():
    ...     fail_twice.calls = getattr(fail_twice, 'calls', 0) + 1
    ...     if fail_twice.calls < 3:
    ...         raise ValueError("Not yet")
    ...     return "success"
    >>> retry_operation(fail_twice, max_attempts=5)
    'success'
    >>> retry_operation(lambda: 42, max_attempts=1)
    42

Requirements:
    - Execute the function up to max_attempts times
    - Return the result on first successful execution
    - If all attempts fail, raise the last exception
    - Wait 0.1 seconds between retries (use time.sleep)

Hints:
    * Hint 1: Use a loop that counts attempts. You'll need to catch exceptions
      inside the loop and decide whether to retry or re-raise.
    
    * Hint 2: Structure your code like this:
      - Validate max_attempts first (raise ValueError if < 1)
      - Loop from 1 to max_attempts:
        - Try to call the function and return result
        - If exception occurs, save it and sleep if not the last attempt
      - After loop, raise the last saved exception
    
    * Hint 3: The last exception should only be raised after all attempts
      are exhausted. Don't forget to import time for the sleep delay.

Debugging Tips:
    - If your function hangs: Check that you're actually incrementing the
      attempt counter and not creating an infinite loop
    - If exceptions aren't caught: Ensure your try/except is INSIDE the loop
    - If the last exception is lost: Store it in a variable before sleeping
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def retry_operation(func: Callable[[], T], max_attempts: int) -> T:
    """Retry a function multiple times on failure.

    Args:
        func: The function to execute (takes no arguments)
        max_attempts: Maximum number of attempts to make

    Returns:
        The result of the function call

    Raises:
        ValueError: If max_attempts is less than 1
        Exception: The last exception raised if all attempts fail
    """
    raise NotImplementedError("Implement retry_operation")
