# Python OOP Journey v2

A structured, week-by-week curriculum for mastering Python fundamentals and object-oriented programming through hands-on exercises, theory, and projects.

## Project Purpose

This repository provides a comprehensive learning path from Python basics to advanced OOP concepts. It's designed for:

- **Learners** working through Python and OOP systematically
- **Instructors** seeking a structured curriculum
- **Recruiters** reviewing portfolio projects
- **Developers** refreshing their OOP fundamentals

## Target Audience

- Beginners with basic programming knowledge looking to master Python
- Self-taught developers wanting structured OOP education
- Bootcamp students seeking supplementary material
- Professionals preparing for technical interviews

## Curriculum Overview

| Week | Topic | Focus |
|------|-------|-------|
| Week 0 | Getting Started | Python setup, fundamentals, file I/O, error handling, Todo CLI project |
| Week 1 | Python Fundamentals | Variables, strings, collections, control flow, functions |
| Week 2 | Advanced Fundamentals | File I/O, exceptions, modules/packages, comprehensions, functional programming, testing |
| Week 3 | OOP Basics | Classes, objects, methods, encapsulation, magic methods, composition (First OOP Week) |
| Week 4 | OOP Intermediate | Inheritance, overriding, ABCs, multiple inheritance, polymorphism, composition |
| Week 5 | Advanced OOP | Descriptors, metaclasses, decorators, dataclasses, iterators, reflection |
| Week 6 | Design Patterns | Creational, structural, and behavioral patterns, Game Framework |
| Week 7 | Real-World OOP | API design, testing, refactoring, services, Personal Finance Tracker |
| Week 8 | Capstone | Library Management System - 151 tests, culmination of entire course |

## Repository Structure

```
python-oop-journey-v2/
├── README.md                   # This file
├── QUICKSTART.md               # Get started in 5 minutes
├── INDEX.md                    # Navigation hub
├── ROADMAP.md                  # Current status and what's ahead
├── week00_getting_started/     # Week 0: Python basics for beginners (31 days)
├── week01_fundamentals/        # Week 1: Python basics
├── week02_fundamentals_advanced/  # Week 2: Advanced fundamentals
├── week03_oop_basics/     # Week 3: OOP foundations
├── week04_oop_intermediate/       # Week 4: Inheritance & polymorphism
├── week05_oop_advanced/   # Week 5: Advanced OOP features
├── week06_patterns/       # Week 6: Design patterns
├── week07_real_world/     # Week 7: Practical OOP
├── week08_capstone/       # Week 8: Library Management System
└── resources/             # Cheatsheets and reference materials
```

Each week contains:
- **Theory docs** (`dayNN_*.md` - Week 0 has 31 days, Weeks 1-8 have 6 days each)
- **Exercises** (`exercises/dayNN/problem_*.py`)
- **Solutions** (`solutions/dayNN/problem_*.py`)
- **Tests** (`tests/dayNN/test_problem_*.py`)
- **Weekly project** (`project/`)

**Note:** Week 0 (`week00_getting_started/`) is designed for absolute beginners with 31 days of content, including special File I/O days (20-23) with their own subdirectories.

## Setup Instructions

1. **Clone or navigate to this repository:**
   ```bash
   cd python-oop-journey-v2
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # For development (includes pytest, black, ruff, mypy):
   pip install -e ".[dev]"
   ```

## Test Instructions

Run all tests from the repository root:

```bash
pytest
```

Run tests for a specific week:

```bash
pytest week01_fundamentals/tests/
```

Run tests with coverage:

```bash
pytest --cov=week01_fundamentals
```

## Current Status

| Week | Status |
|------|--------|
| Week 0 | ✅ Complete - 135+ problems, 799 tests, Todo CLI |
| Week 1 | ✅ Complete - 63 problems, CLI Quiz Game |
| Week 2 | ✅ Complete - 54 problems, Procedural Library System |
| Week 3 | ✅ Complete - 52 problems, Basic E-commerce System |
| Week 4 | ✅ Complete - 38 problems, Animal Shelter |
| Week 5 | ✅ Complete - 51 problems, Task Management System |
| Week 6 | ✅ Complete - 39 problems, Game Framework |
| Week 7 | ✅ Complete - 30 problems, Personal Finance Tracker |
| Week 8 | ✅ Complete - Capstone, Library Management System |

**Total: 6,753+ tests passing** 🎉

## How to Use This Repository

### For Learning

1. Start with [QUICKSTART.md](QUICKSTART.md)
2. Work through weeks sequentially
3. Read the day's theory document first
4. Attempt exercises before looking at solutions
5. Run tests to verify your solutions
6. Complete the weekly project

### Exercises vs Solutions

- **Exercises** (`exercises/`) contain TODOs and `NotImplementedError` - this is where you write code
- **Solutions** (`solutions/`) contain reference implementations - check these when stuck
- **Tests** (`tests/`) validate solutions by default

The committed test suite validates reference solutions to keep the repository "green." When you want to test your own implementations, temporarily modify the imports in the test files.

See [ROADMAP.md](ROADMAP.md) for detailed status and upcoming milestones.

## Development Tools

This project uses:
- **pytest** for testing
- **black** for code formatting
- **ruff** for linting
- **mypy** for type checking

Format code:
```bash
black week01_fundamentals/
```

Lint code:
```bash
ruff check week01_fundamentals/
```

Type check:
```bash
mypy week01_fundamentals/
```

## License

MIT License - feel free to use for personal or educational purposes.

## Contributing

This is a personal learning curriculum. While suggestions are welcome, the structure follows a specific pedagogical progression designed for self-study.
