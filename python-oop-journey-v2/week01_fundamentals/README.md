# Week 1: Python Fundamentals

Build confidence with Python syntax, data types, collections, control flow, and functions before entering OOP.

## Week Objective

By the end of this week, you will:
- Master Python's basic data types and operations
- Work effectively with strings, lists, tuples, dictionaries, and sets
- Control program flow with conditionals and loops
- Write and use functions including recursive solutions
- Build a complete command-line application

## Prerequisites

- Python 3.10 or higher installed
- Basic understanding of programming concepts (variables, functions)
- Completion of repository setup (see root README.md)

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Variables, Data Types, Arithmetic | 11 | Easy-Medium |
| Day 2 | Strings | 11 | Easy-Hard |
| Day 3 | Lists and Tuples | 11 | Medium-Hard |
| Day 4 | Dictionaries and Sets | 10 | Medium |
| Day 5 | Control Flow | 10 | Medium |
| Day 6 | Functions and Recursion | 10 | Medium-Hard |

## File Structure

```
week01_fundamentals/
├── README.md                    # This file
├── day01_variables_types.md     # Day 1 theory
├── day02_strings.md             # Day 2 theory
├── day03_lists_tuples.md        # Day 3 theory
├── day04_dicts_sets.md          # Day 4 theory
├── day05_control_flow.md        # Day 5 theory
├── day06_functions.md           # Day 6 theory
├── exercises/                   # Your working area
│   ├── day01/                   # Day 1 exercises (11 files)
│   ├── day02/                   # Day 2 exercises (11 files)
│   ├── day03/                   # Day 3 exercises (11 files)
│   ├── day04/                   # Day 4 exercises (10 files)
│   ├── day05/                   # Day 5 exercises (10 files)
│   └── day06/                   # Day 6 exercises (10 files)
├── solutions/                   # Reference solutions
│   ├── day01/                   # Day 1 solutions
│   ├── day02/                   # Day 2 solutions
│   ├── day03/                   # Day 3 solutions
│   ├── day04/                   # Day 4 solutions
│   ├── day05/                   # Day 5 solutions
│   └── day06/                   # Day 6 solutions
├── tests/                       # Test suite
│   ├── day01/                   # Day 1 tests (81 tests)
│   ├── day02/                   # Day 2 tests (110 tests)
│   ├── day03/                   # Day 3 tests (116 tests)
│   ├── day04/                   # Day 4 tests (83 tests)
│   ├── day05/                   # Day 5 tests (55 tests)
│   └── day06/                   # Day 6 tests (68 tests)
└── project/                     # Weekly project
    ├── README.md                # Project documentation
    ├── starter/                 # Starter code
    ├── reference_solution/      # Complete solution
    └── tests/                   # Project tests (37 tests)
```

## How to Work Through This Week

### Daily Workflow

1. **Read the theory** document for the day (15-20 minutes)
   - Read through the concepts
   - Run the example code
   - Understand the common mistakes

2. **Attempt exercises** in order of difficulty:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-06: Core practice
   - Problems 07-08: Harder application
   - Problems 09-11: Stretch/bonus

3. **Check solutions** only when stuck:
   - Try to solve each problem yourself first
   - If stuck for 10+ minutes, peek at the solution
   - Understand the solution, then try to implement yourself

4. **Run tests** to verify your work:
   ```bash
   # Test specific problem
   pytest week01_fundamentals/tests/day01/test_problem_01_calculate_sum.py -v
   
   # Test all problems for a day
   pytest week01_fundamentals/tests/day01/ -v
   ```

### Recommended Pace

- **Intensive**: 1 day per calendar day (6 days)
- **Standard**: 2-3 days per week content (2-3 weeks)
- **Deep dive**: Take extra time on challenging problems

## Weekly Project: CLI Quiz Game

After completing the daily exercises, build a command-line quiz game that demonstrates:
- Input/output handling
- Function decomposition
- Control flow (loops, conditionals)
- Data structures (lists, dictionaries)

See [project/README.md](project/README.md) for full requirements.

### Project Structure

```
project/
├── README.md                    # Project requirements
├── starter/quiz_game.py         # Skeleton code with TODOs
├── reference_solution/quiz_game.py  # Complete implementation
└── tests/test_quiz_game.py      # 37 tests
```

## Running Tests

### All Week 1 Tests
```bash
pytest week01_fundamentals/tests/ -v
```

### Specific Day
```bash
pytest week01_fundamentals/tests/day01/ -v
```

### Specific Problem
```bash
pytest week01_fundamentals/tests/day01/test_problem_01_calculate_sum.py -v
```

### With Coverage
```bash
pytest week01_fundamentals/tests/ --cov=week01_fundamentals
```

## Key Concepts by Day

### Day 1: Variables & Types
- Variable naming and conventions
- Numeric types: `int`, `float`
- Text type: `str`
- Boolean type: `bool`
- None type: `NoneType`
- Type conversion: `int()`, `float()`, `str()`
- Tuple unpacking

### Day 2: Strings
- String creation and indexing
- Slicing syntax
- Common methods: `split()`, `join()`, `strip()`, `replace()`
- String formatting: f-strings
- Immutability

### Day 3: Lists & Tuples
- List creation and indexing
- List methods: `append()`, `extend()`, `insert()`, `remove()`, `pop()`
- List comprehensions
- Tuple basics and immutability
- Two-pointer techniques

### Day 4: Dicts & Sets
- Dictionary creation and access
- Dictionary methods: `keys()`, `values()`, `items()`, `get()`
- Set creation and operations
- Set methods: `add()`, `remove()`, `union()`, `intersection()`
- Hash-based lookups

### Day 5: Control Flow
- `if/elif/else` statements
- `for` loops and `range()`
- `while` loops
- `break`, `continue`, `pass`
- Nested loops
- `enumerate()` and `zip()`

### Day 6: Functions & Recursion
- Defining functions with `def`
- Parameters and arguments
- Return values
- Recursion basics
- Base case and recursive case
- Backtracking patterns

## Tips for Success

1. **Type out code** - Don't copy-paste solutions
2. **Experiment** - Modify working code to see what happens
3. **Use the REPL** - Test small snippets interactively
4. **Read errors carefully** - Python's error messages are helpful
5. **Take breaks** - Step away from difficult problems
6. **Review** - Go back to earlier exercises periodically

## Common Pitfalls

- **Off-by-one errors** with indices and ranges
- **Modifying collections while iterating** over them
- **Confusing `is` and `==`** for equality checking
- **Mutable default arguments** in functions
- **Infinite recursion** without proper base cases

## Next Week

Week 2 covers:
- File I/O and file processing
- Exception handling
- Modules and packages
- Comprehensions and generators
- Functional programming basics
- Testing with pytest

---

**Total Exercises**: 63 problems  
**Total Tests**: 513 tests (including project)  
**Estimated Time**: 6-20 hours depending on pace
