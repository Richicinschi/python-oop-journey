# Week 5: Advanced OOP

Deep dive into Python's object model with descriptors, metaclasses, decorators, dataclasses, context managers, and advanced iteration patterns to master class customization and control.

## Week Objective

By the end of this week, you will:
- Create and use descriptors for attribute access control
- Understand and create metaclasses for class-level control
- Build sophisticated decorators with arguments
- Use dataclasses and `__slots__` for cleaner, more efficient code
- Implement custom iterators and generators for memory-efficient processing
- Build context managers with `with` statements for resource management
- Apply reflection and introspection for dynamic object inspection
- Apply these advanced features to build robust, Pythonic systems
- Know when (and when not) to use these powerful features

## Prerequisites

- Completion of Weeks 1-4
- Solid understanding of inheritance, abstract classes, and MRO
- Familiarity with properties and magic methods from Week 3
- Experience with class decorators and advanced function concepts

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Descriptors | 10 | Hard |
| Day 2 | Metaclasses | 10 | Hard |
| Day 3 | Decorators | 13 | Hard |
| Day 4 | Dataclasses and `__slots__` | 6 | Hard |
| Day 5 | Iterators, Generators, and Custom Collections | 6 | Hard |
| Day 6 | Reflection, Introspection, and Context Managers | 6 | Hard |

## File Structure

```
week05_oop_advanced/
├── README.md                        # This file
├── day01_descriptors.md             # Day 1: Descriptors
├── day02_metaclasses.md             # Day 2: Metaclasses
├── day03_decorators.md              # Day 3: Decorators
├── day04_dataclasses_and_slots.md   # Day 4: Dataclasses
├── day05_iterators_generators_collections.md  # Day 5: Iterators
├── day06_reflection_and_context_managers.md   # Day 6: Context Managers
├── exercises/                       # Your working area
│   ├── day01/                       # Day 1 exercises (10 files)
│   ├── day02/                       # Day 2 exercises (10 files)
│   ├── day03/                       # Day 3 exercises (13 files)
│   ├── day04/                       # Day 4 exercises (6 files)
│   ├── day05/                       # Day 5 exercises (6 files)
│   └── day06/                       # Day 6 exercises (6 files)
├── solutions/                       # Reference solutions
│   ├── day01/                       # Day 1 solutions
│   ├── day02/                       # Day 2 solutions
│   ├── day03/                       # Day 3 solutions
│   ├── day04/                       # Day 4 solutions
│   ├── day05/                       # Day 5 solutions
│   └── day06/                       # Day 6 solutions
├── tests/                           # Test suite
│   ├── day01/                       # Day 1 tests
│   ├── day02/                       # Day 2 tests
│   ├── day03/                       # Day 3 tests
│   ├── day04/                       # Day 4 tests
│   ├── day05/                       # Day 5 tests
│   └── day06/                       # Day 6 tests
└── project/                         # Weekly project
    ├── README.md                    # Project documentation
    ├── starter/                     # Starter code
    ├── reference_solution/          # Complete solution
    └── tests/                       # Project tests
```

## Start Here

New to Week 5? Begin with these files:

1. **Read**: `day01_descriptors.md` - Start with the theory
2. **Code**: `exercises/day01/problem_01_validated_attribute.py` - First exercise
3. **Test**: Run `pytest week05_oop_advanced/tests/day01/test_problem_01_validated_attribute.py -v`
4. **Project**: Review `project/README.md` to understand the weekly goal

## Recommended Workflow

### Daily Workflow

1. **Read the theory document** for the day (30-40 minutes)
   - Study the concepts and code examples
   - Run the example code in a Python REPL
   - Understand the execution flow and interactions

2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-05: Core practice
   - Problems 06-08: Advanced application
   - Problems 09-10 (and beyond): Mastery challenges

3. **Check solutions only when stuck**:
   - Try to solve each problem yourself first
   - If stuck for 20+ minutes, review the hints below, then the solution
   - Understand the approach, then implement yourself

