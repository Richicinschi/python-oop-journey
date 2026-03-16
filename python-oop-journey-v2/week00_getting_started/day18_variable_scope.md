# Day 18: Variable Scope

## Learning Objectives

By the end of this day, you will:

- Understand the difference between local and global scope
- Know when variables are accessible
- Learn how to read (but avoid writing) global variables
- Understand function parameter scope

---

## Key Concepts

### 1. Local Scope

Variables created inside a function are **local** to that function:

```python
def my_function() -> None:
    local_var = "I'm local"
    print(local_var)  # Works fine

my_function()
print(local_var)  # Error! local_var is not defined outside
```

Local variables:
- Created when the function is called
- Destroyed when the function ends
- Only accessible inside the function

### 2. Global Scope

Variables created outside functions are **global**:

```python
global_var = "I'm global"

def my_function() -> None:
    print(global_var)  # Can read global variables

my_function()  # Prints: I'm global
print(global_var)  # Also works
```

### 3. The `global` Keyword (Use Sparingly!)

To modify a global variable inside a function, use `global`:

```python
counter = 0

def increment() -> None:
    global counter  # Declare we want to modify the global
    counter += 1    # Now this works

increment()
print(counter)  # 1
```

**Warning:** Modifying global variables makes code harder to understand and test. Prefer returning values instead.

Better approach:

```python
def increment(counter: int) -> int:
    """Return the incremented value."""
    return counter + 1

counter = 0
counter = increment(counter)  # Explicit and clear
```

### 4. Parameters Are Local

Function parameters are local variables:

```python
def greet(name: str) -> None:
    # 'name' is a local variable
    print(f"Hello, {name}!")

greet("Alice")
# 'name' doesn't exist here
```

### 5. Shadowing

A local variable can "shadow" a global variable with the same name:

```python
value = "global"

def show_value() -> None:
    value = "local"  # This is a NEW local variable
    print(value)     # Prints: local

show_value()
print(value)         # Prints: global (unchanged!)
```

### 6. Scope Rules Summary

```python
# Global scope
global_x = 10

def outer() -> None:
    # Enclosing scope (if nested)
    outer_x = 20
    
    def inner() -> None:
        # Local scope
        inner_x = 30
        print(inner_x)   # 30 - local
        print(outer_x)   # 20 - enclosing
        print(global_x)  # 10 - global
    
    inner()

outer()
```

**LEGB Rule** (Local, Enclosing, Global, Built-in):
Python looks for variables in this order.

### 7. Best Practices

```python
# AVOID: Modifying global state
total = 0

def add_to_total(value: int) -> None:
    global total  # Try to avoid this pattern
    total += value

# PREFER: Pure functions with return values
def calculate_new_total(current: int, value: int) -> int:
    """Return new total without side effects."""
    return current + value

total = calculate_new_total(total, 10)
```

---

## Common Mistakes

### 1. Using Local Variable Before Assignment

```python
value = 10

def bad_function() -> None:
    print(value)  # This tries to read global 'value'
    value = 20    # But this makes 'value' local!
    # Error: local variable 'value' referenced before assignment

def good_function() -> None:
    global value  # Explicitly say we want global
    print(value)
    value = 20

# Better: Avoid the issue entirely
def better_function(val: int) -> int:
    print(val)
    return 20
```

### 2. Thinking Modification Affects Global

```python
data = [1, 2, 3]

def modify_list() -> None:
    data = [4, 5, 6]  # Creates NEW local list!

modify_list()
print(data)  # Still [1, 2, 3]
```

### 3. Forgetting Parameters Are Local

```python
def calculate(a: int, b: int) -> int:
    result = a + b
    return result

calculate(5, 3)
print(a)       # Error! 'a' is not defined
print(result)  # Error! 'result' is not defined
```

---

## Connection to Exercises

### Problem 01: Local vs Global
Understand the difference between local and global scope.

### Problem 02: Scope Chain
Practice accessing variables from different scopes.

### Problem 03: Pure Counter
Write a function without global state.

### Problem 04: Counter Class
Simulate a counter using a list (reference behavior).

### Problem 05: Accumulator
Build an accumulator function that tracks state properly.

---

## Connection to Project

In the Todo List project, scope helps organize your code:

```python
# Global constants (these are okay!)
DATA_FILE = "tasks.json"
PRIORITIES = ["low", "medium", "high"]

def load_tasks() -> list[dict]:
    """Load tasks from file - local variables only."""
    try:
        with open(DATA_FILE, 'r') as f:  # f is local
            content = f.read()  # content is local
            return json.loads(content)
    except FileNotFoundError:
        return []  # Return empty list, don't use global

def save_tasks(tasks: list[dict]) -> None:
    """Save tasks - receives data as parameter."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
```

---

## Tips for Success

1. **Prefer local variables** - They're easier to reason about
2. **Minimize global variables** - They make code harder to test
3. **Use parameters and return values** - Explicit data flow is clearer
4. **Avoid `global` keyword** - There's almost always a better way
5. **Remember LEGB** - Local, Enclosing, Global, Built-in
