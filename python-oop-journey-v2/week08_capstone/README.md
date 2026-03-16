# Week 8 Capstone: Library Management System

## 🎯 Welcome to the Capstone

This is the **culmination of your Python OOP Journey**. The Library Management System demonstrates how all concepts from Weeks 1-7 come together in a production-quality application.

## What You're Building

A comprehensive library management system for a multi-branch library network that handles:

- **Books**: Catalog with multiple copies, search, and availability tracking
- **Members**: Registration, borrowing privileges, and account management
- **Loans**: Checkout, return, renewal workflows with due dates
- **Reservations**: Queue system for popular books
- **Fines**: Automated calculation with multiple policies

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pytest (for tests)

### First Steps

```bash
# Navigate to the week08_capstone directory
cd week08_capstone

# Run all tests to verify everything works
python -m pytest tests/ library_management_system/tests/ -v

# Run the demo to see the system in action
python demo.py

# Launch the interactive CLI
python -m library_management_system.interfaces.cli
```

### Interactive CLI

The system includes a full command-line interface:

```bash
# Start the CLI
python -c "from library_management_system.interfaces.cli import main; main()"
```

**CLI Menu:**
1. **Book Catalog** - Add books, search, view details
2. **Member Management** - Register members, view accounts
3. **Circulation** - Check out, return, renew books
4. **Reservations** - Place holds on books
5. **Fines & Payments** - View and process fines
6. **Reports** - View statistics
7. **Demo Data** - Load sample data for testing

## 📚 Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         Presentation Layer (CLI)        │
├─────────────────────────────────────────┤
│         Application Layer (Services)    │
│  - CatalogService                       │
│  - CirculationService                   │
│  - ReservationService                   │
│  - FineService                          │
├─────────────────────────────────────────┤
│         Domain Layer (Entities)         │
│  - Book, BookCopy                       │
│  - Member, Librarian                    │
│  - Loan, Reservation                    │
│  - Fine                                 │
├─────────────────────────────────────────┤
│       Infrastructure Layer (Repos)      │
│  - InMemoryBookRepository               │
│  - InMemoryMemberRepository             │
│  - InMemoryLoanRepository               │
└─────────────────────────────────────────┘
```

### Design Patterns Used

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Repository** | `repositories/` | Abstract data access for testability |
| **Strategy** | `services/catalog_service.py`, `services/fine_service.py` | Pluggable search and fine calculation |
| **Observer** | `services/circulation_service.py` | Event-driven notifications |
| **Factory** | `Loan.create()`, `Fine.create()` | Controlled entity creation |

## 📂 Project Structure

```
week08_capstone/
├── README.md                           # This file
├── demo.py                             # Run this to see the system in action
├── requirements.md                     # Functional requirements
├── domain_model.md                     # Entity relationships
├── architecture.md                     # System design documentation
├── testing_strategy.md                 # Testing approach
│
└── library_management_system/          # Main package
    ├── __init__.py
    │
    ├── domain/                         # Domain entities
    │   ├── book.py                     # Book, BookCopy
    │   ├── member.py                   # Member, Librarian
    │   ├── loan.py                     # Loan, Reservation
    │   ├── fine.py                     # Fine value object
    │   └── enums.py                    # Status enumerations
    │
    ├── repositories/                   # Repository implementations
    │   ├── book_repository.py          # BookRepository ABC + InMemory
    │   ├── member_repository.py        # MemberRepository ABC + InMemory
    │   └── loan_repository.py          # LoanRepository ABC + InMemory
    │
    ├── services/                       # Application services
    │   ├── catalog_service.py          # Book catalog with search strategies
    │   ├── circulation_service.py      # Checkout/return with event bus
    │   ├── reservation_service.py      # Reservation queue management
    │   └── fine_service.py             # Fine calculation with strategies
    │
    ├── interfaces/                     # User interfaces
    │   └── cli.py                      # Command-line interface
    │
    └── tests/                          # Service tests
        ├── test_integration.py         # End-to-end workflows
        ├── test_repositories.py        # Repository tests
        └── test_services.py            # Service layer tests

└── tests/                              # Domain tests
    ├── conftest.py                     # Test configuration
    └── test_domain.py                  # Domain entity tests (100 tests)
