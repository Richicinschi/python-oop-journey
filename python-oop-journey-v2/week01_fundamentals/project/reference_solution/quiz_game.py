"""
Week 1 Project: CLI Quiz Game - Reference Solution

This module implements a complete command-line quiz game.
Use this as a reference for how the starter code should be completed.

Learning objectives demonstrated:
- Function design and organization
- Working with lists and dictionaries
- User input/output handling
- Control flow with loops and conditionals
- Defensive programming with input validation
"""

from typing import List, Dict, Any, Tuple


# Quiz questions data structure
# Using tuples for questions to make them immutable
Question = Dict[str, Any]

QUESTIONS: Tuple[Question, ...] = (
    {
        "question": "What is the capital of France?",
        "options": ("London", "Berlin", "Paris", "Madrid"),
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ("Venus", "Mars", "Jupiter", "Saturn"),
        "answer": "B"
    },
    {
        "question": "What is 2 + 2 * 2?",
        "options": ("6", "8", "4", "10"),
        "answer": "A"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ("Van Gogh", "Picasso", "Da Vinci", "Rembrandt"),
        "answer": "C"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ("Atlantic", "Indian", "Arctic", "Pacific"),
        "answer": "D"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ("Go", "Gd", "Au", "Ag"),
        "answer": "C"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ("5", "6", "7", "8"),
        "answer": "C"
    }
)

# Answer option letters
OPTION_LETTERS = ("A", "B", "C", "D")


def load_questions() -> Tuple[Question, ...]:
    """
    Load and return the quiz questions.
    
    Returns:
        A tuple of question dictionaries, each containing:
        - 'question': str, the question text
        - 'options': tuple of str, the answer choices
        - 'answer': str, the correct answer letter (A, B, C, or D)
    """
    return QUESTIONS


def display_question(question: Question, question_num: int, total: int) -> None:
    """
    Display a single quiz question with its options.
    
    Args:
        question: Dictionary containing question data
        question_num: Current question number (1-indexed)
        total: Total number of questions
    """
    print(f"\nQuestion {question_num} of {total}:")
    print("-" * 40)
    print(question["question"])
    print()
    
    for letter, option in zip(OPTION_LETTERS, question["options"]):
        print(f"  {letter}) {option}")


def get_user_answer() -> str:
    """
    Get and validate the user's answer.
    
    Prompts the user until they enter a valid answer (A, B, C, or D).
    Converts input to uppercase for case-insensitive comparison.
    
    Returns:
        The user's answer as a single uppercase letter (A-D)
    """
    valid_answers = set(OPTION_LETTERS)
    
    while True:
        user_input = input("\nYour answer: ").strip().upper()
        
        if user_input in valid_answers:
            return user_input
        
        print(f"Invalid input. Please enter one of: {', '.join(OPTION_LETTERS)}")


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """
    Check if the user's answer is correct.
    
    Performs case-insensitive comparison and provides feedback.
    
    Args:
        user_answer: The answer provided by the user (A-D)
        correct_answer: The correct answer (A-D)
    
    Returns:
        True if answers match, False otherwise
    """
    is_correct = user_answer.upper() == correct_answer.upper()
    
    if is_correct:
        print("✓ Correct!")
    else:
        print(f"✗ Wrong! The correct answer was {correct_answer}.")
    
    return is_correct


def calculate_score(correct_count: int, total: int) -> float:
    """
    Calculate the percentage score.
    
    Handles edge case where total is 0 to avoid division by zero.
    
    Args:
        correct_count: Number of correct answers
        total: Total number of questions
    
    Returns:
        Percentage score (0.0 - 100.0), or 0.0 if total is 0
    """
    if total == 0:
        return 0.0
    
    return (correct_count / total) * 100


def get_performance_message(percentage: float) -> str:
    """
    Get a performance message based on the percentage score.
    
    Args:
        percentage: The percentage score (0.0 - 100.0)
    
    Returns:
        An encouraging message based on performance
    """
    if percentage >= 90:
        return "Excellent work! You're a quiz master!"
    elif percentage >= 70:
        return "Good job! You know your stuff!"
    elif percentage >= 50:
        return "Not bad! Room for improvement."
    else:
        return "Keep practicing! You'll get better!"


def display_results(score: int, total: int, percentage: float) -> None:
    """
    Display the final quiz results with formatting.
    
    Args:
        score: Number of correct answers
        total: Total number of questions
        percentage: Percentage score (0.0 - 100.0)
    """
    print("\n" + "=" * 40)
    print("           FINAL RESULTS")
    print("=" * 40)
    print(f"Your Score: {score}/{total}")
    print(f"Percentage: {percentage:.1f}%")
    print()
    print(get_performance_message(percentage))
    print("=" * 40)


def play_again() -> bool:
    """
    Ask the user if they want to play again.
    
    Accepts 'y', 'Y', 'yes', 'YES' as affirmative responses.
    Any other input is treated as a negative response.
    
    Returns:
        True if user wants to play again, False otherwise
    """
    print()
    user_input = input("Play again? (y/n): ").strip().lower()
    return user_input.startswith("y")


def run_quiz() -> None:
    """
    Run the main quiz game loop.
    
    Orchestrates the entire quiz flow from loading questions
    to displaying final results.
    """
    questions = load_questions()
    
    if not questions:
        print("No questions available!")
        return
    
    correct_count = 0
    total = len(questions)
    
    for idx, question in enumerate(questions, start=1):
        display_question(question, idx, total)
        user_answer = get_user_answer()
        
        if check_answer(user_answer, question["answer"]):
            correct_count += 1
    
    percentage = calculate_score(correct_count, total)
    display_results(correct_count, total, percentage)


def display_welcome() -> None:
    """Display the welcome banner."""
    print("=" * 40)
    print("     Welcome to CLI Quiz Game!")
    print("=" * 40)
    print("\nTest your knowledge with multiple choice questions.")
    print("Answer by typing A, B, C, or D.\n")


def display_goodbye() -> None:
    """Display the goodbye message."""
    print("\n" + "=" * 40)
    print("  Thanks for playing! Goodbye!")
    print("=" * 40)


def main() -> None:
    """
    Main entry point for the quiz game.
    
    Controls the game replay loop and handles top-level flow.
    """
    display_welcome()
    
    while True:
        run_quiz()
        
        if not play_again():
            break
        
        print("\n" + "-" * 40)
        print("Starting a new game...\n")
    
    display_goodbye()


if __name__ == "__main__":
    main()
