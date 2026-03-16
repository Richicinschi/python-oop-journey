# Day 3: Modules and Packages

## Learning Objectives

By the end of this day, you will be able to:

1. Understand what Python modules are and how they work
2. Create and import modules using various import styles
3. Use `if __name__ == "__main__":` to make modules both importable and executable
4. Structure code into packages with proper `__init__.py` files
5. Understand `sys.path` and how Python finds modules
6. Create and use plugin architectures with module registries
7. Manage namespaces and avoid common import pitfalls

---

## Key Concepts

### 1. What is a Module?

A **module** is simply a Python file (`.py`) containing definitions and statements. When you import a module, Python executes the file and makes its contents available.

```python
# mymath.py - this is a module
PI = 3.14159

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

```python
# main.py - importing the module
import mymath
print(mymath.PI)          # 3.14159
print(mymath.add(2, 3))   # 5
```

### 2. Import Styles

Python offers multiple ways to import modules:

**Import the entire module:**
```python
import math
print(math.sqrt(16))  # 4.0
```

**Import specific names:**
```python
from math import sqrt, pi
print(sqrt(16))   # 4.0
print(pi)         # 3.14159...
```

**Import with alias:**
```python
import numpy as np
from datetime import datetime as dt
```

**Avoid wildcard imports:**
```python
# DON'T DO THIS - pollutes namespace, unclear where names come from
from math import *
```

### 3. Module Execution and `__name__ == "__main__"`

Every module has a `__name__` attribute:
- When a file is run directly: `__name__ == "__main__"`
- When a file is imported: `__name__ == "module_name"`

```python
# calculator.py
print(f"Loading calculator module, __name__ = {__name__}")

def add(a, b):
    return a + b

# This code only runs when the file is executed directly
if __name__ == "__main__":
    print("Running calculator as main program")
    print(f"2 + 3 = {add(2, 3)}")
```

Running directly:
```bash
$ python calculator.py
Loading calculator module, __name__ = __main__
Running calculator as main program
2 + 3 = 5
```

Importing:
```python
import calculator
# Output: Loading calculator module, __name__ = calculator
# The test code does NOT run
```

**Benefits of this pattern:**
- Makes modules importable without side effects
- Allows self-testing within the module
- Separates reusable code from execution code

### 4. Module-Only State

Modules are singletons - Python loads them once and caches them in `sys.modules`. This makes them useful for shared state:

```python
# counter_module.py
count = 0

def increment():
    global count
    count += 1
    return count

def get_count():
    return count
```

```python
# main.py
import counter_module

print(counter_module.get_count())   # 0
counter_module.increment()
counter_module.increment()
print(counter_module.get_count())   # 2

import counter_module  # Same module, same count!
print(counter_module.get_count())   # 2 (not 0)
```

### 5. Packages

A **package** is a directory containing modules and an `__init__.py` file (can be empty).

```
mymath/
    __init__.py
    basic.py
    advanced.py
    utils.py
```

```python
# mymath/__init__.py
from .basic import add, subtract
from .advanced import power, sqrt

__version__ = "1.0.0"
```

```python
# mymath/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

Usage:
```python
import mymath
print(mymath.add(2, 3))  # 5
print(mymath.__version__)  # 1.0.0
```

### 6. sys.path and Module Discovery

Python searches for modules in directories listed in `sys.path`:

```python
import sys
print(sys.path)
# ['', '/usr/lib/python310.zip', '/usr/lib/python3.10', ...]
```

The search order is:
1. Current directory (empty string `''`)
2. `PYTHONPATH` environment variable directories
3. Installation-dependent default paths

**Adding a custom path (rarely needed):**
```python
import sys
sys.path.insert(0, '/path/to/my/modules')
```

**Note:** Avoid modifying `sys.path` in production code. Use proper package installation instead.

### 7. The `__all__` Variable

Control what gets imported with `from module import *`:

```python
# string_utils.py
__all__ = ['capitalize_words', 'reverse_words']  # Only these are exported

def capitalize_words(text):
    return ' '.join(word.capitalize() for word in text.split())

def reverse_words(text):
    return ' '.join(reversed(text.split()))

def _internal_helper():  # Not in __all__
    pass
```

