# Week 2 Project: Procedural Library System

A command-line library management system built with procedural Python. This project reinforces file I/O, exception handling, modular organization, and testing.

## Learning Goals

After completing this project, you will be able to:

- **File I/O**: Read from and write to files for persistent data storage
- **Exception Handling**: Define and raise custom exceptions for domain errors
- **Modular Design**: Organize code into focused modules with clear responsibilities
- **Data Structures**: Use dictionaries and lists to manage collections
- **Testing**: Write comprehensive tests using pytest, including fixtures and temp files

## Project Overview

Build a library system that manages books with persistent storage. The system operates through a functional API—no classes required. This keeps the focus on:

- Pure functions that transform data
- Error handling through exceptions
- File-based persistence
- Module separation of concerns

## Quick Start

**New to this project?** Start here:

1. **Understand the goal**: Read "Learning Goals" and "Project Overview" above
2. **See the contract**: Review "Required Features" and "Public API" sections below
3. **Start coding**: Open `starter/exceptions.py` and complete the TODOs in this order:
   - `exceptions.py` → `book.py` → `storage.py` → `library.py`
4. **Test as you go**: Run `pytest week02_fundamentals_advanced/project/tests/ -v`
5. **Check reference**: Compare with `reference_solution/` when stuck

## Required Features

### Book Management

- `add_book(library, title, author, isbn) -> dict`: Add a new book to the library
- `find_book(library, isbn) -> dict | None`: Find a book by its ISBN
- `search_books(library, query) -> list[dict]`: Search books by title or author (case-insensitive partial match)
- `list_all_books(library) -> list[dict]`: Return all books in the library

### Book Operations

- `checkout_book(library, isbn) -> dict`: Mark a book as checked out
- `return_book(library, isbn) -> dict`: Mark a checked-out book as available
- `is_book_available(library, isbn) -> bool`: Check if a book can be checked out

### Data Persistence

- `save_library(library, filepath) -> None`: Save library data to JSON file
- `load_library(filepath) -> dict`: Load library data from JSON file

### Error Handling

Custom exceptions for domain errors:

- `LibraryError`: Base exception for library errors
- `BookNotFoundError`: Raised when an ISBN doesn't exist
- `BookAlreadyExistsError`: Raised when adding a duplicate ISBN
- `BookNotAvailableError`: Raised when trying to checkout an unavailable book
- `BookAlreadyAvailableError`: Raised when trying to return an available book
- `StorageError`: Raised when file operations fail

## What the Final Behavior Looks Like

Here's how your completed library system should work:

```python
from week02_fundamentals_advanced.project.starter.library import (
    add_book, checkout_book, return_book, search_books, list_all_books
)
from week02_fundamentals_advanced.project.starter.storage import (
    save_library, load_library
)

# Create a new library (just a dictionary)
lib = {}

# Add some books
book1 = add_book(lib, "Effective Python", "Brett Slatkin", "9780134685991")
book2 = add_book(lib, "Clean Code", "Robert Martin", "9780132350884")
print(f"Added: {book1['title']} and {book2['title']}")
# Output: Added: Effective Python and Clean Code

# Search for books
results = search_books(lib, "python")
print(f"Found {len(results)} book(s) matching 'python'")
# Output: Found 1 book(s) matching 'python'

# Checkout a book
checked_out = checkout_book(lib, "9780134685991")
print(f"Checked out: {checked_out['title']} at {checked_out['checked_out_at']}")
# Output: Checked out: Effective Python at 2024-01-15T09:30:00.000000

# Try to checkout same book (raises exception)
from week02_fundamentals_advanced.project.starter.exceptions import BookNotAvailableError
try:
    checkout_book(lib, "9780134685991")
except BookNotAvailableError as e:
    print(f"Error: {e}")
# Output: Error: Book 'Effective Python' is not available for checkout (already checked out)

# Return the book
returned = return_book(lib, "9780134685991")
print(f"Returned: {returned['title']}, available={returned['available']}")
# Output: Returned: Effective Python, available=True

# Save to file
save_library(lib, "my_library.json")
print("Library saved!")

# Load from file
loaded = load_library("my_library.json")
print(f"Loaded {len(loaded)} books from file")
# Output: Loaded 2 books from file
```

