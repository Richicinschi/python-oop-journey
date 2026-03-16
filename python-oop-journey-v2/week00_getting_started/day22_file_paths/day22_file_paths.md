# Day 22: File Paths

## Learning Objectives

By the end of this day, you will be able to:

1. Use `pathlib` for modern, object-oriented path handling
2. Create and manipulate `Path` objects
3. Join paths safely across different operating systems
4. Check file and directory existence
5. Extract path components (name, stem, suffix, parent)

---

## Key Concepts

### 1. The `Path` Object

`pathlib` provides an object-oriented interface for filesystem paths.

```python
from pathlib import Path

# Create a Path object
p = Path('/usr/bin/python')

# Relative path
doc = Path('documents') / 'report.txt'
```

### 2. Creating Paths

```python
from pathlib import Path

# From string
home = Path('/home/user')

# Current directory
cwd = Path.cwd()

# Home directory
home = Path.home()

# Join paths (works on all OS)
config = Path.home() / '.config' / 'myapp' / 'settings.ini'
```

### 3. Path Components

```python
from pathlib import Path

p = Path('/home/user/documents/report.txt')

p.name        # 'report.txt'     (filename with extension)
p.stem        # 'report'         (filename without extension)
p.suffix      # '.txt'           (extension)
p.suffixes    # ['.txt']         (all extensions)
p.parent      # Path('/home/user/documents')
p.parents[0]  # Path('/home/user/documents')
p.parents[1]  # Path('/home/user')
p.parts       # ('/', 'home', 'user', 'documents', 'report.txt')
```

### 4. Checking Existence and Type

```python
from pathlib import Path

p = Path('some_file.txt')

p.exists()      # True if path exists
p.is_file()     # True if it's a file
p.is_dir()      # True if it's a directory
p.is_absolute() # True if absolute path
```

### 5. Creating Directories

```python
from pathlib import Path

# Create directory (and parents if needed)
Path('new_folder').mkdir(parents=True, exist_ok=True)
```

---

## Common Mistakes

### 1. Using String Concatenation for Paths

```python
# Bad - won't work on Windows
path = '/home/user' + '/' + 'documents' + '/' + 'file.txt'

# Good - pathlib handles OS differences
path = Path('/home/user') / 'documents' / 'file.txt'
```

### 2. Not Checking Existence Before Operations

```python
from pathlib import Path

# Check before reading
config = Path('config.txt')
if config.exists():
    content = config.read_text()
else:
    content = "default"
```

### 3. Confusing `name` and `stem`

```python
p = Path('document.txt')

p.name   # 'document.txt' (full filename)
p.stem   # 'document'     (filename without extension)
```

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. get_file_extension | Extracting suffix from Path |
| 02. join_paths | Path joining with `/` operator |
| 03. get_filename_without_ext | Using `stem` property |
| 04. path_exists | Checking existence |
| 05. get_parent_directory | Using `parent` property |

---

## Quick Reference

```python
from pathlib import Path

# Create paths
p = Path('folder') / 'file.txt'
p = Path.home() / 'documents'

# Components
p.name       # Filename with ext
p.stem       # Filename without ext
p.suffix     # Extension
p.parent     # Parent directory
p.parts      # Tuple of components

# Checks
p.exists()   # Does it exist?
p.is_file()  # Is it a file?
p.is_dir()   # Is it a directory?

# Create directory
p.mkdir(parents=True, exist_ok=True)
```

## Connection to Project

Use `pathlib` to make your Todo List app work on any operating system:

```python
from pathlib import Path

# Get the directory where the script is located
APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "tasks.json"

def get_data_path(filename: str = "tasks.json") -> Path:
    """Get path to data file, works on Windows, Mac, and Linux."""
    return Path.home() / ".todo_app" / filename

# Create data directory if it doesn't exist
data_dir = Path.home() / ".todo_app"
data_dir.mkdir(parents=True, exist_ok=True)
```

---

## Next Steps

After completing today's exercises:
1. Practice creating complex directory structures
2. Explore `pathlib` methods like `glob()` and `rglob()`
3. Preview Day 23: **Working with CSV**
