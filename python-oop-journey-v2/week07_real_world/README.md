# Week 7: Real-World OOP

Apply object-oriented programming to realistic systems with professional practices including API design, comprehensive testing, refactoring techniques, and performance awareness.

## Week Objective

By the end of this week, you will:
- Design clean, intuitive APIs that follow object-oriented principles
- Write effective tests for object-oriented code using pytest
- Refactor procedural code into well-structured OOP designs
- Build data processing pipelines using OOP patterns
- Implement service-oriented architectures with clear interfaces
- Understand performance implications of OOP design choices
- Apply type hints and documentation best practices

## Prerequisites

- Completion of Weeks 1-6
- Solid understanding of classes, inheritance, and composition
- Familiarity with design patterns and their applications
- Experience with abstract base classes and interfaces
- Comfort with decorators and context managers

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | API Design | 5 | Medium-Hard |
| Day 2 | Testing OOP Code | 5 | Medium |
| Day 3 | Refactoring to OOP | 5 | Medium-Hard |
| Day 4 | Data Processing with OOP | 5 | Medium |
| Day 5 | Service Architecture | 5 | Hard |
| Day 6 | Performance and Optimization | 5 | Medium-Hard |

## File Structure

```
week07_real_world/
├── README.md                        # This file
├── day01_api_design_with_classes.md # Day 1 theory: Designing clean APIs
├── day02_testing_oop_code.md        # Day 2 theory: Testing strategies
├── day03_refactoring_procedural_to_oop.md  # Day 3 theory: Refactoring techniques
├── day04_data_processing_with_objects.md   # Day 4 theory: Data pipelines with OOP
├── day05_service_oriented_oop.md    # Day 5 theory: Service-oriented design
├── day06_performance_and_optimization.md   # Day 6 theory: Performance considerations
├── exercises/                       # Your working area
│   ├── day01/                       # Day 1 exercises (5 problems)
│   ├── day02/                       # Day 2 exercises (5 problems)
│   ├── day03/                       # Day 3 exercises (5 problems)
│   ├── day04/                       # Day 4 exercises (5 problems)
│   ├── day05/                       # Day 5 exercises (5 problems)
│   └── day06/                       # Day 6 exercises (5 problems)
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

New to this week? Start with **Day 1**:

1. **Read**: [Day 1 Theory - API Design](day01_api_design_with_classes.md) (30-40 minutes)
2. **Exercise**: [Day 1 Problem 1](exercises/day01/problem_01_pagination_api_client.py)
3. **Test**: Run `pytest week07_real_world/tests/day01/test_problem_01_pagination_api_client.py -v`

## How to Check Your Work

### The Verification Path

Follow this sequence to verify your solutions:

1. **Read the theory** for the day before attempting problems
2. **Attempt the exercise** without looking at the solution
3. **Run the provided examples** manually (if any)
4. **Read the matching test file** to understand expected behavior
5. **Run the tests** for your specific problem:
   ```bash
   # Test a specific problem
   pytest week07_real_world/tests/day01/test_problem_01_pagination_api_client.py -v
   
   # Test all problems for a day
   pytest week07_real_world/tests/day01/ -v
   ```
6. **Only after a real attempt**, compare against the reference solution

### Running Tests

```bash
# All Week 7 Tests
pytest week07_real_world/tests/ -v

# Specific Day
pytest week07_real_world/tests/day01/ -v

# Specific Problem
pytest week07_real_world/tests/day01/test_problem_01_pagination_api_client.py -v

# With Coverage
pytest week07_real_world/tests/ --cov=week07_real_world

