"""Exercise: Hello World Plus.

Create an improved "Hello, World" program that demonstrates
what you've learned about Python so far.

Learning Goals:
- Write a complete Python program
- Use print() with different options
- Add proper comments
- Follow Python best practices
- Use f-strings for formatting

Instructions:
1. Complete all TODO sections below
2. Run the program to verify it works
3. Check that your output matches the expected format
"""

from __future__ import annotations


def create_greeting(name: str) -> str:
    """Create a personalized greeting message.
    
    Args:
        name: The person's name to include in the greeting.
        
    Returns:
        A greeting string like "Hello, Alice!"
    """
    # TODO 1: Return an f-string greeting in the format:
    # f"Hello, {name}!"
    raise NotImplementedError("Create the greeting using an f-string")


def create_farewell(name: str) -> str:
    """Create a farewell message.
    
    Args:
        name: The person's name to include in the farewell.
        
    Returns:
        A farewell string like "Goodbye, Alice! Have a great day!"
    """
    # TODO 2: Return a farewell message that includes the name
    # Be creative! Include the name and a friendly closing
    raise NotImplementedError("Create a farewell message with the name")


def print_separator() -> None:
    """Print a decorative separator line.
    
    Print a line of 40 dashes to separate sections.
    Hint: You can multiply strings: "-" * 40
    """
    # TODO 3: Print a line of 40 dashes
    # Use string multiplication: "-" * 40
    raise NotImplementedError("Print the separator line")


def print_program_info(program_name: str, version: float) -> None:
    """Print information about the program.
    
    Args:
        program_name: The name of the program.
        version: The version number (e.g., 1.0).
    """
    # TODO 4: Print program information using an f-string
    # Format: "Program: {name} | Version: {version}"
    raise NotImplementedError("Print program info with name and version")


def main() -> None:
    """Main program entry point.
    
    This function orchestrates the program flow:
    1. Set up variables
    2. Print program info
    3. Print greeting
    4. Print some messages
    5. Print farewell
    """
    # TODO 5: Create a variable 'user_name' with your name
    # Example: user_name = "Alice"
    
    # TODO 6: Create a variable 'program_version' with value 1.0
    
    # TODO 7: Call print_separator() to print a separator line
    
    # TODO 8: Call print_program_info() with:
    #   - program_name="Hello World Plus"
    #   - version=program_version
    
    # TODO 9: Call print_separator() again
    
    # TODO 10: Get the greeting by calling create_greeting(user_name)
    # Store it in a variable and print it
    
    # TODO 11: Print an empty line for spacing (just call print())
    
    # TODO 12: Print "This is my first complete Python program!"
    
    # TODO 13: Print "I'm learning about:"
    # Then print three bullet points:
    #   - "Variables and data"
    #   - "Functions"
    #   - "String formatting"
    
    # TODO 14: Print another empty line
    
    # TODO 15: Get the farewell by calling create_farewell(user_name)
    # Store it in a variable and print it
    
    # TODO 16: Call print_separator() one last time
    
    pass  # Remove this after implementing all TODOs


if __name__ == "__main__":
    main()