### Expected Test Results

All 85 tests should pass:

```bash
$ pytest week02_fundamentals_advanced/project/tests/ -v
============================= test session starts =============================
...
week02_fundamentals_advanced/project/tests/test_library.py::TestLibraryWorkflow::test_full_checkout_return_cycle PASSED
week02_fundamentals_advanced/project/tests/test_library.py::TestLibraryWorkflow::test_persistence_workflow PASSED
========================= 85 passed in 0.15s ================================
```

## Connection to Daily Lessons

This project brings together concepts from all 6 days of Week 2:

| Project Component | Day Lesson | How It Connects |
|-------------------|------------|-----------------|
| `save_library()` / `load_library()` | **Day 1: File I/O** | Uses `json.dump()`/`json.load()`, context managers (`with` statements), and `pathlib.Path` for atomic file writes |
| `storage.py` atomic writes | **Day 1: File I/O** | Creates temp files with `tempfile.mkstemp()` and uses `os.replace()` for safe writes |
| Custom exceptions | **Day 2: Exceptions** | Hierarchy of 6 exception classes inheriting from `LibraryError`, with descriptive messages and stored attributes |
| Exception handling | **Day 2: Exceptions** | Functions raise specific exceptions (`BookNotFoundError`, `InvalidISBNError`) instead of returning error codes |
| Module organization | **Day 3: Modules** | Four separate modules (`book`, `storage`, `library`, `exceptions`) with clear responsibilities and absolute imports |
| `__init__.py` files | **Day 3: Modules** | Proper package structure enabling imports like `from week02_fundamentals_advanced.project.starter.library import add_book` |
| `search_books()` | **Day 4: Comprehensions** | Uses list comprehensions with filtering: `[book for book in library.values() if book_matches_query(book, query)]` |
| List filtering | **Day 4: Comprehensions** | `list_available_books()` and `list_checked_out_books()` use comprehensions to filter collections |
| Sorting operations | **Day 4: Comprehensions** | Uses `list.sort(key=lambda b: b.get("title").lower())` for consistent ordering |
| Pure functions | **Day 5: Functional** | Functions like `is_valid_isbn()`, `normalize_isbn()`, `book_matches_query()` are pure with no side effects |
| Higher-order patterns | **Day 5: Functional** | `book_matches_query()` passed as predicate; lambda functions for sorting keys |
| Immutable data | **Day 5: Functional** | Book dictionaries are treated as values; ISBN normalization ensures consistent keys |
| Test suite | **Day 6: Testing** | 85 tests using pytest fixtures (`empty_library`, `populated_library`, `temp_dir`), parametrization, and tmp_path |
| Fixtures | **Day 6: Testing** | `populated_library` fixture uses `add_book()` to set up test state; `temp_dir` for file isolation |

## File Structure

```
project/
├── README.md                 # This file
├── starter/                  # Incomplete code with TODOs
│   ├── __init__.py
│   ├── exceptions.py         # Custom exception classes
│   ├── book.py              # Book data operations
│   ├── storage.py           # File I/O operations
│   └── library.py           # Main library functions
├── reference_solution/       # Complete working implementation
│   ├── __init__.py
│   ├── exceptions.py
│   ├── book.py
│   ├── storage.py
│   └── library.py
└── tests/
    ├── __init__.py
    └── test_library.py      # Comprehensive test suite
```

## Module Responsibilities

### `exceptions.py`

Defines the exception hierarchy for the library system. All exceptions inherit from `LibraryError`.