### 8. Plugin Architecture Pattern

A common pattern for extensible systems:

```python
# plugins/__init__.py
_registry = {}

def register(name, plugin):
    _registry[name] = plugin

def get_plugin(name):
    return _registry.get(name)

def list_plugins():
    return list(_registry.keys())
```

```python
# plugins/email_plugin.py
from . import register

def send_email(to, message):
    print(f"Sending email to {to}: {message}")

register('email', send_email)
```

```python
# main.py
import plugins.email_plugin  # Registers the plugin
from plugins import get_plugin

email_func = get_plugin('email')
email_func('user@example.com', 'Hello!')
```

### 9. Relative Imports

Within packages, use relative imports:

```python
# mypackage/submodule.py
from . import sibling_module        # Same package
from .parent import ParentClass      # Parent module
from .. import grandparent_module    # Parent package
from ..sibling import SiblingClass   # Sibling of parent
```

**Important:** Relative imports only work inside packages, not in top-level scripts.

---

## Common Mistakes

### 1. Circular Imports

```python
# a.py
from b import func_b  # Imports b

def func_a():
    return func_b()

# b.py
from a import func_a  # Imports a - CIRCULAR!

def func_b():
    return "Hello"
```

**Solutions:**
- Restructure to remove the circular dependency
- Use late imports (inside functions)
- Use abstract base classes or interfaces

### 2. Naming Conflicts

```python
# DON'T name your module like a standard library module
# random.py, time.py, io.py, sys.py, etc.

# When you do:
import random  # Imports YOUR random.py, not stdlib!
```

### 3. Import Side Effects

```python
# bad_module.py
print("Running expensive operation...")  # Runs on import!
data = load_large_dataset()  # Runs on import!

def useful_function():
    pass
```

**Solution:** Use `if __name__ == "__main__":` or lazy initialization.

### 4. Modifying sys.path Improperly

```python
# DON'T do this in library code
import sys
sys.path.insert(0, '../some/path')  # Fragile!

# Better: proper package installation
```

### 5. Mutable Default Arguments in Modules

```python
# config.py - shared mutable state
default_settings = {}  # Shared by all imports!

def get_settings():
    return default_settings
```

### 6. Not Using `__all__`

Without `__all__`, `from module import *` imports all names that don't start with underscore, including imports from other modules.

---

## Connection to Exercises

| Problem | Skills Practiced |
|---------|------------------|
| 01. module_counter | Module-level state, import tracking |
| 02. import_tracker | Decorators with module state, function metadata |
| 03. plugin_registry | Registry pattern, dynamic registration |
| 04. package_math_tools | Creating packages, submodules, `__init__.py` |
| 05. string_utils_module | Module organization, `__all__` |
| 06. calculator_package | Package structure, relative imports |
| 07. config_package_loader | Multi-source config, package organization |
| 08. namespace_cleanup | Namespace management, selective imports |

---

## Weekly Project Connection

The Week 2 project is a **Procedural Library System**. Day 3's concepts are essential because:

- **Modules** separate different concerns (books, members, loans, reports)
- **Packages** organize related functionality cleanly
- **Plugin pattern** allows extending the system (different report formats, storage backends)
- **Main guard** allows running modules standalone for testing

---

## Quick Reference

```python
# Module structure
"""Module docstring."""
from __future__ import annotations
import standard_lib
import third_party
import local_module

__all__ = ['public_function', 'PublicClass']

# Module-level constants
DEFAULT_VALUE = 100

# Classes and functions
class MyClass:
    pass

def public_function():
    pass

def _private_helper():
    pass

# Main guard
if __name__ == "__main__":
    # Test code or CLI entry point
    pass

# Package __init__.py structure
"""Package description."""
from __future__ import annotations

from .module1 import func1
from .module2 import Class2

__version__ = "1.0.0"
__all__ = ['func1', 'Class2']
```

---

## Next Steps

After completing today's exercises:
1. Review how modules enable code reuse across files
2. Practice creating a simple package with multiple modules
3. Preview Day 4: **Comprehensions and Generators** - for concise data processing
