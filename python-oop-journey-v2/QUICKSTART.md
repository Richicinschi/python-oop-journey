# Quick Start Guide

Get started with Python OOP Journey v2 in 5 minutes.

## 1. Install Dependencies

```bash
# Navigate to the repository
cd python-oop-journey-v2

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## 2. Verify Setup

Run the test suite to ensure everything works:

```bash
pytest
```

You should see all tests passing. If not, check your Python version (3.10+) and installation.

## 3. Read Your First Theory Doc

**For absolute beginners:** Start with Week 0, Day 0:

```bash
# Or open in your editor/IDE
week00_getting_started/day00_welcome.md
```

**If you already know Python basics:** Start with Week 1, Day 1:

```bash
week01_fundamentals/day01_variables_types.md
```

## 4. Open Your First Exercise

**For Week 0 beginners:** Look at the first exercise file:

```bash
week00_getting_started/exercises/day04/problem_01_assign_and_print.py
```

**For Week 1:** Look at the first exercise file:

```bash
week01_fundamentals/exercises/day01/problem_01_calculate_sum.py
```

Try to implement the function. When stuck, check the solution in the corresponding `solutions/` directory.

## 5. Run Your First Test

Test a specific problem:

```bash
# Week 0 example
pytest week00_getting_started/tests/day04/test_problem_01_assign_and_print.py -v

# Week 1 example
pytest week01_fundamentals/tests/day01/test_problem_01_calculate_sum.py -v
```

## Recommended Daily Workflow

1. **Read** the day's theory document (15-20 minutes)
2. **Understand** the examples and concepts
3. **Attempt** exercises 01-03 (warm-up) without looking at solutions
4. **Check** solutions only when truly stuck
5. **Continue** with exercises 04-08 (core practice)
6. **Review** solutions for any you couldn't solve
7. **Optional**: Try stretch problems 09-10
8. **Run** tests to verify your understanding

## Week Structure

Each week follows this pattern:

| Day | Focus | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Theory + Warm-up exercises | 8-10 | Easy-Medium |
| Day 2 | Theory + Core practice | 8-10 | Medium |
| Day 3 | Theory + Core practice | 8-10 | Medium |
| Day 4 | Theory + Application | 6-10 | Medium-Hard |
| Day 5 | Theory + Application | 6-10 | Medium-Hard |
| Day 6 | Theory + Review/Stretch | 6-10 | Varied |
| End | Weekly Project | - | Integrated |

## Navigation Tips

- Use [INDEX.md](INDEX.md) for week-by-week navigation
- Each week has its own README with specific topics
- Solutions are organized to mirror exercises exactly
- Tests target solutions by default (repo stays green)

## Learning Tips

1. **Don't rush** - Quality over quantity
2. **Type out** solutions instead of copy-pasting
3. **Experiment** - Modify solutions to see what happens
4. **Take notes** in `daily_log.md`
5. **Track progress** in `progress_tracker.md`
6. **Ask why** - Understanding beats memorization

## Common Commands

```bash
# Run all tests
pytest

# Run specific week's tests
pytest week01_fundamentals/tests/ -v

# Run specific day's tests
pytest week01_fundamentals/tests/day01/ -v

# Run with coverage report
pytest --cov=week01_fundamentals --cov-report=term-missing

# Format code
black week01_fundamentals/

# Lint code
ruff check week01_fundamentals/
```

## Next Steps

1. **For absolute beginners:**
   - Read [week00_getting_started/README.md](week00_getting_started/README.md)
   - Start with [week00_getting_started/day00_welcome.md](week00_getting_started/day00_welcome.md)
   - Complete all 31 days before moving to Week 1

2. **If you already know Python:**
   - Read [week01_fundamentals/README.md](week01_fundamentals/README.md)
   - Start with [week01_fundamentals/day01_variables_types.md](week01_fundamentals/day01_variables_types.md)

3. Work through exercises at your own pace
4. Complete the weekly project when ready

Happy learning! 🚀
