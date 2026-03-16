# Week 4: Intermediate OOP

Master inheritance, method overriding, abstract base classes, multiple inheritance, polymorphism, and composition while learning when to use inheritance versus composition.

## Week Objective

By the end of this week, you will:
- Understand inheritance and the "is-a" relationship
- Use `super()` to extend parent class behavior
- Create and implement abstract base classes
- Navigate multiple inheritance and the Method Resolution Order (MRO)
- Design effective mixin classes
- Apply polymorphism and duck typing
- Know when to use inheritance versus composition
- Build a hierarchical class system for the weekly project

## Prerequisites

- Completion of Week 3 (OOP Basics)
- Solid understanding of classes, objects, and encapsulation
- Familiarity with methods, properties, and magic methods

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Inheritance Basics | 8 | Medium |
| Day 2 | Method Overriding and `super()` | 6 | Medium |
| Day 3 | Abstract Base Classes | 6 | Medium-Hard |
| Day 4 | Multiple Inheritance and MRO | 6 | Hard |
| Day 5 | Polymorphism and Duck Typing | 6 | Medium |
| Day 6 | Composition vs Inheritance | 6 | Medium-Hard |

## File Structure

```
week04_oop_intermediate/
├── README.md                          # This file
├── day01_inheritance_basics.md        # Day 1 theory: Inheritance Basics
├── day02_method_overriding_super.md   # Day 2 theory: Method Overriding and super()
├── day03_abstract_base_classes.md     # Day 3 theory: Abstract Base Classes
├── day04_multiple_inheritance_mro.md  # Day 4 theory: Multiple Inheritance and MRO
├── day05_polymorphism.md              # Day 5 theory: Polymorphism and Duck Typing
├── day06_composition_vs_inheritance.md # Day 6 theory: Composition vs Inheritance
├── exercises/                         # Your working area
│   ├── day01/                         # Day 1 exercises (8 files)
│   ├── day02/                         # Day 2 exercises (6 files)
│   ├── day03/                         # Day 3 exercises (6 files)
│   ├── day04/                         # Day 4 exercises (6 files)
│   ├── day05/                         # Day 5 exercises (6 files)
│   └── day06/                         # Day 6 exercises (7 files)
├── solutions/                         # Reference solutions
│   ├── day01/                         # Day 1 solutions
│   ├── day02/                         # Day 2 solutions
│   ├── day03/                         # Day 3 solutions
│   ├── day04/                         # Day 4 solutions
│   ├── day05/                         # Day 5 solutions
│   └── day06/                         # Day 6 solutions
├── tests/                             # Test suite
│   ├── day01/                         # Day 1 tests
│   ├── day02/                         # Day 2 tests
│   ├── day03/                         # Day 3 tests
│   ├── day04/                         # Day 4 tests
│   ├── day05/                         # Day 5 tests
│   └── day06/                         # Day 6 tests
└── project/                           # Weekly project
    ├── README.md                      # Project documentation
    ├── starter/                       # Starter code with TODOs
    ├── reference_solution/            # Complete solution
    └── tests/                         # Project tests
```

## Start Here

**New to this week?** Follow this path:

1. **Read** → `day01_inheritance_basics.md` - Learn the core inheritance concepts
2. **Code** → `exercises/day01/problem_01_vehicle_hierarchy.py` - Your first exercise
3. **Test** → Run `pytest week04_oop_intermediate/tests/day01/test_problem_01_vehicle_hierarchy.py -v`
4. **Repeat** → Continue through all Day 1 exercises
5. **Progress** → Move to Day 2 theory, then Day 2 exercises
6. **Project** → After Day 3, start the [Animal Shelter project](project/README.md)

## How to Work Through This Week

### Daily Workflow

1. **Read the theory** document for the day (20-30 minutes)
   - Study the concepts and code examples
   - Run the example code in a Python REPL
   - Understand the inheritance diagrams

2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-05: Core practice
   - Problems 06+: Advanced concepts and applications

3. **Check your work** (see "How to Check Your Work" below)

4. **Review solutions** only when stuck:
   - Try to solve each problem yourself first
   - If stuck for 15+ minutes, review the solution
   - Understand the approach, then implement yourself

### Recommended Pace

- **Intensive**: 1 day per calendar day (6 days)
- **Standard**: 2-3 days per week content (2 weeks)
- **Deep dive**: Take extra time on MRO, polymorphism, and composition patterns

## Weekly Project: Animal Shelter Management System

Build an animal shelter management system using all Week 4 concepts:

- **Inheritance**: Animal type hierarchy (Dog, Cat, Bird, Rabbit inherit from Animal)
- **Method Overriding & super()**: Customizing base behaviors for specific animal types
- **Abstract Base Classes**: Enforcing interfaces for animals and staff members
- **Multiple Inheritance**: Mixins for logging and timestamps
- **Polymorphism**: Processing different animal types uniformly through common interfaces
- **Composition**: Enclosure management (Enclosure HAS-A animals, not IS-A animals)

See [project/README.md](project/README.md) for full requirements.

