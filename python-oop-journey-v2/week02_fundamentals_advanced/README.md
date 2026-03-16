# Week 2: Advanced Fundamentals

Move from basic syntax into file handling, modules, functional patterns, and testing.

## Week Objective

By the end of this week, you will:
- Read from and write to files in various formats
- Handle errors gracefully using exceptions
- Organize code into modules and packages
- Use comprehensions and generators effectively
- Apply functional programming patterns
- Write tests with pytest

## Prerequisites

- Completion of Week 1: Python Fundamentals
- Understanding of basic Python syntax
- Familiarity with functions and control flow

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | File I/O and File Processing | 11 | Easy-Medium |
| Day 2 | Exceptions and Defensive Programming | 10 | Medium |
| Day 3 | Modules and Packages | 8 | Medium |
| Day 4 | Comprehensions and Generators | 10 | Medium |
| Day 5 | Functional Programming Basics | 8 | Medium |
| Day 6 | Testing with pytest | 7 | Medium |

## File Structure

```
week02_fundamentals_advanced/
├── README.md                    # This file
├── day01_file_io.md             # Day 1 theory
├── day02_exceptions.md          # Day 2 theory
├── day03_modules_packages.md    # Day 3 theory
├── day04_comprehensions_generators.md  # Day 4 theory
├── day05_functional_programming.md     # Day 5 theory
├── day06_testing_with_pytest.md        # Day 6 theory
├── exercises/                   # Your working area
│   ├── day01/                   # Day 1 exercises (11 files)
│   ├── day02/                   # Day 2 exercises (10 files)
│   ├── day03/                   # Day 3 exercises (8 files)
│   ├── day04/                   # Day 4 exercises (10 files)
│   ├── day05/                   # Day 5 exercises (8 files)
│   └── day06/                   # Day 6 exercises (7 files)
├── solutions/                   # Reference solutions
│   ├── day01/                   # Day 1 solutions
│   ├── day02/                   # Day 2 solutions
│   ├── day03/                   # Day 3 solutions
│   ├── day04/                   # Day 4 solutions
│   ├── day05/                   # Day 5 solutions
│   └── day06/                   # Day 6 solutions
├── tests/                       # Test suite
│   ├── day01/                   # Day 1 tests
│   ├── day02/                   # Day 2 tests
│   ├── day03/                   # Day 3 tests
│   ├── day04/                   # Day 4 tests
│   ├── day05/                   # Day 5 tests
│   └── day06/                   # Day 6 tests
└── project/                     # Weekly project
    ├── README.md                # Project documentation
    ├── starter/                 # Starter code
    ├── reference_solution/      # Complete solution
    └── tests/                   # Project tests
```

## 🚀 START HERE

New to this week? Begin with **Day 1 theory**:
1. Open [`day01_file_io.md`](day01_file_io.md) - read the theory (15-20 minutes)
2. Attempt [`exercises/day01/problem_01_count_lines.py`](exercises/day01/problem_01_count_lines.py)
3. Run tests: `pytest week02_fundamentals_advanced/tests/day01/test_problem_01_count_lines.py -v`
4. Check your solution against [`solutions/day01/problem_01_count_lines.py`](solutions/day01/problem_01_count_lines.py) when stuck

---

## How to Work Through This Week

### Daily Workflow

1. **Read the theory** document for the day (15-20 minutes)
2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-06: Core practice
   - Problems 07-08: Harder application
   - Problems 09-11: Stretch/bonus (if available)
3. **Check solutions** only when stuck
4. **Run tests** to verify your work

### Running Tests

```bash
# Test specific day
pytest week02_fundamentals_advanced/tests/day01/ -v

# Test specific problem
pytest week02_fundamentals_advanced/tests/day01/test_problem_01_count_lines.py -v

# Test all of Week 2
pytest week02_fundamentals_advanced/tests/ -v
```

## How to Check Your Work

### The Verification Path

Follow this learner verification workflow to check your understanding honestly:

1. **Read the theory doc** for the day
   - Understand the core concepts before attempting exercises
   - Work through the examples in the theory doc yourself

2. **Attempt the exercise honestly** without looking at solutions
   - Read the problem statement carefully
   - Identify the expected inputs and outputs
   - Think through your approach before coding

3. **Run the provided examples manually**
   - Test your solution with the examples in the docstring
   - Try additional test cases you invent yourself
   - Verify edge cases (empty inputs, single items, etc.)

4. **Read the matching reference test file** to understand expected behavior
   - Tests are located in `tests/dayXX/test_problem_XX_*.py`
   - Tests show you exactly what behavior is expected
   - Tests clarify edge cases not obvious from the exercise

