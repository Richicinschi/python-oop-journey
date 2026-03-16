"""Problem 01: Local vs Global Variables

Topic: Variable Scope - Local and Global
Difficulty: Easy

Write a function that demonstrates local vs global variable behavior.

Function Signature:
    def demonstrate_local_global() -> dict[str, int]

Requirements:
    - Create a local variable with value 10
    - Access the global variable (defined below)
    - Return a dict showing both values

Behavior Notes:
    - Local variables are created inside functions
    - Global variables are defined at module level
    - Functions can read global variables
    - To modify globals, use 'global' keyword

Global Variable:
    global_counter = 100  # Defined at module level

Examples:
    >>> demonstrate_local_global()
    {'local_value': 10, 'global_value': 100}

Note:
    - Don't use 'global' keyword for this exercise
    - Just read the global variable, don't modify it

"""

from __future__ import annotations

# Global variable
global_counter = 100


def demonstrate_local_global() -> dict[str, int]:
    """Demonstrate local vs global variable behavior.

    Returns:
        A dictionary with local and global values.
    """
    raise NotImplementedError("Implement demonstrate_local_global")