4. **Connect to the weekly project**:
   - See how each day's concepts appear in the project
   - Apply what you learned to extend the project

## How to Check Your Work

### The Verification Path

Follow this sequence to verify your solutions without spoiling the learning:

1. **Read the theory doc**  
   Understand the concept before writing code.

2. **Attempt the exercise honestly**  
   Write your solution without looking at reference material.

3. **Run the provided examples manually**  
   Test your code in a Python REPL or small script.

4. **Read the matching reference tests**  
   Tests clarify expected behavior. Run them to see what's required:   
   ```bash
   pytest week05_oop_advanced/tests/day01/test_problem_01_validated_attribute.py -v
   ```

5. **Compare to reference solution only after a real attempt**  
   Solutions are in `solutions/`. Study them after you've tried yourself.

### Running Tests

```bash
# Test specific problem
pytest week05_oop_advanced/tests/day01/test_problem_01_validated_attribute.py -v

# Test all problems for a day
pytest week05_oop_advanced/tests/day01/ -v

# Test entire week
pytest week05_oop_advanced/tests/ -v

# With coverage
pytest week05_oop_advanced/tests/ --cov=week05_oop_advanced
```

### Expected Results

- All tests should pass for the reference solutions
- Your implementation should match the behavior demonstrated in tests
- Edge cases should be handled gracefully

## Debugging Guidance

### Common Week 5 Pitfalls

#### Descriptor `__get__` / `__set__` Confusion

**Symptom**: Descriptor methods not being called, or infinite recursion.

**Common causes**:
- Instance attributes shadowing descriptors (set on instance before descriptor)
- Forgetting to check `if instance is None` for class-level access
- Accessing the attribute name inside `__get__` causing recursive lookup

**Debug tips**:
```python
class MyDescriptor:
    def __get__(self, instance, owner):
        print(f"__get__ called: instance={instance}, owner={owner}")
        if instance is None:
            return self  # Class access
        # Store in instance dict with different key or use separate storage
        return instance.__dict__.get(self.name)
```

#### Metaclass `__new__` / `__init__` Order

**Symptom**: Changes in metaclass not appearing, or errors during class creation.

**Order of execution**:
1. `metaclass.__new__()` - Creates the class object
2. `metaclass.__init__()` - Initializes the class object
3. `class.__call__()` - Creates instances (calls `__new__` then `__init__`)

**Debug tips**:
```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class {name}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls
    
    def __init__(cls, name, bases, namespace):
        print(f"Initializing class {name}")
        super().__init__(name, bases, namespace)
```

#### Decorator Argument Handling

**Symptom**: `TypeError: decorated() takes X arguments but Y were given`

**Common pattern confusion**:
```python
# Decorator without arguments
@my_decorator
def func(): pass
# -> my_decorator(func)

# Decorator with arguments  
@my_decorator(arg=1)
def func(): pass
# -> my_decorator(arg=1)(func)  # Returns actual decorator
```

**Fix**: Use a factory pattern for parameterized decorators:
```python
def decorator_factory(arg):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            # use arg here
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
```

#### Iterator Exhaustion

**Symptom**: Iterator works once but is empty on second use.

**Cause**: Iterators are single-use. Once exhausted, they don't reset.

**Fix**: Convert to list if you need multiple passes, or recreate the iterator:
```python
# Iterator - single use
results = my_generator()
list(results)  # First pass works
list(results)  # Second pass empty!

# Solution: recreate or store as list
def get_results():
    return my_generator()  # Fresh iterator each call

# Or convert once
results_list = list(my_generator())  # Can iterate multiple times
```

#### Generator `send()` / `throw()` / `close()`

**Symptom**: `TypeError: can't send non-None value to a just-started generator`

**Cause**: First `send()` must be None to prime the generator.

**Fix**:
```python
def my_gen():
    value = yield "initial"
    while True:
        value = yield f"got: {value}"

gen = my_gen()
print(next(gen))        # Prime: prints "initial"
print(gen.send("hello"))  # Now works: prints "got: hello"
```

