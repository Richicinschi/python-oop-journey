# Week 00: Getting Started with Python

Welcome to Python OOP Journey! This week covers the absolute basics of Python programming for complete beginners.

## Learning Path Overview

This week takes you from zero programming experience to being comfortable with Python fundamentals. Each day builds on the previous, creating a solid foundation for Object-Oriented Programming.

## Daily Topics

### Foundation Phase (Days 00-07)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **00** | Welcome and Overview | What is programming, course roadmap |
| **01** | Installing Python | Python versions, installation, verification |
| **02** | Environment Setup | VS Code, terminal, virtual environments |
| **03** | First Program | `print()`, comments, running Python files |
| **04** | Variables and Assignment | Variable naming, assignment, unpacking |
| **05** | Basic Data Types | `int`, `float`, `str`, `bool`, type conversion |
| **06** | Simple Input/Output | `input()`, `print()`, f-strings, formatting |
| **07** | Basic Operators | Arithmetic, comparison, logical operators |

### Control Flow Phase (Days 08-11)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **08** | Boolean Logic | `True`/`False`, comparisons, logical operators |
| **09** | If Statements | `if`, `elif`, `else`, nested conditions |
| **10** | While Loops | `while`, `break`, `continue`, infinite loops |
| **11** | For Loops | `for`, `range()`, iterating over sequences |

### Data Structures Phase (Days 12-15)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **12** | Lists | Creating, indexing, slicing, methods |
| **13** | Tuples | Immutable sequences, packing/unpacking |
| **14** | Dictionaries | Key-value pairs, methods, iteration |
| **15** | Sets | Unordered collections, set operations |

### Functions Phase (Days 16-19)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **16** | Defining Functions | `def`, parameters, return values |
| **17** | Function Parameters | Default args, `*args`, `**kwargs` |
| **18** | Variable Scope | Local, global, `global`, `nonlocal` |
| **19** | Built-in Functions | Common utilities, `map()`, `filter()`, `zip()` |

### File I/O Phase (Days 20-23)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **20** | Reading Files | `open()`, reading modes, line iteration |
| **21** | Writing Files | Write modes, `with` statement, file paths |
| **22** | File Paths | `pathlib`, `os.path`, absolute vs relative |
| **23** | Working with CSV | `csv` module, reading/writing CSV data |

### Error Handling Phase (Days 24-27)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **24** | Understanding Errors | Syntax vs runtime, error types, stack traces |
| **25** | Try/Except | Exception handling, `try`/`except`/`finally` |
| **26** | Common Exceptions | `ValueError`, `TypeError`, `KeyError`, etc. |
| **27** | Debugging Basics | `print()` debugging, common mistakes |

### Modules & Practice Phase (Days 28-30)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **28** | Modules and Imports | `import`, `from`, creating modules, `__name__` |
| **29** | Review and Practice | Comprehensive exercises, mini-challenges |
| **30** | Final Project | **Todo List CLI Application** |

---

## How to Check Your Work

This section answers: **"How do I know my solution is right?"**

### The Recommended Verification Path

Follow this sequence for each exercise to maximize learning:

1. **Read the theory doc** for the day
   - Understand the concepts before attempting problems
   - Review the examples and common mistakes sections

2. **Attempt the exercise honestly**
   - Try to solve it on your own first
   - Don't look at the solution or tests yet
   - Write your best attempt even if incomplete

3. **Run the provided examples manually**
   - Open a Python interpreter or create a test script
   - Test your function with the example inputs from the docstring
   - Verify the output matches what the docstring shows

4. **Read the matching reference tests**
   - Tests are located in `tests/dayXX/test_problem_XX_name.py`
   - Reading tests helps you understand the expected behavior
   - Look for edge cases you might have missed

5. **Compare to reference solution only after a real attempt**
   - Solutions are in `solutions/dayXX/problem_XX_name.py`
   - Compare your approach to the reference
   - Understand why the solution works

### Running Tests

To run all Week 00 tests:

```bash
pytest week00_getting_started/tests/
pytest week00_getting_started/day20_reading_files/tests/
pytest week00_getting_started/day21_writing_files/tests/
pytest week00_getting_started/day22_file_paths/tests/
pytest week00_getting_started/day23_working_with_csv/tests/
pytest week00_getting_started/day03_tests/
pytest week00_getting_started/project/tests/
pytest week00_getting_started/project/tests/
```

To run tests for a specific day:

```bash
# Standard days
pytest week00_getting_started/tests/day04/

# Special structure days
pytest week00_getting_started/day20_reading_files/tests/
```

To run a specific test file:

```bash
pytest week00_getting_started/tests/day04/test_problem_01_assign_and_print.py -v
```

### What If My Solution Fails Tests?

1. **Read the test failure message carefully**
   - It shows what input was used
   - It shows what your function returned
   - It shows what was expected

2. **Use print debugging**
   - Add `print()` statements to see intermediate values
   - Check variable types with `type(variable)`
   - Trace through your logic step by step

3. **Check the hints in the exercise file**
   - Medium and hard exercises include hint comments
   - Look for the "HINTS" section in the docstring

4. **Review the day theory doc**
   - Re-read the relevant concept section
   - Look at the common mistakes section

### Test Coverage Philosophy

