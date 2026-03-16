# Python OOP Journey v2 - Repo-Level Agent Guide

This is the repo-local agent guide for the `python-oop-journey-v2` curriculum.

## Quick Reference

- **Project**: Python OOP learning curriculum (Weeks 1-8)
- **Parent Workspace**: `c:\Users\digitalnomad\Documents\oopkimi`
- **Current Status**: Week 1 Complete ✅

## Working Rules

### Structural Rules (Non-Negotiable)

1. **One problem per file** - No giant exercise files
2. **Valid Python module names** - Use `problem_XX_name.py`, never `01_name.py`
3. **No wildcard imports** - Use explicit imports only
4. **No sys.path hacks** - Imports must work naturally
5. **Tests target solutions** - Keeps the committed repo green

### Directory Structure

```
weekXX_topic/
  __init__.py
  README.md
  dayXX_topic.md              # Theory document
  exercises/dayXX/            # Exercise files with TODOs
  solutions/dayXX/            # Complete reference solutions
  tests/dayXX/                # Tests (import from solutions)
  project/                    # Weekly project
```

### File Naming

- Theory: `day01_variables_types.md`
- Problems: `problem_01_calculate_sum.py`
- Tests: `test_problem_01_calculate_sum.py`

### Import Patterns

Tests should import:
```python
from week01_fundamentals.solutions.day01.problem_01_calculate_sum import calculate_sum
```

### Pedagogical Rules

- Week 1-2: No OOP required for solutions
- Week 3+: Introduce classes cleanly
- Week 5+: Advanced features (descriptors, metaclasses)
- Week 6: Design patterns explicitly
- Week 8: Capstone integration

## When Resuming Work

1. Check `../memory.md` for current status
2. Read this file for working rules
3. Run `pytest` to verify current state
4. Check `ROADMAP.md` for what's next

## Handoff Notes

- **Week 1**: ✅ Complete with 513 tests passing
- **Week 2**: ⏳ Ready to implement
- **Root pytest**: Configured to run Week 1 tests

## Testing Commands

```bash
# Run all tests
pytest

# Run specific week
pytest week01_fundamentals/tests/

# Run specific day
pytest week01_fundamentals/tests/day01/

# Run with coverage
pytest --cov=week01_fundamentals
```

## See Also

- `../memory.md` - Project-wide status and handoff
- `../recreate_project_prompt.txt` - Full rebuild specification
- `ROADMAP.md` - Current roadmap
- `README.md` - Project overview