#### Context Manager Exception Handling

**Symptom**: Exceptions being swallowed or not properly handled in `with` blocks.

**Key rule**: Returning `True` from `__exit__` suppresses the exception.

**Debug template**:
```python
class MyContext:
    def __enter__(self):
        print("Entering")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting: exc_type={exc_type}")
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
            # Return True to suppress, None/False to propagate
        # Don't forget: cleanup happens whether or not exception occurred
```

#### Forgetting `return self` in `__enter__`

**Symptom**: `AttributeError: 'NoneType' object has no attribute 'X'` inside `with` block.

**Fix**: Always return self from `__enter__`:
```python
def __enter__(self):
    # setup code
    return self  # Required!
```

### General Debugging Tips

1. **Use `print()` liberally**: Trace through metaclass and descriptor execution
2. **Check MRO**: Use `Class.__mro__` to understand method resolution
3. **Inspect with `dir()`**: Use `dir(obj)` to see available attributes
4. **Read the CPython source**: Many built-in types demonstrate these patterns
5. **Start with working code**: Modify working examples rather than writing from scratch

## Hints for Medium and Hard Exercises

### Day 1: Descriptors

#### Problem 08: Read-Only Attribute (Medium)

**Hint 1 - Conceptual nudge**: You need to track which instances have had their value set. A dictionary mapping instances to values works, but consider: what should happen if someone accesses the attribute before setting it?

**Hint 2 - Structural plan**: 
- Use `__set_name__` to capture the attribute name
- Store values in a dictionary keyed by instance id or using `WeakKeyDictionary`
- Track a separate set of "already set" instances
- Raise `AttributeError` with a clear message on subsequent sets

**Hint 3 - Edge-case warning**: What about deletion? If `allow_deletion=True`, removing an instance from your "set" tracking allows it to be set again. Also, handle class access (`instance is None`) by returning `self`.

#### Problem 10: Weak Reference Descriptor (Hard)

**Hint 1 - Conceptual nudge**: `WeakKeyDictionary` is your friend here. It automatically removes entries when the key (instance) is garbage collected.

**Hint 2 - Structural plan**:
- Initialize a `WeakKeyDictionary` in `__init__`
- Store/retrieve values using `self._data[instance] = value`
- `__contains__` should check `instance in self._data`
- For `CachedComputation`, you need to store the computed value after first access

**Hint 3 - Edge-case warning**: `WeakKeyDictionary` cannot have its keys (instances) deleted directly - entries disappear when the instance is garbage collected. Test your `__delete__` carefully. Also, `CachedComputation` needs to handle the case where the compute function is passed as an argument vs used as a decorator.

### Day 2: Metaclasses

#### Problem 07: Abstract Method Enforcement Metaclass (Hard)

**Hint 1 - Conceptual nudge**: You need to inspect the class being created AND all its base classes. Look for methods marked with a special attribute that your `@MustImplement` decorator adds.

**Hint 2 - Structural plan**:
- `@MustImplement` should set a flag attribute on the function (e.g., `func._must_implement = True`)
- In `AbstractMeta.__new__`, collect all abstract methods from bases using `_get_abstract_methods`
- Check if the current class implements any of them
- If any abstracts remain unimplemented, raise `TypeError`

**Hint 3 - Edge-case warning**: A class with unimplemented abstract methods is itself abstract and should be allowed. Only concrete classes (no unimplemented abstracts) should raise errors. Consider how to mark a class as "explicitly abstract" if needed.

#### Problem 10: Auto-Serialization Metaclass (Hard)

**Hint 1 - Conceptual nudge**: You need to dynamically create methods (`to_dict`, `from_dict`, etc.) and attach them to the class. Use `staticmethod` or ordinary functions, then `setattr(cls, name, method)`.

