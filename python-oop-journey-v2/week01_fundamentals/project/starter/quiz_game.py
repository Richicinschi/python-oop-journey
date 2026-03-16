"""
Week 1 Project: CLI Quiz Game - Starter Code

This module implements a simple command-line quiz game.
Complete all TODOs to create a working implementation.

Learning objectives:
- Function design and organization
- Working with lists and dictionaries
- User input/output handling
- Control flow with loops and conditionals
"""

from typing import List, Dict, Any


# Sample quiz questions data structure
# Each question is a dictionary with keys: question, options, answer
QUESTIONS: List[Dict[str, Any]] = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "B"
    },
    {
        "question": "What is 2 + 2 * 2?",
        "options": ["6", "8", "4", "10"],
        "answer": "A"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"],
        "answer": "C"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "D"
    }
]


def load_questions() -> List[Dict[str, Any]]:
    """
    Load and return the list of quiz questions.
    
    Returns:
        A list of dictionaries, each containing:
        - 'question': str, the question text
        - 'options': list of str, the answer choices
        - 'answer': str, the correct answer letter (A, B, C, or D)
    """
    # TODO: Return the QUESTIONS list
    pass


def display_question(question: Dict[str, Any], question_num: int, total: int) -> None:
    """
    Display a single quiz question with its options.
    
    Args:
        question: Dictionary containing question data
        question_num: Current question number (1-indexed)
        total: Total number of questions
    """
    # TODO: Display question header with format "Question X of Y:"
    # TODO: Print the question text
    # TODO: Print each option with its letter (A, B, C, D)
    # HINT: Use enumerate with start=65 and chr() for A, B, C, D
    # Or simply use: for i, option in enumerate(question['options']): ...
    pass


def get_user_answer() -> str:
    """
    Get and validate the user's answer.
    
    Prompts the user until they enter a valid answer (A, B, C, or D).
    Converts input to uppercase.
    
    Returns:
        The user's answer as a single uppercase letter (A-D)
    """
    # TODO: Use a while loop to keep asking until valid input
    # TODO: Get input from user with prompt "Your answer: "
    # TODO: Convert input to uppercase
    # TODO: Check if input is one of: A, B, C, D
    # TODO: If invalid, print error message and loop again
    # TODO: Return valid answer
    pass


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """
    Check if the user's answer is correct.
    
    Args:
        user_answer: The answer provided by the user (A-D)
        correct_answer: The correct answer (A-D)
    
    Returns:
        True if answers match, False otherwise
    """
    # TODO: Compare user_answer with correct_answer (case-insensitive)
    # TODO: Print "Correct!" or "Wrong!" message
    # TODO: Return True if correct, False otherwise
    pass


def calculate_score(correct_count: int, total: int) -> float:
    """
    Calculate the percentage score.
    
    Args:
        correct_count: Number of correct answers
        total: Total number of questions
    
    Returns:
        Percentage score (0.0 - 100.0)
    """
    # TODO: Calculate percentage: (correct / total) * 100
    # TODO: Handle case where total is 0 to avoid division by zero
    # TODO: Return the percentage as a float
    pass


def display_results(score: int, total: int, percentage: float) -> None:
    """
    Display the final quiz results.
    
    Args:
        score: Number of correct answers
        total: Total number of questions
        percentage: Percentage score (0.0 - 100.0)
    """
    # TODO: Print a results header with formatting (e.g., ============)
    # TODO: Print the score as "X/Y"
    # TODO: Print the percentage
    # TODO: Print a message based on percentage:
    #       90-100: "Excellent!"
    #       70-89:  "Good job!"
    #       50-69:  "Not bad!"
    #       0-49:   "Keep practicing!"
    pass


def play_again() -> bool:
    """
    Ask the user if they want to play again.
    
    Returns:
        True if user wants to play again, False otherwise
    """
    # TODO: Prompt user with "Play again? (y/n): "
    # TODO: Get input and convert to lowercase
    # TODO: Return True if input starts with 'y', False otherwise
    pass


def run_quiz() -> None:
    """
    Run the main quiz game loop.
    
    This function orchestrates the entire quiz flow:
    1. Load questions
    2. Display each question
    3. Get and check answers
    4. Track score
    5. Display final results
    """
    # TODO: Load questions using load_questions()
    
    # TODO: Initialize correct_count to 0
    
    # TODO: Get total number of questions
    
    # TODO: Loop through each question with enumerate
    #   - Display the question using display_question()
    #   - Get user's answer using get_user_answer()
    #   - Check if correct using check_answer()
    #   - If correct, increment correct_count
    #   - Print a blank line for readability
    
    # TODO: Calculate percentage using calculate_score()
    
    # TODO: Display results using display_results()
    pass


def main() -> None:
    """
    Main entry point for the quiz game.
    
    Displays welcome message and controls the game replay loop.
    """
    # TODO: Print welcome message with title formatting
    
    # TODO: Use a while loop to:
    #   - Run the quiz using run_quiz()
    #   - Ask to play again using play_again()
    #   - Continue if True, break if False
    
    # TODO: Print goodbye message
    pass


if __name__ == "__main__":
    main()
