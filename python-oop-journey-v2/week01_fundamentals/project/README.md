# Week 1 Project: CLI Quiz Game

A command-line quiz game built with Python fundamentals. This project reinforces concepts learned throughout Week 1: variables, functions, control flow, and data structures.

---

## Project Overview

Build an interactive quiz game that runs in the terminal. Players answer multiple-choice questions, earn points for correct answers, and can play multiple rounds. This project demonstrates how to structure a simple Python application using functions and basic data structures.

---

## Learning Goals

By completing this project, you will:

- **Master basic I/O operations**: Reading user input and displaying formatted output
- **Practice function design**: Breaking problems into small, testable functions
- **Apply control flow**: Using loops, conditionals, and logical operators
- **Work with data structures**: Storing and manipulating data using lists and dictionaries
- **Write testable code**: Creating functions that can be unit tested
- **Structure a simple project**: Organizing code into logical components

---

## Required Features

Your quiz game must implement:

### Core Functionality
1. **Question Loading**: Load a set of quiz questions from a data structure (list of dictionaries)
2. **Question Display**: Show each question with numbered multiple-choice options
3. **Answer Input**: Accept and validate user input (A, B, C, or D)
4. **Answer Checking**: Compare user answer against correct answer
5. **Score Tracking**: Keep running total of correct answers
6. **Results Display**: Show final score and percentage after all questions
7. **Play Again**: Ask if user wants to play another round

### Code Organization
- Each major operation in its own function
- Clear separation between data (questions) and logic
- Input validation to handle unexpected user input
- Docstrings for all functions
- Type hints for function parameters and return values

---

## Optional Stretch Features

Once you have the core working, consider adding:

### Difficulty Levels
- Easy, Medium, Hard question sets
- Different scoring multipliers per difficulty
- Player selects difficulty at game start

### Timer
- Countdown timer for each question
- Bonus points for fast answers
- Time limit enforced

### High Score Tracking
- Save best scores to a file
- Display leaderboard at game start
- Track player names with scores

### Question Categories
- Organize questions by topic (Science, History, Geography, etc.)
- Let players choose category
- Mix questions from multiple categories

### Enhanced UX
- Color-coded feedback (green for correct, red for wrong)
- Progress indicator ("Question 3 of 10")
- ASCII art title screen
- Sound effects (platform-dependent)

---

## Project Structure

```
week01_fundamentals/project/
├── README.md                           # This file
├── starter/
│   └── quiz_game.py                    # Skeleton code with TODOs
├── reference_solution/
│   └── quiz_game.py                    # Complete working implementation
└── tests/
    └── test_quiz_game.py               # Unit tests for quiz functions
```

---

## How Starter Code Is Organized

The starter file (`starter/quiz_game.py`) provides:

1. **Data Structure Template**: A sample `QUESTIONS` list showing the expected format
2. **Function Skeletons**: All required functions defined with `pass` and TODO comments
3. **Main Function**: Entry point with basic game loop outline
4. **Type Hints**: Function signatures include expected types
5. **Docstrings**: Each function has a description of what it should do

### Functions to Implement

| Function | Purpose |
|----------|---------|
| `load_questions()` | Returns the list of question dictionaries |
| `display_question(question, question_num, total)` | Shows question and options formatted |
| `get_user_answer()` | Gets and validates A/B/C/D input from user |
| `check_answer(user_answer, correct_answer)` | Returns True if answers match |
| `calculate_score(correct_count, total)` | Returns percentage score |
| `display_results(score, total, percentage)` | Shows final score summary |
| `play_again()` | Asks and returns True if user wants to replay |
| `run_quiz()` | Main game loop orchestrating all functions |
| `main()` | Entry point with welcome message |

---

## How Reference Solution Is Organized

The reference solution (`reference_solution/quiz_game.py`) demonstrates:

1. **Clean Function Design**: Each function does one thing well
2. **Defensive Programming**: Input validation and error handling
3. **Consistent Naming**: Clear, descriptive variable and function names
4. **Modular Structure**: Easy to extend or modify individual parts
5. **Pythonic Patterns**: List comprehensions, f-strings, etc.

### Key Design Decisions

- **Immutable Question Data**: Questions stored as tuples inside the list to prevent accidental modification
- **Case-Insensitive Answers**: Both 'a' and 'A' accepted as valid
- **Clear Visual Separation**: Blank lines and formatting for readability
- **Graceful Degradation**: Handles empty question lists and edge cases

---

## How to Run Tests

### Run All Project Tests

From the repository root:

```bash
# Run all tests for the quiz game
pytest week01_fundamentals/project/tests/ -v
```

### Run Individual Test Files

```bash
# Test only the quiz game
pytest week01_fundamentals/project/tests/test_quiz_game.py -v
```

### Run Specific Tests

```bash
# Test a specific function
pytest week01_fundamentals/project/tests/test_quiz_game.py::test_load_questions -v

# Test with more detail
pytest week01_fundamentals/project/tests/test_quiz_game.py -v --tb=short
```

### Test Against Your Solution

To test your implementation:

1. Copy your `quiz_game.py` to the tests directory (or adjust imports)
2. Run pytest
3. All tests should pass for a complete implementation

### Test Coverage

The test suite covers:

- **Data loading**: Verifies questions load correctly
- **Answer validation**: Tests correct/incorrect answer detection
- **Score calculation**: Verifies percentage math
- **Input handling**: Mocks user input for testing game flow
- **Edge cases**: Empty questions, invalid input handling

---

## Running the Game

### Run the Starter Version

```bash
# Navigate to project directory
cd week01_fundamentals/project/starter

# Run the skeleton (will need implementation)
python quiz_game.py
```

### Run the Reference Solution

```bash
# Navigate to reference solution
cd week01_fundamentals/project/reference_solution

# Run the complete game
python quiz_game.py
```

---

## Expected Game Flow

```
================================
     Welcome to Quiz Game!
================================

Question 1 of 5:
--------------------
What is the capital of France?
  A) London
  B) Berlin
  C) Paris
  D) Madrid

Your answer: C
✓ Correct!

Question 2 of 5:
...

================================
           RESULTS
================================
Your Score: 4/5
Percentage: 80.0%
Great job!

Play again? (y/n): n
Thanks for playing!
```

---

## Tips for Success

1. **Start with data**: Define your questions list first
2. **Implement one function at a time**: Test each as you go
3. **Use the REPL**: Try functions interactively
4. **Handle edge cases**: What if input is 'e' or empty?
5. **Keep it simple**: Get core working before stretch features
6. **Read the tests**: They show expected behavior

---

## Common Pitfalls

- **Forgetting to return**: Functions that should return values but don't
- **String comparison issues**: Not normalizing case ('A' vs 'a')
- **Input validation loops**: Not handling invalid input properly
- **Global state**: Relying on global variables instead of parameters
- **Off-by-one errors**: Question numbering starting at 0 vs 1

---

## Submission Checklist

Before moving to Week 2, ensure:

- [ ] All required functions implemented
- [ ] Game runs without errors
- [ ] All tests pass
- [ ] Code has docstrings and type hints
- [ ] Play again functionality works
- [ ] Input validation handles edge cases

---

## Further Exploration

Ideas to extend this project:

1. Load questions from a JSON file instead of hardcoded list
2. Add true/false questions alongside multiple choice
3. Implement a hint system (costs points)
4. Add multiple player support (hot-seat mode)
5. Create a GUI version using tkinter (Week 5+ concept)

---

**Good luck and have fun building your quiz game!**
