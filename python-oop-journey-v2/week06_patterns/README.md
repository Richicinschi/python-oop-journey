# Week 6: Design Patterns

Master the essential design patterns that solve common object-oriented design problems. Learn patterns as tradeoffs and tools—not rules—understanding when to apply (and when to avoid) each pattern.

## Week Objective

By the end of this week, you will:
- Recognize common design problems that patterns solve
- Implement Creational patterns to control object instantiation
- Apply Structural patterns to compose classes and objects
- Use Behavioral patterns to manage communication between objects
- Understand the costs and benefits of each pattern
- Know when NOT to use a pattern (over-engineering avoidance)
- Build a flexible game framework using multiple patterns

## Prerequisites

- Completion of Weeks 1-5
- Solid understanding of classes, inheritance, and composition
- Familiarity with abstract base classes and interfaces
- Comfort with higher-order functions and decorators

## Daily Topics

| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Creational Patterns | 5 | Medium |
| Day 2 | Structural Patterns | 5 | Medium |
| Day 3 | Behavioral Patterns I | 5 | Hard |
| Day 4 | Behavioral Patterns II | 5 | Hard |
| Day 5 | Pattern Tradeoffs and Anti-Patterns | 5 | Medium |
| Day 6 | Patterns in a Mini Framework | 5 | Hard |

## File Structure

```
week06_patterns/
├── README.md                          # This file
├── day01_creational_patterns.md       # Day 1 theory: Factory, Builder, Singleton
├── day02_structural_patterns.md       # Day 2 theory: Adapter, Decorator, Facade
├── day03_behavioral_patterns_part_1.md # Day 3 theory: Observer, Strategy, Command
├── day04_behavioral_patterns_part_2.md # Day 4 theory: State, Template Method, Iterator
├── day05_pattern_tradeoffs.md         # Day 5 theory: When to use (and avoid) patterns
├── day06_patterns_in_a_small_framework.md # Day 6 theory: Pattern integration
├── exercises/                         # Your working area
│   ├── day01/                         # Day 1 exercises (5 files)
│   ├── day02/                         # Day 2 exercises (5 files)
│   ├── day03/                         # Day 3 exercises (5 files)
│   ├── day04/                         # Day 4 exercises (5 files)
│   ├── day05/                         # Day 5 exercises (5 files)
│   └── day06/                         # Day 6 exercises (5 files)
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
    ├── starter/                       # Starter code
    ├── reference_solution/            # Complete solution
    └── tests/                         # Project tests
```

## Start Here

New to Week 6? Begin with:

1. **Read** [Day 1 Theory](day01_creational_patterns.md) - Understanding Factory, Builder, Singleton, Prototype
2. **Attempt** [Day 1 Exercises](exercises/day01/) - Start with problem_01_factory_method_notifications.py
3. **Check your work** using the verification path below
4. **Review** the reference solution only when stuck

## How to Work Through This Week

### Daily Workflow

1. **Read the theory** document for the day (30-40 minutes)
   - Study the pattern intent and structure
   - Understand the problem each pattern solves
   - Review the class diagrams and examples

2. **Attempt exercises** in order:
   - Problems 01-03: Warm-up/foundational
   - Problems 04-05: Harder application

3. **Check solutions** only when stuck:
   - Try to solve each problem yourself first
   - If stuck for 20+ minutes, review the solution
   - Understand the approach, then implement yourself

4. **Run tests** to verify your work (see How to Check Your Work below)

### Recommended Pace

- **Intensive**: 1 day per calendar day (6 days)
- **Standard**: 2 days per week content (1-2 weeks)
- **Deep dive**: Take extra time on tradeoffs and when NOT to use patterns

## How to Check Your Work

### The Verification Path

Follow this sequence to verify your understanding without short-circuiting the learning process:

**Step 1: Read the Theory**
- Understand the pattern's intent (the WHY)
- Study the structure (the WHAT)
- Review the provided examples

**Step 2: Attempt the Exercise**
- Implement the pattern based on the exercise description
- Focus on the core pattern structure
- Don't worry about making it perfect

**Step 3: Run Manual Examples**
```python
# Add a simple test at the bottom of your exercise file
if __name__ == "__main__":
    # Create instances and test your implementation
    result = your_function()
    print(f"Result: {result}")
```

**Step 4: Read the Matching Test File**
- Tests show expected behavior without revealing implementation
- Located in `tests/dayXX/test_problem_XX_name.py`
- Understand what inputs produce what outputs
- Note edge cases tested

**Step 5: Run Tests Against Your Solution**
```bash
# Test a specific problem
pytest week06_patterns/tests/day01/test_problem_01_factory_method_notifications.py -v

# Test all problems for a day
pytest week06_patterns/tests/day01/ -v
```

**Step 6: Compare with Reference Solution**
- Only after you've made a genuine attempt
- Reference solutions are in `solutions/dayXX/`
- Focus on understanding differences, not copying

### Test Commands

```bash
# All Week 6 tests
pytest week06_patterns/tests/ -v

# Specific Day
pytest week06_patterns/tests/day01/ -v

# Specific Problem
pytest week06_patterns/tests/day01/test_problem_01_factory_method_notifications.py -v

# With Coverage
pytest week06_patterns/tests/ --cov=week06_patterns
```

## Weekly Project: Game Framework

Build a flexible game framework demonstrating multiple design patterns:

