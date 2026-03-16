# Day 6: Functions and Recursion

## Learning Objectives

By the end of this day, you will:

- Define and call functions with proper syntax and conventions
- Understand positional, keyword, default, and variable-length arguments
- Return single and multiple values from functions
- Grasp the concept of recursion and when to use it
- Identify base cases and recursive cases in recursive algorithms
- Solve classic problems using recursion (Fibonacci, factorial, search)
- Understand the call stack and recursion depth limits
- Apply memoization to optimize recursive solutions

---

## Key Concepts

### 1. Defining Functions

Functions are reusable blocks of code that perform specific tasks.

```python
def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")  # "Hello, Alice!"
```

**Key elements:**
- `def` keyword to define a function
- Function name (should be descriptive, lowercase with underscores)
- Parameters in parentheses (can include type hints)
- Docstring describing what the function does
- Function body (indented)
- Optional `return` statement

### 2. Parameters and Arguments

**Positional arguments:** Matched by position.
```python
def power(base: int, exponent: int) -> int:
    return base ** exponent

result = power(2, 3)  # base=2, exponent=3
```

**Keyword arguments:** Matched by name, can be in any order.
```python
result = power(exponent=3, base=2)  # Same result
```

**Default parameters:** Provide default values.
```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

greet("Bob")              # "Hello, Bob!"
greet("Bob", "Hi")        # "Hi, Bob!"
```

**Important:** Default values are evaluated once at definition time, not at call time.

```python
def append_item(item: int, lst: list | None = None) -> list:
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# Avoid: def bad(item, lst=[]):
```

### 3. Return Values

Functions can return single values or multiple values (as a tuple).

```python
def min_max(numbers: list[int]) -> tuple[int, int]:
    """Return minimum and maximum values."""
    return min(numbers), max(numbers)

minimum, maximum = min_max([3, 1, 4, 1, 5])
```

Functions without explicit `return` return `None`.

### 4. Variable-Length Arguments

```python
def sum_all(*args: int) -> int:
    """Sum any number of arguments."""
    return sum(args)

result = sum_all(1, 2, 3, 4)  # 10
```

```python
def print_info(**kwargs: str) -> None:
    """Print key-value pairs."""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age="30")
```

### 5. Recursion Basics

Recursion is when a function calls itself to solve a smaller version of the same problem.

**Components of recursion:**
1. **Base case**: The simplest case that can be solved directly (stops recursion)
2. **Recursive case**: The function calls itself with a smaller subproblem

```python
def countdown(n: int) -> None:
    """Count down from n to 0."""
    if n < 0:  # Base case
        return
    print(n)
    countdown(n - 1)  # Recursive case

countdown(5)  # Prints 5, 4, 3, 2, 1, 0
```

### 6. Classic Recursion: Factorial

```python
def factorial(n: int) -> int:
    """Calculate n! recursively.
    
    n! = n × (n-1) × (n-2) × ... × 1
    0! = 1 (by definition)
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case
```

Visualizing `factorial(4)`:
```
factorial(4)
    4 * factorial(3)
        3 * factorial(2)
            2 * factorial(1)
                return 1
            return 2
        return 6
    return 24
```

### 7. Classic Recursion: Fibonacci

```python
def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (naive recursive approach)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:  # Base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case
```

**Problem:** This has exponential time complexity O(2^n) due to repeated calculations.

### 8. Memoization

Memoization stores results of expensive function calls to avoid redundant calculations.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)

# Manual memoization approach
def fibonacci_manual(n: int, memo: dict[int, int] | None = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_manual(n - 1, memo) + fibonacci_manual(n - 2, memo)
    return memo[n]
```

Time complexity: O(n), Space complexity: O(n)

### 9. Recursion for Search: Binary Search

```python
def binary_search(arr: list[int], target: int, left: int = 0, right: int | None = None) -> int:
    """Find target index in sorted array, or -1 if not found."""
    if right is None:
        right = len(arr) - 1
    
    if left > right:  # Base case: not found
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:  # Base case: found
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)
```

### 10. Recursion for Permutations and Combinations

**Generating all permutations:**
```python
def permutations(items: list) -> list[list]:
    """Generate all permutations of items."""
    if len(items) <= 1:
        return [items]
    
    result = []
    for i, item in enumerate(items):
        rest = items[:i] + items[i+1:]
        for p in permutations(rest):
            result.append([item] + p)
    return result