**Hint 2 - Structural plan**:
- Detect fields from `__annotations__` and instance attributes
- Create `to_dict` that iterates over fields, calling `to_dict()` recursively for nested `Serializable` objects
- `from_dict` needs to instantiate the class and set attributes
- Respect `__serialize_fields__` and `__exclude_fields__`

**Hint 3 - Edge-case warning**: Nested serialization is tricky! When serializing, check if a value has a `to_dict` method. When deserializing, check if the field type is a `Serializable` subclass. Handle lists of serializable objects specially.

### Day 3: Decorators

#### Problem 10: Rate Limit Decorator (Hard)

**Hint 1 - Conceptual nudge**: This needs a decorator factory (parameterized decorator). You need to track call times per decorated function.

**Hint 2 - Structural plan**:
- Outer function takes `max_calls` and `period`, returns actual decorator
- Decorator receives the function, returns wrapper
- Wrapper maintains a list of call timestamps
- Before each call, remove timestamps older than `period`, then check count
- Use `time.time()` for timestamps

**Hint 3 - Edge-case warning**: Each decorated function needs its OWN call history. Don't use a shared list! Use a closure variable or function attribute. Also, preserve function metadata with `@functools.wraps`.

#### Problem 13: Requires Decorator (Medium)

**Hint 1 - Conceptual nudge**: You need to inspect the function's arguments at runtime. The `user` parameter could be positional or keyword.

**Hint 2 - Structural plan**:
- Use `inspect.signature` or `**kwargs` to find the `user` argument
- Check if `user.permissions` (a set) is a superset of required permissions
- Raise `PermissionError` if not

**Hint 3 - Edge-case warning**: What if `user` is not passed? The function signature might not even have it. Consider using `*args, **kwargs` in your wrapper and searching for `user` in kwargs or by position.

### Day 4: Dataclasses

#### Problem 04: Event Payload Model (Medium)

**Hint 1 - Conceptual nudge**: Factory methods are `@classmethod` that create and return instances with pre-filled values.

**Hint 2 - Structural plan**:
- Each factory method creates an `Event` with specific `event_type` and `payload`
- Use `cls(...)` or `Event(...)` to instantiate
- `from_dict` should use `**data` unpacking or explicit field assignment

**Hint 3 - Edge-case warning**: Auto-generated fields (UUID, timestamp) need default factories. When reconstructing from dict, you may want to preserve the original values rather than generating new ones.

### Day 5: Iterators and Generators

#### Problem 04: Tree Traversal Generator (Medium)

**Hint 1 - Conceptual nudge**: Recursive generators need `yield from` to delegate to sub-generators.

**Hint 2 - Structural plan**:
- Inorder: `yield from inorder(left)`, `yield value`, `yield from inorder(right)`
- Preorder: `yield value`, then left, then right
- Postorder: left, right, then `yield value`
- Level order: use a queue (collections.deque)

**Hint 3 - Edge-case warning**: Always check `if node is None` before recursing. For level order, remember to add children to the queue even if they're None (or check before adding).

### Day 6: Context Managers

#### Problem 05: Transaction Context Manager (Medium)

**Hint 1 - Conceptual nudge**: You need to buffer changes and only apply them on successful exit. If an exception occurs, discard the buffer.

**Hint 2 - Structural plan**:
- `__init__` stores the database reference
- `__enter__` returns self
- `set`/`delete` buffer changes in a local dict, not the database
- `__exit__` commits if no exception, rolls back if exception
- `get` checks buffer first, then database

**Hint 3 - Edge-case warning**: What happens if someone deletes a key that exists in the database, then tries to get it? You need a way to mark "deleted in transaction" vs "not touched". Consider using a sentinel value or separate tracking set.

#### Problem 06: Temporary Config Override (Medium)

**Hint 1 - Conceptual nudge**: You need to save the original values, set new ones, then restore originals on exit - whether successful or not.

**Hint 2 - Structural plan**:
- `__init__` takes config object and override dict
- `__enter__` saves original values, applies overrides, returns self
- `__exit__` restores all original values

