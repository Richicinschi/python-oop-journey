# Day 20: Reading Files

## Learning Objectives

By the end of this day, you will be able to:

1. Open files using the `open()` function and `with` statement
2. Read entire files with `read()` method
3. Read files line by line with `readlines()` method
4. Handle file reading errors gracefully
5. Use context managers for safe file handling

---

## Key Concepts

### 1. Opening Files with `open()`

The `open()` function returns a file object that allows you to read from or write to files.

```python
# Basic syntax
file = open('filename.txt', 'r')  # 'r' = read mode (default)
content = file.read()
file.close()  # Always close when done!
```

**Common modes:**
- `'r'` - Read (default)
- `'w'` - Write (creates new or truncates existing)
- `'a'` - Append
- `'r+'` - Read and write

### 2. The `with` Statement (Context Manager)

The `with` statement ensures files are properly closed, even if errors occur.

```python
# Recommended approach
with open('filename.txt', 'r') as file:
    content = file.read()
# File is automatically closed here
```

### 3. Reading Methods

**`read()`** - Read entire file as a single string:

```python
with open('data.txt', 'r') as file:
    content = file.read()
    print(content)
```

**`readlines()`** - Read all lines into a list:

```python
with open('data.txt', 'r') as file:
    lines = file.readlines()
    # Each line includes the newline character
    for line in lines:
        print(line.strip())  # strip() removes whitespace/newlines
```

**Iterate directly over file object** (most memory-efficient):

```python
with open('data.txt', 'r') as file:
    for line in file:
        print(line.strip())
```

### 4. Reading Specific Amounts

```python
with open('data.txt', 'r') as file:
    # Read first 100 characters
    chunk = file.read(100)
    
    # Read next line only
    line = file.readline()
```

### 5. Error Handling

```python
from pathlib import Path

def safe_read_file(filepath: str) -> str | None:
    """Read file safely, returning None if file doesn't exist."""
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None
```

---

## Common Mistakes

### 1. Forgetting to Close Files

```python
# Bad - file stays open
file = open('data.txt', 'r')
data = file.read()
# Forgot to close!

# Good - using with statement
with open('data.txt', 'r') as file:
    data = file.read()
# Automatically closed
```

### 2. Not Handling FileNotFoundError

```python
# Will crash if file doesn't exist
with open('missing.txt', 'r') as file:
    content = file.read()

# Safe approach
try:
    with open('missing.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    content = ""
```

### 3. Reading After File is Closed

```python
with open('data.txt', 'r') as file:
    lines = file.readlines()

# ERROR - file is already closed!
more_content = file.read()
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. read_file_contents | Basic file reading with `read()` |
| 02. count_lines | Using `readlines()` to count lines |
| 03. find_word_in_file | Line-by-line searching |
| 04. read_first_n_lines | Selective reading with `readline()` |
| 05. count_word_occurrences | Text processing from files |

---

## Quick Reference

```python
# Read entire file
with open('file.txt', 'r') as f:
    content = f.read()

# Read lines into list
with open('file.txt', 'r') as f:
    lines = f.readlines()

# Iterate over lines
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Read specific amount
with open('file.txt', 'r') as f:
    chunk = f.read(100)  # First 100 chars

# Safe reading with error handling
try:
    with open('file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    content = None
```

## Connection to Project

Reading files is essential for the Todo List app - you need to load saved tasks:

```python
import json
from pathlib import Path

def load_tasks(filepath: str = "tasks.json") -> list[dict]:
    """Load tasks from JSON file."""
    path = Path(filepath)
    if not path.exists():
        return []  # Return empty list if no file yet
    
    with open(filepath, 'r') as file:
        return json.load(file)

# Usage: tasks are loaded when app starts
tasks = load_tasks()
print(f"Loaded {len(tasks)} tasks")
```

---

## Next Steps

After completing today's exercises:
1. Practice with different file sizes
2. Explore the difference between `read()` and `readlines()`
3. Preview Day 21: **Writing Files**