```

### 11. Understanding the Call Stack

Each recursive call adds a new frame to the call stack:

```python
def factorial_verbose(n: int, depth: int = 0) -> int:
    indent = "  " * depth
    print(f"{indent}factorial({n})")
    
    if n <= 1:
        print(f"{indent}→ return 1")
        return 1
    
    result = n * factorial_verbose(n - 1, depth + 1)
    print(f"{indent}→ return {result}")
    return result

factorial_verbose(3)
# Output:
# factorial(3)
#   factorial(2)
#     factorial(1)
#     → return 1
#   → return 2
# → return 6
```

### 12. Recursion Depth Limit

Python has a default recursion limit (usually 1000):

```python
import sys
print(sys.getrecursionlimit())  # 1000

# Can be increased (use with caution):
sys.setrecursionlimit(2000)
```

Deep recursion can cause a `RecursionError`.

---

## Common Mistakes

### 1. Missing Base Case

```python
def bad_countdown(n: int) -> None:
    print(n)
    bad_countdown(n - 1)  # No base case - infinite recursion!
```

### 2. Not Progressing Toward Base Case

```python
def bad_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return bad_fibonacci(n) + bad_fibonacci(n - 1)  # n never decreases!
```

### 3. Mutable Default Arguments

```python
def bad_append(item: int, items: list = []) -> list:  # Don't do this!
    items.append(item)
    return items

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] - Surprise! The list persists!
```

### 4. Ignoring Return Values

```python
def sum_recursive(numbers: list[int]) -> int:
    if not numbers:
        return 0
    # Bug: Not returning the result!
    numbers[0] + sum_recursive(numbers[1:])  # Missing 'return'
```

### 5. Overusing Recursion

Not every problem needs recursion. Simple iteration is often clearer:

```python
# Overly complex
sum_range(n: int) -> int:
    if n <= 0:
        return 0
    return n + sum_range(n - 1)

# Simpler and more efficient
def sum_range_simple(n: int) -> int:
    return sum(range(n + 1))
```

### 6. Not Handling Edge Cases

```python
def factorial_no_validation(n: int) -> int:
    if n == 0:
        return 1
    return n * factorial_no_validation(n - 1)
    # Crashes with RecursionError for negative inputs
```

---

## Connection to Exercises

### Problems 01-03: Building Intuition (Warm-up)

- **Problem 01 (Fibonacci Recursive)**: Practice basic recursion with the classic sequence
- **Problem 02 (Fibonacci Memoized)**: Learn to optimize recursive solutions
- **Problem 03 (Factorial)**: Master the simplest recursion pattern

**Focus:** Identify base cases and ensure progress toward them.

### Problems 04-05: Recursive Patterns (Core)

- **Problem 04 (Power Recursive)**: Multiple recursive cases (positive/negative exponent)
- **Problem 05 (Binary Search Recursive)**: Divide-and-conquer with index tracking

**Focus:** Managing state across recursive calls (carry extra parameters).

### Problems 06-08: Combinatorial Recursion (Harder)

- **Problem 06 (Permutations)**: Generate all arrangements using choice + recursion
- **Problem 07 (Subsets)**: Build the power set with include/exclude pattern
- **Problem 08 (Combination Sum)**: Backtracking with pruning

**Focus:** Managing partial solutions and backtracking.

### Problems 09-10: Classic Algorithms (Stretch)

- **Problem 09 (N-Queens)**: Constraint satisfaction with backtracking
- **Problem 10 (Word Search)**: 2D grid traversal with state tracking

**Focus:** Complex state management and pruning search spaces.

---

## Weekly Project Connection

The Week 1 project (Command-Line Quiz Game) uses functions to:

- Display questions and collect answers
- Calculate and display scores
- Load quiz data from files
- Manage game state

After mastering Day 6, you'll be able to:
- Organize your quiz game into clean, reusable functions
- Understand function scope and return values
- Use recursion if needed for score calculations or navigation

---

## Tips for Success

1. **Always identify the base case first** before writing recursive code
2. **Trace through small examples** by hand to verify your logic
3. **Draw the recursion tree** to visualize the call pattern
4. **Start with naive recursion**, then add memoization if needed
5. **Watch for off-by-one errors** in index-based recursion
6. **Test edge cases**: empty inputs, single elements, maximum depth
7. **When stuck, write the iterative version first** to understand the pattern