# Project Tests
pytest week07_real_world/project/tests/ -v
```

### Test Output Guide

- **PASSED**: Your solution works correctly
- **FAILED**: Review the assertion message to understand what's wrong
- **ERROR**: Usually indicates missing imports or syntax errors

## Weekly Project: Personal Finance Tracker

Build a comprehensive personal finance tracking system that demonstrates real-world OOP practices:

- **Clean API design**: Intuitive interfaces for accounts, transactions, and budgets
- **Comprehensive testing**: Unit, integration, and property-based tests
- **Data processing**: Import and analyze financial data from multiple sources
- **Service architecture**: Separate concerns into distinct service layers
- **Type safety**: Full type hints and validation
- **Performance optimization**: Efficient queries and data structures

See [project/README.md](project/README.md) for full requirements.

### Project Structure

```
project/
├── README.md                    # Project requirements
├── starter/                     # Skeleton code with TODOs
├── reference_solution/          # Complete implementation
└── tests/                       # Project tests
```

## Recommended Workflow

### Daily Workflow

1. **Read the theory** document for the day (30-40 minutes)
   - Study the concepts and professional practices
   - Review the code examples and patterns
   - Understand real-world application contexts

2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-05: Core practice and advanced application

3. **Check solutions** only when stuck:
   - Try to solve each problem yourself first
   - If stuck for 20+ minutes, review the solution
   - Understand the approach, then implement yourself

4. **Run tests** to verify your work (see How to Check Your Work above)

### Recommended Pace

- **Intensive**: 1 day per calendar day (6 days)
- **Standard**: 2 days per week content (1-2 weeks)
- **Deep dive**: Take extra time on testing strategies and refactoring patterns

## Key Concepts by Day

### Day 1: API Design
- **Interface design**: Creating intuitive, discoverable APIs
- **Fluent interfaces**: Method chaining for readable code
- **Builder pattern**: Step-by-step object construction
- **Immutability**: Safe, predictable objects
- **Validation**: Input sanitization and error handling

### Day 2: Testing OOP Code
- **Unit testing**: Testing classes and methods in isolation
- **Test fixtures**: Setup and teardown with pytest
- **Mocking**: Isolating dependencies with unittest.mock
- **Parametrized tests**: Testing multiple scenarios efficiently
- **Contract-style testing**: Ensuring implementation consistency

### Day 3: Refactoring to OOP
- **Code smells**: Identifying procedural patterns
- **Extract class**: Moving related data and behavior together
- **Replace conditional with polymorphism**: Strategy pattern application
- **Dependency injection**: Flexible, testable designs
- **Legacy code**: Safe refactoring techniques

### Day 4: Data Processing with OOP
- **Pipeline pattern**: Chaining data transformations
- **Iterator protocol**: Processing large datasets lazily
- **ETL design**: Extract, transform, load patterns
- **Validation pipelines**: Data quality assurance
- **Error handling**: Graceful degradation in pipelines

### Day 5: Service Architecture
- **Service layer**: Separating business logic from infrastructure
- **Repository pattern**: Abstracting data access
- **Dependency injection**: Loose coupling between components
- **Interface segregation**: Client-specific interfaces
- **Permission policies**: Flexible authorization systems

### Day 6: Performance and Optimization
- **Profiling**: Identifying bottlenecks with cProfile
- **Memory optimization**: `__slots__`, caching strategies
- **Algorithmic complexity**: Big-O considerations in OOP
- **Lazy evaluation**: Deferred computation patterns
- **Trade-offs**: Readability vs performance

## Hints and Debugging Support

### Getting Unstuck

For Medium and Hard exercises, look for inline hints in the exercise files following this format:

```python
# HINT 1 (Conceptual): Think about what pattern would let you chain methods...
# HINT 2 (Structural): You'll need a method that returns self for chaining...
# HINT 3 (Edge Case): Don't forget to validate the direction parameter...
```

### Common Debugging Pitfalls in Real-World OOP

#### 1. API Design Mistakes
- **Breaking fluent interface**: Forgetting to return `self` from chainable methods
- **Inconsistent return types**: Sometimes returning None, sometimes raising exceptions
- **Exposing implementation details**: Direct access to internal data structures
- **Missing validation**: Late validation causing confusing errors

**Fix**: Always return `Self` from fluent methods, validate at construction time, use properties for computed values.

#### 2. Testing Coverage Gaps
- **Testing implementation details**: Testing private methods instead of public behavior
- **Over-mocking**: Mocking too many layers makes tests brittle
- **Missing edge cases**: Empty inputs, boundary values, invalid states
- **Shared mutable state**: Tests that depend on execution order

**Fix**: Test behavior not structure, mock only external dependencies, test boundary conditions, use fixtures for isolation.

#### 3. Refactoring Risks
- **Refactoring without tests**: Changing code without safety net
- **Big bang changes**: Rewriting everything at once
- **Preserving procedural API**: Creating classes that just wrap functions
- **Over-engineering**: Adding unnecessary abstraction

**Fix**: Write tests first, refactor incrementally, migrate callers gradually, keep it simple.

#### 4. Service Boundary Confusion
- **Anemic services**: Services that are just proxies to repositories
- **God services**: Single service handling too many responsibilities
- **Hidden dependencies**: Creating repositories inside methods
- **Leaky abstractions**: Exposing internal details to callers

**Fix**: Services should encapsulate business logic, keep services focused, inject dependencies, maintain clean interfaces.

## Tips for Success

1. **Design for readability first** - Clear code is easier to optimize and maintain
2. **Write tests as you go** - Don't leave testing for the end
3. **Refactor incrementally** - Small, safe changes reduce risk
4. **Measure before optimizing** - Profile to find real bottlenecks
5. **Use type hints consistently** - They serve as documentation and catch errors
6. **Study real codebases** - Django, FastAPI, and pandas demonstrate these patterns
7. **Document intent, not mechanics** - Explain why, not just what

## Common Pitfalls

- **Testing implementation details** - Test behavior, not internal structure
- **Over-mocking** - Mock at the right abstraction level
- **Premature optimization** - Don't optimize without profiling first
- **God objects** - Classes that know too much and do too much
- **Tight coupling** - Services that depend on concrete implementations
- **Ignoring edge cases** - Real-world data is messy and incomplete
- **Leaky abstractions** - Implementation details exposed in interfaces
- **Feature creep** - Adding features without clear requirements

## Next Week

Week 8 is the Capstone Project:
- Build a complete, production-ready application
- Apply all concepts from Weeks 1-7
- Design your own architecture and APIs
- Implement comprehensive tests and documentation
- Present a portfolio-ready project

---

**Total Exercises**: 30 problems  
**Total Tests**: ~930 tests (including project)  
**Estimated Time**: 10-24 hours depending on pace