Key functions:
- `LibraryError.__init__(message)` - Base exception with message storage
- `BookNotFoundError.__init__(isbn)` - Store ISBN in exception attribute
- `InvalidISBNError.__init__(isbn, reason)` - Store ISBN and reason for invalid format

### `book.py`

Book data structure and operations:

- `create_book(title, author, isbn) -> dict`: Create a new book dictionary
- `is_valid_isbn(isbn) -> bool`: Validate ISBN format (13 characters, alphanumeric)
- `format_book_display(book) -> str`: Pretty-print a book for display

Book dictionary structure:

```python
{
    "isbn": "9780134685991",
    "title": "Effective Python",
    "author": "Brett Slatkin",
    "available": True,
    "checked_out_at": None  # ISO timestamp when checked out
}
```

### `storage.py`

File persistence operations:

- Save/load library to/from JSON
- Handle file path errors
- Atomic write operations (write to temp file, then rename)

### `library.py`

Main API that orchestrates book operations and storage:

- All public functions for managing the library
- Combines operations from other modules
- Handles library state as a dictionary

## How to Run

### Setup

From the repository root:

```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

### Run the Reference Solution

```python
from week02_fundamentals_advanced.project.reference_solution.library import (
    add_book, checkout_book, save_library, load_library
)

# Create a new library
lib = {}

# Add some books
add_book(lib, "Effective Python", "Brett Slatkin", "9780134685991")
add_book(lib, "Clean Code", "Robert Martin", "9780132350884")

# Checkout a book
checkout_book(lib, "9780134685991")

# Save to file
save_library(lib, "my_library.json")

# Load from file
loaded = load_library("my_library.json")
print(f"Loaded {len(loaded)} books")
```

### Run Tests

From the repository root:

```bash
# Run all project tests
pytest week02_fundamentals_advanced/project/tests/ -v

# Run with coverage
pytest week02_fundamentals_advanced/project/tests/ --cov=week02_fundamentals_advanced.project.reference_solution
```

### Work with the Starter Code

**Recommended approach:**

1. Navigate to `week02_fundamentals_advanced/project/starter/`
2. Open each module file and complete the TODOs in this order:
   - **Start with `exceptions.py`**: Define your custom exceptions first - other modules import these
   - **Then `book.py`**: Implement ISBN validation and book creation - foundational for all operations
   - **Next `storage.py`**: Implement file persistence - uses exceptions for error handling
   - **Finally `library.py`**: Implement the main API - orchestrates everything
3. Test your implementation by running the test suite against your code
4. Compare with the reference solution when needed

**Why this order?**
- `exceptions.py` has no dependencies - start here to build your error handling foundation
- `book.py` only depends on exceptions - implement validation logic next
- `storage.py` depends on exceptions - uses them for file operation failures
- `library.py` depends on all three - brings everything together

## Testing Strategy

The test suite covers:

- **Unit tests**: Each function in isolation
- **Integration tests**: Multiple operations together
- **Error cases**: Exceptions raised appropriately
- **File I/O**: Using pytest's `tmp_path` fixture for temp directories
- **Edge cases**: Empty libraries, invalid inputs, boundary conditions

## Project Completion Checklist

- [ ] All starter TODOs completed
- [ ] `add_book` validates ISBN and prevents duplicates
- [ ] `checkout_book` and `return_book` handle state correctly
- [ ] `search_books` finds partial matches case-insensitively
- [ ] All custom exceptions defined and used appropriately
- [ ] JSON persistence works correctly
- [ ] All tests pass
- [ ] No wildcard imports used
- [ ] Type hints on all functions

## Tips

1. **Start with exceptions**: Define the exception hierarchy first
2. **Test early**: Write a test, then implement the function
3. **Validate inputs**: Check ISBN format and raise appropriate exceptions
4. **Immutable operations**: Consider returning new data rather than modifying in place
5. **Atomic writes**: Use a temporary file when saving to prevent data corruption
6. **Read the tests**: The test file shows exactly what behavior is expected