Tests in this course serve two purposes:
1. **Verification**: Confirm your solution works correctly
2. **Documentation**: Show expected behavior through examples

Reading the test files is encouraged—they often demonstrate edge cases and invalid inputs you should handle.

---

## File Organization

```
week00_getting_started/
├── README.md                           # This file
├── day00_welcome.md                    # Day 0: Course overview
├── day01_installing_python.md          # Day 1: Installation
├── day02_environment_setup.md          # Day 2: Environment
├── day03_first_program.md              # Day 3: First program
├── day04_variables.md                  # Day 4: Variables
├── day05_basic_types.md                # Day 5: Data types
├── day06_input_output.md               # Day 6: I/O
├── day07_operators.md                  # Day 7: Operators
├── day08_boolean_logic.md              # Day 8: Booleans
├── day09_if_statements.md              # Day 9: If statements
├── day10_while_loops.md                # Day 10: While loops
├── day11_for_loops.md                  # Day 11: For loops
├── day12_lists_basics.md               # Day 12: Lists
├── day13_tuples_basics.md              # Day 13: Tuples
├── day14_dictionaries_basics.md        # Day 14: Dictionaries
├── day15_sets_basics.md                # Day 15: Sets
├── day16_defining_functions.md         # Day 16: Functions
├── day17_function_parameters.md        # Day 17: Parameters
├── day18_variable_scope.md             # Day 18: Scope
├── day19_builtin_functions.md          # Day 19: Built-ins
├── day20_reading_files/                # Day 20: Reading files (special structure)
│   ├── day20_reading_files.md
│   ├── solutions/
│   └── tests/
├── day21_writing_files/                # Day 21: Writing files (special structure)
│   ├── day21_writing_files.md
│   ├── solutions/
│   └── tests/
├── day22_file_paths/                   # Day 22: File paths (special structure)
│   ├── day22_file_paths.md
│   ├── solutions/
│   └── tests/
├── day23_working_with_csv/             # Day 23: CSV (special structure)
│   ├── day23_working_with_csv.md
│   ├── solutions/
│   └── tests/
├── day24_understanding_errors.md       # Day 24: Errors
├── day25_try_except.md                 # Day 25: Exceptions
├── day26_common_exceptions.md          # Day 26: Common errors
├── day27_debugging_basics.md           # Day 27: Debugging
├── day28_modules_and_imports.md        # Day 28: Modules
├── day29_review_and_practice.md        # Day 29: Review
├── day30_final_project.md              # Day 30: Project
├── exercises/                          # Exercises (Days 01-19, 24-29)
│   ├── day01/ through day19/
│   ├── day24/ through day29/
├── solutions/                          # Solutions (Days 01-19, 24-29)
│   ├── day01/ through day19/
│   ├── day24/ through day29/
├── tests/                              # Tests (Days 04-19, 24-29)
│   ├── day04/ through day19/
│   ├── day24/ through day29/
├── day01_exercises/                    # Day 1 exercises
├── day02_exercises/                    # Day 2 exercises
├── day03_exercises/                    # Day 3 exercises
├── day03_solutions/                    # Day 3 solutions
├── day03_tests/                        # Day 3 tests
├── project/                            # Final project (Todo CLI)
│   ├── README.md
│   ├── starter/
│   ├── reference_solution/
│   └── tests/
├── notebooks/                          # Jupyter notebooks (5)
└── cheatsheets/                        # Quick reference (6)
```

---

## Coding Standards

All exercises follow these standards:
- Type hints on all function signatures
- Docstrings with Args and Returns sections
- `from __future__ import annotations` at the top
- Valid Python module names: `problem_XX_snake_case.py`

---

## Weekly Project: Todo List CLI

Build a command-line todo list application that demonstrates:
- File persistence (JSON storage)
- CRUD operations (Create, Read, Update, Delete)
- Input validation and error handling
- Modular code organization

See `project/` directory for full requirements and starter code.

---

## Difficulty Levels

Exercises are marked with difficulty levels:

- **Easy**: Straightforward application of the day's concepts
- **Medium**: Requires combining multiple concepts or careful attention to edge cases
- **Hard**: Challenging problems that may require significant problem-solving

Medium and hard exercises include hints in their docstrings to help when you get stuck.

---

## Supplementary Materials

### Jupyter Notebooks (5)
Located in `notebooks/`:
1. `00_getting_started.ipynb` - Interactive Python introduction
2. `01_python_basics_walkthrough.ipynb` - Variables and data types
3. `02_control_flow_walkthrough.ipynb` - Conditionals and loops
4. `03_collections_walkthrough.ipynb` - Lists, dicts, sets
5. `04_functions_walkthrough.ipynb` - Function definitions

### Cheat Sheets (6)
Located in `cheatsheets/`:
1. `python_syntax_cheatsheet.md` - Core syntax
2. `data_types_cheatsheet.md` - Built-in types
3. `control_flow_cheatsheet.md` - If statements and loops
4. `functions_cheatsheet.md` - Function patterns
5. `common_errors_cheatsheet.md` - Exception handling
6. `vs_code_shortcuts.md` - VS Code shortcuts

---

**Total Days**: 31 (Days 00-30)  
**Total Exercises**: 135+ problems  
**Total Tests**: 787+ tests  
**Project**: 1 complete CLI application  
**Estimated Time**: 40-60 hours depending on pace