- **Factory pattern**: Create different enemy types dynamically
- **Observer pattern**: Event system for game state changes
- **Strategy pattern**: Swappable AI behaviors and combat algorithms
- **Command pattern**: Undoable player actions and replay system
- **State pattern**: Game states (Menu, Playing, Paused, GameOver)
- **Component pattern**: Entity-Component-System architecture

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

### Day 1: Creational Patterns
- **Factory Method**: Delegate instantiation to subclasses
- **Abstract Factory**: Create families of related objects
- **Builder**: Construct complex objects step by step
- **Singleton**: Ensure one instance (and when to avoid it)
- **Prototype**: Clone existing objects

### Day 2: Structural Patterns
- **Adapter**: Convert one interface to another
- **Decorator**: Add responsibilities dynamically
- **Facade**: Simplified interface to a complex subsystem
- **Composite**: Tree structures and part-whole hierarchies
- **Proxy**: Placeholder for expensive or remote objects

### Day 3: Behavioral Patterns I
- **Observer**: Publish-subscribe notification system
- **Strategy**: Family of interchangeable algorithms
- **Command**: Encapsulate requests as objects
- **State**: Alter behavior when state changes
- **Mediator**: Reduce direct object communication

### Day 4: Behavioral Patterns II
- **Template Method**: Algorithm skeleton with varying steps
- **Iterator**: Sequential access without exposing internals
- **Visitor**: Operations across object structures
- **Chain of Responsibility**: Pass requests along a chain
- **Memento**: Capture and restore object state

### Day 5: Pattern Tradeoffs and Anti-Patterns
- **YAGNI**: You Aren't Gonna Need It
- **KISS**: Keep It Simple, Stupid
- **Pattern abuse**: Using patterns without clear need
- **Complexity cost**: Every pattern adds indirection
- **When to refactor TO a pattern**: Emergent design
- **When to refactor AWAY from a pattern**: Simplification

### Day 6: Patterns in a Mini Framework
- **Plugin pattern**: Extensible systems
- **Event Bus**: Decoupled communication
- **Command Dispatcher**: Action routing
- **Component Registry**: Component management
- **State Persistence**: Save/load with Memento

## Stuck? Here Are Some Hints

### Getting Unstuck on Hard Exercises

For **MEDIUM** and **HARD** exercises (especially Days 3, 4, and 6), use this hint ladder:

**Hint 1: Conceptual Nudge**
- Re-read the pattern's intent in the theory doc
- Ask: "What problem does this pattern solve?"
- Identify which pattern component you need to focus on

**Hint 2: Structural Plan**
- Write out the class structure first
- Identify: What classes do I need? What are their relationships?
- Draw a simple diagram on paper

**Hint 3: Edge-Case Warning**
- What happens in the "empty" or "none" case?
- Did I handle the error/invalid state?
- Are my state transitions valid?

### Common Design Pattern Pitfalls

**Over-Engineering Simple Problems**
- Sign: Using a pattern when a simple function would suffice
- Fix: Start simple, add pattern only when pain emerges

**Wrong Pattern for the Problem**
- Sign: Force-fitting a favorite pattern to every problem
- Fix: Understand the problem first, then select pattern

**Tight Coupling in Supposedly Loose Patterns**
- Sign: Context class inspecting concrete strategy types
- Fix: Trust the interface; don't use isinstance checks

**Forgetting Pattern Intent, Focusing Only on Structure**
- Sign: Copying pattern structure without understanding why
- Fix: Re-read the intent; understand the problem being solved

**State Management in State Pattern**
- Sign: Context managing state transitions instead of states
- Fix: Let states decide their valid transitions

**Observer Memory Leaks**
- Sign: Observers not being garbage collected
- Fix: Use weak references or explicit detach

**Factory vs Builder Confusion**
- Sign: Using Builder when object creation is simple
- Fix: Factory for polymorphic creation; Builder for complex construction

### Debugging Tips for Pattern Exercises

1. **Print the flow**: Add print statements to see method calls
2. **Test components separately**: Test each class in isolation
3. **Check inheritance**: Ensure proper abstract method implementation
4. **Verify delegation**: Make sure context delegates to strategy/state
5. **Trace state transitions**: Log state changes for State pattern

## Tips for Success

1. **Learn the WHY, not just the HOW** - Patterns solve specific problems; understand the problem first
2. **Start simple** - Implement without patterns first, then refactor when pain points emerge
3. **Study real examples** - Look at Django, Flask, pytest source for pattern usage
4. **Draw diagrams** - Visualize object relationships and message flows
5. **Practice recognition** - Identify patterns in code you read
6. **Know the costs** - Every pattern adds complexity; make sure it's worth it

## Common Pitfalls

- **Pattern obsession** - Using patterns for patterns' sake
- **Premature abstraction** - Applying patterns before understanding the problem
- **Golden hammer** - Every problem looks like a nail for your favorite pattern
- **Naming confusion** - Calling any factory method "Factory Pattern"
- **Over-engineering** - Multiple patterns solving problems you don't have
- **Ignoring Python idioms** - Using Java-style patterns when Pythonic alternatives exist
- **State explosion** - Too many states in State pattern, too many strategies

## Next Week

Week 7 covers Real-World OOP:
- Working with real APIs and external libraries
- Testing strategies for object-oriented code
- Refactoring legacy code to OOP
- Performance considerations
- Documentation and type hints
- Packaging and distribution of OOP projects

---

**Total Exercises**: 30 problems  
**Total Tests**: ~280 tests (including project)  
**Estimated Time**: 8-20 hours depending on pace