```

## 🎓 Learning Objectives

By completing this capstone, you will demonstrate mastery of:

### From Week 1-2 (Fundamentals)
- Proper use of type hints throughout
- Exception handling with custom exception hierarchies
- Working with datetime and Decimal for financial calculations

### From Week 3-4 (OOP Basics)
- Rich domain models with behavior in entities
- Encapsulation with private attributes
- Class methods as factory functions
- Properties for computed attributes

### From Week 5 (Advanced OOP)
- Dataclasses with validation (`__post_init__`)
- Frozen dataclasses for value objects
- ClassVar for class-level constants

### From Week 6 (Design Patterns)
- Repository pattern for persistence abstraction
- Strategy pattern for interchangeable algorithms
- Observer pattern for event handling
- Factory pattern for controlled creation

### From Week 7 (Real-World OOP)
- Layered architecture
- Separation of concerns
- Testable design

## ✅ How to Check Your Work

### Run All Tests

```bash
# All 151 tests should pass
python -m pytest tests/ library_management_system/tests/ -v
```

### Run the Demo

```bash
# See a complete workflow demonstration
python demo.py
```

### Test the CLI

```bash
# Launch interactive mode
python -c "from library_management_system.interfaces.cli import main; main()"

# Then try:
# 7. Demo: Setup Sample Data
# 1. Book Catalog > List all books
# 2. Member Management > List all members
# 3. Circulation > Checkout book
```

### Code Quality Checks

```bash
# Type checking (if mypy installed)
mypy library_management_system/

# Linting (if ruff installed)
ruff check library_management_system/
```

## 🔗 Connections to Previous Weeks

| This Week | Builds On |
|-----------|-----------|
| `Book.__post_init__` validation | Week 3: Class initialization |
| `Member.can_borrow()` method | Week 3: Methods and encapsulation |
| `Fine` frozen dataclass | Week 5: Immutable value objects |
| Repository pattern | Week 6: Design patterns |
| Strategy pattern for search | Week 6: Strategy pattern |
| Observer pattern for events | Week 6: Observer pattern |
| Layered architecture | Week 7: Real-world OOP |
| Comprehensive tests | Week 2, 7: Testing strategies |

## 🧪 Test Coverage

The capstone includes **151 tests** covering:

- **Domain layer (100 tests)**: Entity creation, validation, business rules
- **Repository layer (15 tests)**: Data persistence operations
- **Service layer (14 tests)**: Business workflows
- **Integration tests (22 tests)**: End-to-end scenarios

## 📝 Key Files to Study

1. **`domain/book.py`** - Rich entity with validation and relationships
2. **`domain/member.py`** - Complex business rules (can_borrow, fines)
3. **`repositories/book_repository.py`** - Repository pattern implementation
4. **`services/circulation_service.py`** - Observer pattern with EventBus
5. **`services/fine_service.py`** - Strategy pattern for fine calculation

## 🐛 Common Issues and Solutions

### Issue: Tests fail with import errors
**Solution**: Make sure you're running pytest from the `week08_capstone` directory or the repo root:
```bash
cd python-oop-journey-v2
python -m pytest week08_capstone/tests/ -v
```

### Issue: CLI shows wrong method names
**Solution**: The CLI has been updated to match the domain model. If you see errors about missing methods like `find_copy_by_id`, ensure you have the latest version.

### Issue: Demo script shows attribute errors
**Solution**: The demo has been updated to use correct attribute names (`isbn` not `id`, `member_id` not `id`, etc.)

## 📖 Documentation

- **`architecture.md`** - System architecture and patterns
- **`domain_model.md`** - Entity relationships and invariants
- **`requirements.md`** - Functional and non-functional requirements
- **`testing_strategy.md`** - Testing philosophy and organization

## 🎉 Capstone Completion Checklist

- [ ] All 151 tests pass
- [ ] Demo script runs without errors
- [ ] CLI launches and basic operations work
- [ ] You understand how all four design patterns are used
- [ ] You can trace a checkout workflow through all layers
- [ ] You can explain how this project connects to Weeks 1-7

## Next Steps

Congratulations on completing the Python OOP Journey! You now have:

1. **Strong fundamentals** (Weeks 1-2)
2. **OOP mastery** (Weeks 3-5)
3. **Design pattern knowledge** (Week 6)
4. **Real-world skills** (Week 7)
5. **A portfolio project** (Week 8)

Consider:
- Adding a database-backed repository
- Creating a web API with FastAPI
- Adding authentication to the CLI
- Packaging the project for PyPI

---

*Part of the Python OOP Journey v2 curriculum.*