**Hint 3 - Edge-case warning**: Make sure to restore even if an exception occurs. Use `try/finally` logic in `__exit__`. What if a key didn't exist originally? You might need to delete it during restoration.

## Weekly Project: Task Management System

Build a sophisticated task management system using advanced OOP features:

- **Custom task types**: Auto-registered via metaclass
- **Validation system**: Descriptors for type checking and constraints
- **Resource management**: Context managers for database/file operations
- **Mathematical operations**: Magic methods for task statistics and aggregations
- **Plugin architecture**: Metaclass-based auto-registration system
- **Audit logging**: Context managers for transaction safety

See [project/README.md](project/README.md) for full requirements.

### Project Structure

```
project/
├── README.md                    # Project requirements
├── starter/                     # Skeleton code with TODOs
├── reference_solution/          # Complete implementation
└── tests/                       # Project tests
```

## Key Concepts by Day

### Day 1: Descriptors
- The descriptor protocol: `__get__`, `__set__`, `__delete__`
- Data vs non-data descriptors
- Built-in descriptors: `property`, `staticmethod`, `classmethod`
- Implementing custom validators and converters
- Lazy evaluation with descriptors
- Weak references in descriptors to avoid cycles
- Storage strategies: instance dict vs descriptor dict

### Day 2: Metaclasses
- Understanding `type` as the default metaclass
- Creating custom metaclasses by subclassing `type`
- `__new__` vs `__init__` in metaclasses
- `__call__` for controlling instance creation
- Common patterns: Singleton, Registry, Validation
- Metaclass inheritance and conflict resolution
- `__init_subclass__` as a simpler alternative

### Day 3: Decorators
- Function decorators and `@` syntax
- Class decorators for modifying class behavior
- Decorators with arguments (decorator factories)
- Multiple decorators and execution order
- Preserving function metadata with `functools.wraps`
- Decorators for caching (`functools.lru_cache`)
- Decorators for class methods and properties

### Day 4: Dataclasses and `__slots__`
- Creating data classes with `@dataclass`
- Field customization with `field()`
- Comparison methods generation
- Immutable dataclasses (`frozen=True`)
- Inheritance with dataclasses
- `__slots__` for memory optimization
- When to use dataclasses vs regular classes

### Day 5: Iterators, Generators, and Custom Collections
- Iterator protocol: `__iter__` and `__next__`
- Creating generators with `yield`
- Generator expressions vs list comprehensions
- `yield from` for delegation
- `collections.abc` interfaces
- Custom container types
- Memory-efficient iteration patterns

### Day 6: Reflection, Introspection, and Context Managers
- Runtime object inspection with `type()`, `dir()`, `getattr()`
- Dynamic attribute handling: `__getattr__`, `__getattribute__`, `__setattr__`
- Context manager protocol: `__enter__` and `__exit__`
- `@contextmanager` decorator
- `contextlib` utilities
- Resource management patterns
- Exception handling in context managers

## Tips for Success

1. **Understand the call order** - Learn when `__new__`, `__init__`, `__get__`, etc. are called
2. **Use `print()` debugging** - Trace through metaclass and descriptor execution
3. **Read the CPython source** - Many built-in types demonstrate these patterns
4. **Start with working code** - Modify working examples rather than writing from scratch
5. **Know the alternatives** - Metaclasses vs class decorators vs `__init_subclass__`
6. **Profile before optimizing** - Don't add complexity without measurement
7. **Document your intent** - Advanced features can be confusing to readers

## Next Week

Week 6 covers Design Patterns:
- Creational patterns: Factory, Singleton, Builder
- Structural patterns: Adapter, Decorator, Facade, Proxy
- Behavioral patterns: Strategy, Observer, Command
- Pythonic implementations of classic patterns
- When to apply (and when to avoid) design patterns

---

**Total Exercises**: 51 problems  
**Total Tests**: ~878 tests (including project)  
**Estimated Time**: 15-30 hours depending on pace