### Project Structure

```
project/
├── README.md                    # Project requirements
├── starter/                     # Skeleton code with TODOs
│   ├── animal.py
│   ├── staff.py
│   ├── enclosure.py
│   ├── adoption.py
│   └── shelter.py
├── reference_solution/          # Complete implementation
│   ├── animal.py
│   ├── staff.py
│   ├── enclosure.py
│   ├── adoption.py
│   └── shelter.py
└── tests/                       # Project tests
    └── test_shelter.py
```

## How to Check Your Work

### Recommended Verification Path

Follow this sequence to verify your solutions effectively:

**1. Read the Theory First**
- Study the day's theory document thoroughly
- Understand the concepts and code examples
- Run the example code in a Python REPL
- Pay attention to inheritance diagrams

**2. Attempt the Exercise Honestly**
- Read the problem statement carefully
- Look at the provided examples in the docstring
- Implement the TODO sections one at a time
- **Don't look at the solution yet!**

**3. Run Manual Examples**
Test your code interactively before running the full test suite:

```python
# Example: Test in Python REPL
from week04_oop_intermediate.exercises.day01.problem_01_vehicle_hierarchy import Car, ElectricCar

# Test basic functionality
car = Car("Toyota", "Camry", 2023)
print(car.get_info())  # Should print formatted info

# Test inheritance
electric = ElectricCar("Tesla", "Model 3", 2023, 75)
print(electric.get_info())  # Should include battery info
print(isinstance(electric, Car))  # Should be True
```

**4. Read the Tests**
Before running tests, read them to understand expected behavior:

```bash
# View test file to understand expectations
cat week04_oop_intermediate/tests/day01/test_problem_01_vehicle_hierarchy.py
```

Tests often clarify edge cases not fully explained in the exercise.

**5. Run the Tests**

```bash
# Test specific problem (fastest feedback)
pytest week04_oop_intermediate/tests/day01/test_problem_01_vehicle_hierarchy.py -v

# Test all problems for a day
pytest week04_oop_intermediate/tests/day01/ -v

# Test entire week (comprehensive)
pytest week04_oop_intermediate/tests/ -v
```

**6. Compare with Reference Solution (After Attempt)**
Only look at solutions after a genuine attempt:

```bash
# Compare your approach with reference
cat week04_oop_intermediate/solutions/day01/problem_01_vehicle_hierarchy.py
```

Focus on understanding different approaches, not copying code.

### Self-Check Questions

For each exercise, verify:
- [ ] Does my code handle the basic cases shown in examples?
- [ ] Does it handle edge cases mentioned in requirements?
- [ ] Are class relationships correct (is-a vs has-a)?
- [ ] Did I use `super()` appropriately when extending parent behavior?
- [ ] Are type hints complete and correct?
- [ ] Do all tests pass?

### Debugging Tips

**Inspect Classes Interactively:**
```python
from week04_oop_intermediate.exercises.day01.problem_01_vehicle_hierarchy import ElectricCar

# See method resolution order
print(ElectricCar.__mro__)

# Get detailed help
help(ElectricCar)

# Check attributes
print(dir(ElectricCar))
```

**Understand Test Failures:**
When a test fails, Python shows:
- Which test failed
- What was expected
- What was actually returned
- Line number where assertion failed

Read this output carefully—it tells you exactly what's wrong.

## Key Concepts by Day

### Day 1: Inheritance Basics
- Base classes and derived classes
- The "is-a" relationship
- `isinstance()` and `issubclass()`
- Method overriding basics
- Inheriting attributes and methods
- Single inheritance patterns

### Day 2: Method Overriding and `super()`
- Method overriding mechanics
- Using `super()` to call parent methods
- `super().__init__()` for parent initialization
- Extending vs replacing parent behavior
- Cooperative multiple inheritance with `super()`

### Day 3: Abstract Base Classes
- Abstract Base Classes (ABCs) with `abc` module
- `@abstractmethod` decorator
- Abstract properties
- Concrete vs abstract classes
- Interface definition and enforcement
- When to use ABCs vs regular inheritance

### Day 4: Multiple Inheritance and MRO
- Multiple inheritance syntax
- Method Resolution Order (MRO)
- The diamond problem
- `__mro__` attribute and `mro()` method
- Mixin classes
- Designing cooperative hierarchies

### Day 5: Polymorphism and Duck Typing
- Polymorphism as "many forms"
- Inheritance-based polymorphism
- Duck typing: "If it walks like a duck..."
- Protocols and structural subtyping
- Polymorphic collections and functions
- Strategy pattern

### Day 6: Composition vs Inheritance
- "is-a" vs "has-a" relationships
- When to prefer composition
- Strategy pattern using composition
- Plugin architectures with composition
- Repository pattern
- Refactoring from inheritance to composition

## Tips for Success

