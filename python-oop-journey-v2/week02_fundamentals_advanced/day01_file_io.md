# Day 1: File I/O and File Processing

## Learning Objectives

By the end of this day, you will be able to:

1. Open, read from, and write to files using Python's built-in `open()` function
2. Use context managers (`with` statement) for safe file handling
3. Understand different file modes: read, write, append, binary
4. Process CSV files using the `csv` module
5. Work with JSON data using the `json` module
6. Navigate filesystems using the `pathlib` module
7. Create custom context managers for resource management

---

## Key Concepts

### 1. Opening Files with `open()`

The `open()` function returns a file object for reading or writing:

```python
# Basic file opening
file = open('data.txt', 'r')  # Open for reading
content = file.read()
file.close()  # Must close to free resources
```

**File Modes:**

| Mode | Description |
|------|-------------|
| `'r'` | Read (default). File must exist. |
| `'w'` | Write. Creates new file or truncates existing. |
| `'a'` | Append. Creates new file or appends to existing. |
| `'x'` | Exclusive creation. Fails if file exists. |
| `'b'` | Binary mode (e.g., `'rb'`, `'wb'`). |
| `'+'` | Read and write (e.g., `'r+'`). |

---

### 2. Context Managers (`with` Statement)

Context managers ensure files are properly closed, even if errors occur:

```python
# Recommended approach - context manager
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed here

# Equivalent to:
file = open('data.txt', 'r')
try:
    content = file.read()
finally:
    file.close()
```

**Reading methods:**

```python
with open('data.txt', 'r') as f:
    # Read entire file as string
    content = f.read()
    
    # Read line by line (memory efficient for large files)
    for line in f:
        process(line.strip())
    
    # Read all lines into a list
    lines = f.readlines()
    
    # Read single line
    first_line = f.readline()
```

---

### 3. Writing to Files

```python
# Write mode (overwrites existing content)
with open('output.txt', 'w') as f:
    f.write('Hello, World!\n')
    f.writelines(['Line 1\n', 'Line 2\n'])

# Append mode (adds to existing content)
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

---

### 4. Working with CSV Files

The `csv` module handles comma-separated values:

```python
import csv

# Reading CSV
with open('data.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
    for row in reader:
        name, age = row[0], int(row[1])
        print(f'{name} is {age} years old')

# Reading as dictionaries
with open('data.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

# Writing CSV
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age'])
    writer.writerows([['Alice', 30], ['Bob', 25]])
```

**Note:** Always use `newline=''` when opening CSV files to prevent blank lines on Windows.

---

### 5. Working with JSON Files

The `json` module handles JavaScript Object Notation:

```python
import json

# Reading JSON
with open('config.json', 'r') as f:
    data = json.load(f)  # Returns Python dict/list

# Writing JSON
config = {'debug': True, 'port': 8080}
with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)

# Working with strings
data = json.dumps({'key': 'value'}, indent=2)
parsed = json.loads(data)
```

---

### 6. Path Manipulation with `pathlib`

Modern, object-oriented path handling (Python 3.4+):

```python
from pathlib import Path

# Creating paths
p = Path('/home/user/documents')
file = p / 'report.txt'  # Path joining with /

# Common operations
if file.exists():
    content = file.read_text()
    
# Directory traversal
for py_file in Path('.').rglob('*.py'):
    print(py_file)

# Creating directories
Path('new_folder').mkdir(parents=True, exist_ok=True)

# File properties
size = file.stat().st_size
modified = file.stat().st_mtime
```

---

### 7. Creating Custom Context Managers

Implement `__enter__` and `__exit__` for custom resource management:

```python
from typing import Any
import time

class Timer:
    """Context manager that times code execution."""
    
    def __enter__(self) -> 'Timer':
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.time() - self.start
        print(f'Elapsed: {self.elapsed:.4f} seconds')

# Usage
with Timer() as t:
    # Code to time
    result = sum(range(1000000))
```

**Using `contextlib` decorator:**

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name: str):
    print(f'Acquiring {name}')
    resource = create_resource(name)
    try:
        yield resource
    finally:
        print(f'Releasing {name}')
        resource.cleanup()
```

---

## Common Mistakes

### 1. Not Closing Files

```python
# Bad - resource leak
file = open('data.txt')
data = file.read()
# Forgot to close!

# Good - context manager
with open('data.txt') as file:
    data = file.read()
```

### 2. Reading After File is Closed

```python
with open('data.txt') as f:
    lines = f.readlines()

print(lines[0])  # OK - data in memory
content = f.read()  # Error - file is closed!
```

### 3. Incorrect CSV Newlines on Windows

```python
# Bad - creates blank lines on Windows
with open('data.csv', 'w') as f:
    writer = csv.writer(f)

# Good
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
```

### 4. Reading Large Files Into Memory

```python
# Bad for large files - consumes memory
with open('huge.log') as f:
    lines = f.readlines()  # Loads everything!
    
# Good - iterate line by line
with open('huge.log') as f:
    for line in f:  # Memory efficient
        process(line)
```

### 5. String vs Binary Mode Confusion

```python
# Text mode (default)
with open('text.txt', 'r') as f:
    content = f.read()  # Returns str

# Binary mode
with open('image.png', 'rb') as f:
    data = f.read()  # Returns bytes
```

### 6. Path Concatenation with Strings

```python
# Bad - platform dependent
path = folder + '/' + filename  # Fails on Windows

# Good - pathlib
from pathlib import Path
path = Path(folder) / filename
```

---

## Connection to Exercises

Today's exercises reinforce these concepts through practical problems:

| Problem | Skills Practiced |
|---------|------------------|
| 01. count_lines | File reading, iteration |
| 02. find_longest_line | Text processing, file traversal |
| 03. word_frequency | String processing, dictionaries |
| 04. merge_files | Multiple file handling, writing |
| 05. filter_lines | Pattern matching, filtering |
| 06. csv_column_sum | CSV parsing, data aggregation |
| 07. merge_json_files | JSON processing, merging data |
| 08. analyze_log | Log parsing, statistics |
| 09. timer_context | Custom context managers |
| 10. safe_file_writer | Atomic operations, backup |
| 11. directory_tree | Pathlib, recursion |

---

## Weekly Project Connection

The Week 2 project is a **Procedural Library System**. Day 1's concepts are essential because:

- **File I/O** stores book records persistently
- **CSV/JSON** handles data import/export
- **Context managers** ensure data integrity during writes
- **Pathlib** manages configuration and data directories

---

## Quick Reference

```python
from pathlib import Path
import csv
import json

# Reading a file
with open('file.txt', 'r') as f:
    content = f.read()

# Writing a file
with open('file.txt', 'w') as f:
    f.write('content')

# CSV operations
with open('data.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['column'])

# JSON operations
with open('data.json') as f:
    data = json.load(f)

# Pathlib operations
p = Path('folder') / 'file.txt'
if p.exists():
    text = p.read_text()
```

---

## Next Steps

After completing today's exercises:
1. Run the tests to verify your solutions
2. Review any problems you found challenging
3. Preview Day 2: **Exceptions and Defensive Programming**
