# Functions Cheatsheet

Complete guide to defining and using functions in Python.

---

## Defining Functions

### Basic Function

```python
def greet():
    """This is a docstring - describes the function."""
    print("Hello, World!")

# Call the function
greet()
```

### Function with Parameters

```python
def greet(name):
    """Greet a specific person."""
    print(f"Hello, {name}!")

greet("Alice")  # Output: Hello, Alice!
```

### Function with Return Value

```python
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

result = add(3, 5)  # result is 8
```

### Multiple Return Values

```python
def get_min_max(numbers):
    """Return both min and max."""
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([3, 1, 4, 1, 5])
```

---

## Parameter Types

### Required Parameters

```python
def greet(name, greeting):
    print(f"{greeting}, {name}!")

greet("Alice", "Hello")  # Both required
```

### Default Parameters

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")          # Hi, Bob!

# Important: Default values are evaluated once!
def append_item(item, my_list=[]):
    my_list.append(item)
    return my_list

# Better - use None as default
def append_item(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

### Keyword Arguments

```python
def create_user(name, age, city="Unknown"):
    print(f"{name}, {age}, from {city}")

# Order doesn't matter with keywords
create_user(age=25, name="Alice")
create_user("Bob", city="NYC", age=30)
```

### *args - Variable Positional Arguments

```python
def sum_all(*numbers):
    """Accept any number of positional arguments."""
    total = 0
    for n in numbers:
        total += n
    return total

sum_all(1, 2, 3)      # 6
sum_all()             # 0
sum_all(1, 2, 3, 4, 5)  # 15

# Inside function, args is a tuple
def show_args(*args):
    print(args)       # (1, 2, 3)
    print(type(args)) # <class 'tuple'>
```

### **kwargs - Variable Keyword Arguments

```python
def print_info(**kwargs):
    """Accept any number of keyword arguments."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25)

# Inside function, kwargs is a dictionary
def show_kwargs(**kwargs):
    print(kwargs)       # {'name': 'Alice', 'age': 25}
    print(type(kwargs)) # <class 'dict'>
```

### Combined Parameter Types

```python
def complex_function(
    required,
    default="value",
    *args,
    keyword_only,
    **kwargs
):
    """
    Order matters:
    1. Required positional
    2. Default/optional positional
    3. *args
    4. Keyword-only (after * or *args)
    5. **kwargs
    """
    pass

# Keyword-only with *
def func(*, keyword_only):
    """All parameters after * are keyword-only."""
    pass

func(keyword_only=5)  # Must use keyword!
```

---

## Argument Unpacking

```python
# Unpack list/tuple with *
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
result = add(*nums)   # Same as add(1, 2, 3)

# Unpack dictionary with **
def create_user(name, age):
    return {"name": name, "age": age}

data = {"name": "Alice", "age": 25}
user = create_user(**data)  # Same as create_user(name="Alice", age=25)
```

---

## Lambda Functions

```python
# Short anonymous functions
square = lambda x: x ** 2
square(5)  # 25

# Multiple parameters
add = lambda x, y: x + y
add(3, 4)  # 7

# Common use with sorted
students = [("Alice", 25), ("Bob", 20), ("Charlie", 23)]
students.sort(key=lambda x: x[1])  # Sort by age

# With map, filter
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

---

## Scope and Variables

```python
# Local variables
def my_func():
    x = 10        # Local to my_func
    print(x)

# Global variables
x = 100           # Global

def my_func():
    print(x)      # Can read global

# Modifying global
def my_func():
    global x
    x = 200       # Modifies global x

# Nonlocal (for nested functions)
def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20    # Modifies outer's x
    inner()
    print(x)      # 20
```

---

## Built-in Functions Reference

### Type Conversion

| Function | Description | Example |
|----------|-------------|---------|
| `int(x)` | Convert to integer | `int("42")` → `42` |
| `float(x)` | Convert to float | `float("3.14")` → `3.14` |
| `str(x)` | Convert to string | `str(42)` → `"42"` |
| `bool(x)` | Convert to boolean | `bool(1)` → `True` |
| `list(x)` | Convert to list | `list("abc")` → `['a','b','c']` |
| `tuple(x)` | Convert to tuple | `tuple([1,2])` → `(1,2)` |
| `set(x)` | Convert to set | `set([1,1,2])` → `{1,2}` |
| `dict(x)` | Convert to dict | `dict([("a",1)])` |

### Math Functions

| Function | Description | Example |
|----------|-------------|---------|
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `round(x, n)` | Round to n decimals | `round(3.14159, 2)` → `3.14` |
| `divmod(a, b)` | Quotient and remainder | `divmod(17, 5)` → `(3, 2)` |
| `pow(x, y)` | x to power y | `pow(2, 3)` → `8` |
| `sum(iter)` | Sum of iterable | `sum([1,2,3])` → `6` |
| `min(iter)` | Minimum value | `min([3,1,4])` → `1` |
| `max(iter)` | Maximum value | `max([3,1,4])` → `4` |

### Sequence Functions

| Function | Description | Example |
|----------|-------------|---------|
| `len(x)` | Length | `len("hello")` → `5` |
| `range(stop)` | Generate sequence | `range(5)` → `0,1,2,3,4` |
| `range(start, stop, step)` | Range with options | `range(0, 10, 2)` |
| `enumerate(iter)` | Index and value | `enumerate(["a","b"])` |
| `zip(*iters)` | Pair iterables | `zip([1,2], ["a","b"])` |
| `sorted(iter)` | Return sorted list | `sorted([3,1,2])` |
| `reversed(iter)` | Reverse iterator | `reversed([1,2,3])` |

### Input/Output

| Function | Description | Example |
|----------|-------------|---------|
| `print(*objects)` | Print to console | `print("Hello")` |
| `input(prompt)` | Read user input | `name = input("Name: ")` |
| `open(file)` | Open file | `open("data.txt")` |

### Object Functions

| Function | Description | Example |
|----------|-------------|---------|
| `type(x)` | Type of object | `type(42)` → `<class 'int'>` |
| `isinstance(x, type)` | Type check | `isinstance(42, int)` → `True` |
| `id(x)` | Object identity | `id(x)` |
| `dir(x)` | List attributes | `dir(str)` |
| `help(x)` | Documentation | `help(str)` |
| `callable(x)` | Is callable? | `callable(print)` → `True` |

### Logical/Functional

| Function | Description | Example |
|----------|-------------|---------|
| `all(iter)` | All True? | `all([True, True])` → `True` |
| `any(iter)` | Any True? | `any([False, True])` → `True` |
| `map(func, iter)` | Apply function | `map(str, [1,2,3])` |
| `filter(func, iter)` | Filter items | `filter(None, [0,1,2])` |

---

## Decorators (Advanced)

```python
# A decorator is a function that modifies another function
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Equivalent to: say_hello = my_decorator(say_hello)

say_hello()
# Output:
# Before
# Hello!
# After
```

---

## Function Best Practices

1. **Use docstrings** to document what the function does
2. **Keep functions small** and focused on one task
3. **Use descriptive names** like `calculate_area` not `calc`
4. **Avoid side effects** when possible (pure functions)
5. **Return early** to reduce nesting
6. **Use type hints** (Python 3.5+) for clarity:

```python
def greet(name: str, age: int) -> str:
    """Return a greeting string."""
    return f"Hello {name}, you are {age}"
```