1. **Draw diagrams** - Sketch class hierarchies to visualize inheritance
2. **Use `help()` and `__mro__`** - Inspect class relationships interactively
3. **Start simple** - Build single inheritance before attempting multiple
4. **Prefer composition** - Not everything needs inheritance
5. **Test incrementally** - Verify parent classes work before testing children
6. **Read error messages** - Python's MRO errors are informative
7. **Think before inheriting** - Ask "is this truly an is-a relationship?"

## Common Pitfalls

- **Forgetting `super().__init__()`** - Parent attributes not initialized
- **Method shadowing** - Accidentally overriding parent methods
- **Diamond problem confusion** - Not understanding MRO in complex hierarchies
- **Overusing inheritance** - Using "is-a" when "has-a" is better
- **Mixing super() styles** - Inconsistent use of `super()` vs direct parent calls
- **Abstract class instantiation** - Trying to instantiate ABCs directly
- **Missing abstract methods** - Forgetting to implement all required methods
- **Breaking polymorphism** - Using excessive isinstance checks
- **Tight coupling** - Deep inheritance hierarchies that are hard to change

## Debugging Guide for Common Week 4 Issues

### Inheritance Hierarchy Confusion

**Symptom:** Unsure which class inherits from which, or why a method isn't being found.

**Debug:**
```python
# Check the Method Resolution Order
print(YourClass.__mro__)

# Check if an object is an instance of a class
print(isinstance(obj, ParentClass))

# Check if a class is a subclass of another
print(issubclass(ChildClass, ParentClass))
```

### Method Resolution Order (MRO) Surprises

**Symptom:** The wrong method is being called in multiple inheritance.

**Debug:**
```python
# See the full MRO
print(YourClass.__mro__)

# Or use the mro() method
print(YourClass.mro())

# Check which method would be called
print(YourClass.__mro__[1].method_name)  # First parent's method
```

**Common Fix:** Ensure parent classes use `super()` properly for cooperative inheritance.

### super() Usage Mistakes

**Symptom:** `AttributeError` or parent initialization not happening.

**Common mistakes:**
```python
# WRONG - Missing parentheses
super.__init__()  # This won't raise an error but does nothing!

# WRONG - Calling parent's __init__ directly (breaks MRO)
ParentClass.__init__(self)

# CORRECT
super().__init__()  # Python 3 style
```

**Debug:** Add print statements to track initialization:
```python
def __init__(self):
    print(f"Before super: {self.__class__.__name__}")
    super().__init__()
    print(f"After super: {self.__class__.__name__}")
```

### Abstract Method Implementation Errors

**Symptom:** `TypeError: Can't instantiate abstract class YourClass with abstract methods method_name`

**Debug:**
```python
from abc import ABC, abstractmethod

class MyABC(ABC):
    @abstractmethod
    def required_method(self): pass

# This will fail
try:
    obj = MyABC()
except TypeError as e:
    print(e)  # Shows which methods are missing

# Check what methods need implementation
print(MyABC.__abstractmethods__)
```

**Common Fix:** Ensure all methods decorated with `@abstractmethod` are implemented in concrete classes.

### Multiple Inheritance Diamond Problem

**Symptom:** Parent class `__init__` called multiple times, or attributes overwritten unexpectedly.

**Example diamond:**
```
    User
   /    \
Admin  PowerUser
   \    /
 SuperAdmin
```

**Debug:** Use `super()` properly in all classes:
```python
class User:
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)  # Important!

class Admin(User):
    def __init__(self, admin_level=1, **kwargs):
        self.admin_level = admin_level
        super().__init__(**kwargs)  # Continues the chain

class SuperAdmin(Admin, PowerUser):
    def __init__(self, name, admin_level=2, power_level=2):
        super().__init__(  # Only need one super() call
            name=name,
            admin_level=admin_level,
            power_level=power_level
        )
```

### Composition vs Inheritance Decision Paralysis

**When to use inheritance:**
- Clear "is-a" relationship (Dog IS-A Animal)
- Want to share implementation
- Child can truly substitute for parent (Liskov Substitution)

**When to use composition:**
- "has-a" relationship (Car HAS-A Engine)
- Want to change behavior at runtime
- Need to avoid tight coupling
- Multiple behaviors that can be mixed and matched

**The "Favor Composition" heuristic:**
```python
# Inheritance approach (more rigid)
class ElectricCar(Car): ...

# Composition approach (more flexible)
class Car:
    def __init__(self, power_source):
        self.power_source = power_source  # Can be Battery, GasTank, etc.
```

### Inspecting Object State

**Debug object attributes:**
```python
obj = YourClass()

# See all attributes
print(obj.__dict__)

# See all methods and attributes
print(dir(obj))

# Check specific attribute exists
print(hasattr(obj, 'attribute_name'))

# Get attribute with default
print(getattr(obj, 'maybe_missing', 'default_value'))
```

## Next Week

Week 5 covers Advanced OOP:
- Magic methods and operator overloading
- Context managers and `with` statements
- Descriptors and property decorators
- Metaclasses
- Class and static methods deep dive
- Design patterns in Python

---

**Total Exercises**: 38 problems  
**Total Tests**: ~240 tests (including project)  
**Estimated Time**: 6-20 hours depending on pace