5. **Compare against the reference solution only after a real attempt**
   - Solutions are in `solutions/dayXX/problem_XX_*.py`
   - Study the solution to understand the approach
   - Ask yourself: "Why did they do it this way?"

### Understanding Test Results

```bash
# Run tests with detailed output
pytest week02_fundamentals_advanced/tests/day01/ -v

# A passing test shows:
# tests/day01/test_problem_01_count_lines.py::test_count_lines_normal_file PASSED

# A failing test shows:
# tests/day01/test_problem_01_count_lines.py::test_count_lines_empty_file FAILED
# AssertionError: assert 0 == -1  (your output vs expected)
```

### When You Get Stuck

**For Medium/Hard exercises**, hints are provided in the exercise file comments.

**Common Week 2 Debugging Tips:**

| Issue | What to Check |
|-------|---------------|
| File operations fail | Are you using `with open()` for proper cleanup? |
| Exception not caught | Is your `except` block catching the right exception type? |
| Import errors | Check your relative vs absolute imports |
| Generator produces nothing | Did you iterate the generator or just create it? |
| Lambda gives wrong result | Check variable scope - lambdas capture variables, not values |
| Dictionary comprehension fails | Are keys unique? Duplicates overwrite silently |
| Context manager crashes | Ensure `__exit__` handles exceptions properly |
| Iterator exhausted early | Generators can only be consumed once - recreate if needed |

## How to Check Your Work

### Quick Verification (as you work)
```bash
# Test the problem you just solved
pytest week02_fundamentals_advanced/tests/day01/test_problem_01_count_lines.py -v

# Test all problems for a day
pytest week02_fundamentals_advanced/tests/day01/ -v
```

### Recommended Verification Path
1. **Read** the theory doc for the day
2. **Attempt** the exercise without looking at solutions
3. **Run** the small examples in the exercise file manually
4. **Read** the test file to understand expected behavior
5. **Compare** with reference solution only after a real attempt

### Full Week Verification
```bash
# Test all of Week 2
pytest week02_fundamentals_advanced/tests/ -v

# Run project tests
pytest week02_fundamentals_advanced/project/tests/ -v
```

**Green tests = Your solution is correct!**

---

## Weekly Project: Procedural Library System

Build a library management system using procedural programming:
- File-based book storage
- Exception handling for invalid operations
- Modular code organization
- Comprehensive test suite

See [project/README.md](project/README.md) for full requirements.

**When to start the project**: Complete Days 1-4 before beginning the project. The project reinforces file I/O (Day 1), exceptions (Day 2), modules (Day 3), and comprehensions (Day 4).

## Key Concepts by Day

### Day 1: File I/O
- Opening files with `open()`
- Context managers (`with` statement)
- Reading modes: `read()`, `readline()`, `readlines()`
- Writing modes: `write()`, `writelines()`
- CSV and JSON handling
- File paths with `pathlib`

### Day 2: Exceptions
- `try/except/else/finally` blocks
- Built-in exception types
- Custom exception classes
- Exception chaining
- Defensive programming patterns
- EAFP vs LBYL philosophies

### Day 3: Modules & Packages
- Module imports and `__name__ == "__main__"`
- Relative vs absolute imports
- Package structure with `__init__.py`
- `sys.path` and PYTHONPATH
- Creating installable packages

### Day 4: Comprehensions & Generators
- List, dict, and set comprehensions
- Generator functions with `yield`
- Generator expressions
- `itertools` module
- Lazy evaluation
- Memory efficiency

### Day 5: Functional Programming
- Pure functions and side effects
- Higher-order functions
- `map()`, `filter()`, `reduce()`
- Lambda expressions
- `functools`: `partial`, `wraps`
- Closures and decorators

### Day 6: Testing with pytest
- Test functions and assertions
- Fixtures for setup/teardown
- Parametrized tests
- Mocking with `unittest.mock`
- Test coverage
- TDD workflow

## Tips for Success

1. **Practice file operations** - They're essential for real-world Python
2. **Master exception handling** - Don't let errors crash your programs
3. **Embrace generators** - They're memory-efficient and Pythonic
4. **Write tests early** - They save debugging time
5. **Think modular** - Break code into reusable components

## Common Pitfalls

- **Resource leaks** - Always use `with` for file operations
- **Bare except clauses** - Catch specific exceptions
- **Circular imports** - Watch your module dependencies
- **Mutable default arguments** - Classic Python gotcha
- **Overusing lambdas** - Named functions are clearer for complex logic

## Next Week

Week 3 introduces Object-Oriented Programming:
- Classes and objects
- Instance, class, and static methods
- Encapsulation and properties
- Magic methods
- Composition and aggregation

---

**Total Exercises**: 54 problems  
**Estimated Time**: 6-18 hours depending on pace
