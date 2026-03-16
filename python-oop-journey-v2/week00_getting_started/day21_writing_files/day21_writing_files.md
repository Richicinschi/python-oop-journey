# Day 21: Writing Files

## Learning Objectives

By the end of this day, you will be able to:

1. Write data to files using the `write()` method
2. Use append mode (`'a'`) to add to existing files
3. Create new files safely
4. Write multiple lines efficiently
5. Handle write errors and permissions

---

## Key Concepts

### 1. Writing with `write()` Method

The `write()` method writes a string to a file.

```python
# Write mode ('w') - creates new or overwrites existing
with open('output.txt', 'w') as file:
    file.write('Hello, World!')
```

**Important:** Write mode (`'w'`) will **overwrite** existing file contents!

### 2. Append Mode (`'a'`)

Append mode adds content to the end of a file without deleting existing content.

```python
# Append mode ('a') - creates new or adds to existing
with open('log.txt', 'a') as file:
    file.write('New log entry\n')
```

### 3. Writing Multiple Lines

```python
lines = ['First line', 'Second line', 'Third line']

# Using write() with newlines
with open('output.txt', 'w') as file:
    for line in lines:
        file.write(line + '\n')

# Using writelines() - note: doesn't add newlines automatically
with open('output.txt', 'w') as file:
    file.writelines([line + '\n' for line in lines])
```

### 4. Creating New Files Safely

```python
from pathlib import Path

def create_file_if_not_exists(filepath: str, content: str = "") -> bool:
    """Create a new file only if it doesn't exist."""
    path = Path(filepath)
    if path.exists():
        return False  # File already exists
    
    with open(filepath, 'w') as file:
        file.write(content)
    return True
```

### 5. Error Handling

```python
try:
    with open('output.txt', 'w') as file:
        file.write('Important data')
except PermissionError:
    print('Permission denied - cannot write to file')
except IOError as e:
    print(f'I/O error occurred: {e}')
```

---

## Common Mistakes

### 1. Forgetting Newlines

```python
# Bad - everything on one line
with open('output.txt', 'w') as file:
    file.write('Line 1')
    file.write('Line 2')
# Result: Line 1Line 2

# Good - add newlines
with open('output.txt', 'w') as file:
    file.write('Line 1\n')
    file.write('Line 2\n')
```

### 2. Using Read Mode for Writing

```python
# ERROR - trying to write in read mode
with open('file.txt', 'r') as file:
    file.write('data')  # io.UnsupportedOperation: not writable
```

### 3. Accidentally Overwriting Files

```python
# Dangerous - overwrites existing content
with open('important.txt', 'w') as file:
    file.write('new data')

# Safer - check if file exists first
from pathlib import Path
if not Path('important.txt').exists():
    with open('important.txt', 'w') as file:
        file.write('new data')
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. write_string_to_file | Basic file writing |
| 02. append_to_file | Append mode usage |
| 03. write_lines_to_file | Writing multiple lines |
| 04. create_new_file | Safe file creation |
| 05. overwrite_file | Controlled file overwriting |

---

## Quick Reference

```python
# Write (overwrite existing)
with open('file.txt', 'w') as f:
    f.write('content')

# Append (add to end)
with open('file.txt', 'a') as f:
    f.write('more content\n')

# Write multiple lines
with open('file.txt', 'w') as f:
    f.writelines(['line1\n', 'line2\n'])

# Create only if not exists
from pathlib import Path
if not Path('file.txt').exists():
    with open('file.txt', 'w') as f:
        f.write('')

# Error handling
try:
    with open('file.txt', 'w') as f:
        f.write('data')
except PermissionError:
    pass
```

## Connection to Project

Writing files saves your Todo List data between sessions:

```python
import json
from pathlib import Path

def save_tasks(tasks: list[dict], filepath: str = "tasks.json") -> None:
    """Save tasks to JSON file."""
    with open(filepath, 'w') as file:
        json.dump(tasks, file, indent=2)

# Usage: save after every change
tasks = [{"id": 1, "description": "Buy milk", "completed": False}]
save_tasks(tasks)  # Data persists after app closes!
```

---

## Next Steps

After completing today's exercises:
1. Practice appending to log files
2. Experiment with different write modes
3. Preview Day 22: **File Paths**
