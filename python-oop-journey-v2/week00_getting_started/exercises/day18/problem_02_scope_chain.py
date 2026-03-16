"""Problem 02: Scope Chain

Topic: Variable Scope - LEGB Rule
Difficulty: Medium

Write nested functions that demonstrate the scope chain.

Function Signature:
    def outer_function(x: int) -> int

Requirements:
    - outer_function takes parameter x
    - Define inner_function inside outer_function
    - inner_function should access x from outer scope
    - Return the result of calling inner_function()

Behavior Notes:
    - Python looks for variables in LEGB order:
      L = Local, E = Enclosing, G = Global, B = Built-in
    - inner_function can read x from outer_function
    - This demonstrates the 'E' (Enclosing) in LEGB

Examples:
    >>> outer_function(5)
    10
    
    >>> outer_function(10)
    20

Implementation:
    - inner_function should multiply x by 2
    - outer_function returns inner_function()

"""

from __future__ import annotations


def outer_function(x: int) -> int:
    """Demonstrate scope chain with nested functions.

    Args:
        x: A value from outer scope.

    Returns:
        Result from inner function accessing outer scope.
    """
    raise NotImplementedError("Implement outer_function with inner_function")
