"""Solution: Hello World Plus.

A complete "Hello, World" program demonstrating best practices
for beginner Python programmers.
"""

from __future__ import annotations


def create_greeting(name: str) -> str:
    """Create a personalized greeting message.
    
    Args:
        name: The person's name to include in the greeting.
        
    Returns:
        A greeting string like "Hello, Alice!"
        
    Example:
        >>> create_greeting("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"


def create_farewell(name: str) -> str:
    """Create a farewell message.
    
    Args:
        name: The person's name to include in the farewell.
        
    Returns:
        A farewell string like "Goodbye, Alice! Have a great day!"
        
    Example:
        >>> create_farewell("Bob")
        'Goodbye, Bob! Have a great day!'
    """
    return f"Goodbye, {name}! Have a great day!"


def print_separator() -> None:
    """Print a decorative separator line.
    
    Prints a line of 40 dashes to separate sections visually.
    """
    print("-" * 40)


def print_program_info(program_name: str, version: float) -> None:
    """Print information about the program.
    
    Args:
        program_name: The name of the program.
        version: The version number (e.g., 1.0).
        
    Example:
        >>> print_program_info("My App", 2.5)
        Program: My App | Version: 2.5
    """
    print(f"Program: {program_name} | Version: {version}")


def main() -> None:
    """Main program entry point.
    
    Orchestrates the program flow and demonstrates basic Python concepts
    including variables, functions, string formatting, and output.
    """
    # Set up variables
    user_name = "Learner"
    program_version = 1.0
    
    # Print header with separators
    print_separator()
    print_program_info("Hello World Plus", program_version)
    print_separator()
    
    # Print greeting
    greeting = create_greeting(user_name)
    print(greeting)
    print()  # Empty line for spacing
    
    # Program description
    print("This is my first complete Python program!")
    print("I'm learning about:")
    print("  - Variables and data")
    print("  - Functions")
    print("  - String formatting")
    
    # Print farewell
    print()  # Empty line for spacing
    farewell = create_farewell(user_name)
    print(farewell)
    
    # Footer separator
    print_separator()


if __name__ == "__main__":
    main()
