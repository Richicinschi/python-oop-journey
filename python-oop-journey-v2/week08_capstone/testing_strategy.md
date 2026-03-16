# Library Management System - Testing Strategy

## Overview

This document outlines the comprehensive testing approach for the Library Management System capstone. The goal is to ensure correctness, maintainability, and confidence in the codebase through multiple levels of testing.

## Testing Philosophy

1. **Test Behavior, Not Implementation**: Focus on what the code does, not how it does it
2. **Fast Feedback**: Unit tests should run in milliseconds
3. **Deterministic**: Tests should produce the same results every time
4. **Readable**: Tests document expected behavior
5. **Maintainable**: Tests evolve with the codebase

## Test Pyramid

```
        /\
       /  \      E2E Tests (CLI Scenarios)
      /----\         ~5% of tests
     /      \
    /--------\   Integration Tests (Services + Repos)
   /          \      ~15% of tests
  /------------\
 /              \  Unit Tests (Domain, Value Objects)
/________________\     ~80% of tests
```

## Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_domain.py           # Domain entity tests
├── test_services.py         # Service layer tests
├── test_repositories.py     # Repository implementation tests
└── test_cli.py              # CLI integration tests
```

## Unit Testing

### Domain Entity Tests

**Scope:** Book, BookCopy, Member, Loan, Reservation, Fine

**Coverage Goals:**
- 100% branch coverage for business logic
- All validation rules tested
- State transitions verified
- Edge cases covered

**Example Test Categories:**

```python
# Book Tests
def test_book_creation_with_valid_data(): ...
def test_book_creation_rejects_empty_title(): ...
def test_book_creation_rejects_invalid_isbn(): ...
def test_book_adds_copy_to_catalog(): ...

# Member Tests
def test_member_can_borrow_when_active(): ...
def test_member_cannot_borrow_when_suspended(): ...
def test_member_cannot_exceed_loan_limit(): ...
def test_member_cannot_borrow_with_high_fines(): ...

# Loan Tests
def test_loan_creation_sets_correct_due_date(): ...
def test_loan_can_be_renewed_when_eligible(): ...
def test_loan_cannot_be_renewed_when_reserved(): ...
def test_loan_cannot_be_renewed_more_than_twice(): ...
```

### Value Object Tests

**Scope:** Fine, enums, small value types

**Characteristics:**
- Immutable behavior
- Equality based on values, not identity
- Validation at construction

**Example:**
```python
def test_fine_is_immutable_after_creation(): ...
def test_fine_equality_based_on_amount_and_reason(): ...
def test_fine_rejects_negative_amount(): ...
```

## Integration Testing

### Service Layer Tests

**Scope:** CirculationService, ReservationService, FineService

**Approach:**
- Use in-memory repositories
- Test service + repository integration
- Verify data consistency

**Example:**
```python
def test_checkout_creates_loan_and_updates_copy_status(
    circulation_service, book_repo, member_repo, loan_repo
):
    # Arrange
    member = create_active_member()
    book = create_available_book()
    member_repo.save(member)
    book_repo.save(book)
    
    # Act
    loan = circulation_service.checkout(book.copies[0].barcode, member.member_id)
    
    # Assert
    assert loan.status == LoanStatus.ACTIVE
    assert book.copies[0].status == CopyStatus.BORROWED
    assert member.active_loan_count == 1
```

### Repository Tests

**Scope:** InMemoryRepository implementations

**Test Matrix:**
- Save and retrieve entity
- Update existing entity
- Delete entity
- List all entities
- Find by criteria

**Example:**
```python
def test_repository_saves_and_retrieves_book(): ...
def test_repository_updates_existing_book(): ...
def test_repository_returns_none_for_missing_id(): ...
def test_repository_lists_all_saved_books(): ...
```

## Acceptance Testing

### Use Case Tests

**Scope:** End-to-end scenarios

**Format:** Given-When-Then

**Examples:**

```python
def test_member_borrows_book_and_returns_it():
    """Complete borrowing workflow."""
    # Given: Active member and available book
    # When: Librarian checks out book to member
    # Then: Book shows as borrowed
    # When: Member returns book
    # Then: Book shows as available, no fines

def test_overdue_book_generates_fine():
    """Fine calculation workflow."""
    # Given: Book checked out 20 days ago
    # When: Book is returned today
    # Then: Fine is calculated at $0.50/day

def test_reservation_queue_is_respected():
    """Reservation fulfillment workflow."""
    # Given: Book borrowed by Member A
    # And: Member B and C have reservations
    # When: Member A returns book
    # Then: Member B is notified, book held for them
```

## Fixtures and Test Data

### Shared Fixtures (conftest.py)

```python
@pytest.fixture
def book_factory():
    """Factory for creating test books."""
    def _factory(**overrides):
        return Book(
            isbn=overrides.get("isbn", "978-0-123456-78-9"),
            title=overrides.get("title", "Test Book"),
            authors=overrides.get("authors", ("Test Author",)),
            publisher=overrides.get("publisher", "Test Publisher"),
            publication_year=overrides.get("publication_year", 2024),
            genre=overrides.get("genre", "Fiction"),
        )
    return _factory

@pytest.fixture
def active_member():
    """Create an active member ready to borrow."""
    return Member(
        member_id="MEM001",
        name="Test Member",
        email="test@example.com",
        status=MembershipStatus.ACTIVE,
    )

@pytest.fixture
def in_memory_repositories():
    """Set up clean in-memory repositories."""
    return {
        "books": InMemoryBookRepository(),
        "members": InMemoryMemberRepository(),
        "loans": InMemoryLoanRepository(),
    }
```

### Fixture Scopes

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `book_factory` | Session | Immutable factory function |
| `active_member` | Function | Fresh member for each test |
| `in_memory_repositories` | Function | Clean state for each test |

## Test Data Builders

```python
class BookBuilder:
    """Builder for creating test books with defaults."""
    
    def __init__(self):
        self.isbn = "978-0-123456-78-9"
        self.title = "Default Title"
        self.authors = ("Default Author",)
        self.publisher = "Default Publisher"
        self.publication_year = 2024
        self.genre = "Fiction"
        self.copies = []
    
    def with_isbn(self, isbn: str) -> "BookBuilder":
        self.isbn = isbn
        return self
    
    def with_copy(self, barcode: str) -> "BookBuilder":
        self.copies.append(BookCopy(barcode=barcode, book_isbn=self.isbn))
        return self
    
    def build(self) -> Book:
        book = Book(...)
        for copy in self.copies:
            book.add_copy(copy)
        return book
```

## Coverage Goals

| Component | Target Coverage | Priority |
|-----------|-----------------|----------|
| Domain entities | 95%+ | Critical |
| Value objects | 100% | Critical |
| Service layer | 90%+ | High |
| Repositories | 85%+ | High |
| CLI | 70%+ | Medium |

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test File
```bash
python -m pytest tests/test_domain.py -v
```

### With Coverage
```bash
python -m pytest tests/ --cov=library_management_system --cov-report=term-missing
```

### Specific Test
```bash
python -m pytest tests/test_domain.py::test_book_creation -v
```

### Fail Fast (stop on first failure)
```bash
python -m pytest tests/ -x
```

## Test Naming Conventions

- Test functions: `test_<what_is_being_tested>_<condition>()`
- Test classes: `Test<ComponentBeingTested>`
- Descriptive names that explain the scenario

**Good:**
- `test_member_cannot_borrow_when_suspended()`
- `test_loan_renewal_extends_due_date_by_14_days()`
- `test_fine_calculation_uses_tiered_policy_correctly()`

**Bad:**
- `test_member()`
- `test_loan()`
- `test1()`

## Assertions and Matchers

### Prefer Explicit Assertions

```python
# Good
assert loan.due_date == checkout_date + timedelta(days=14)
assert member.active_loan_count == 0
assert book.copies[0].status == CopyStatus.AVAILABLE

# Avoid
assert loan is not None  # Too vague
assert len(something) > 0  # What are we checking?
```

### Custom Matchers (if needed)

```python
class IsOverdue:
    """Matcher for overdue loans."""
    def __eq__(self, loan):
        return loan.status == LoanStatus.OVERDUE

def test_overdue_loan_is_marked_correctly():
    loan = create_overdue_loan()
    assert loan == IsOverdue()
```

## Mocking and Patching

### When to Mock

- External dependencies (email service, file system)
- Time-based operations (use freezegun)
- Randomness (seed RNG)

### When NOT to Mock

- In-memory repositories (use real implementations)
- Domain entities (test real behavior)
- Value objects (test real behavior)

### Example: Time-Based Testing

```python
from freezegun import freeze_time

@freeze_time("2024-01-15")
def test_due_date_is_14_days_from_checkout():
    loan = create_loan(checkout_date=date.today())
    assert loan.due_date == date(2024, 1, 29)

@freeze_time("2024-02-01")
def test_overdue_loan_calculates_fine_correctly():
    # Loan due 2024-01-15, today is 2024-02-01 (17 days overdue)
    loan = create_loan(due_date=date(2024, 1, 15))
    fine = calculate_fine(loan)
    assert fine.amount == Decimal("8.50")  # 17 * $0.50
```

## Continuous Integration

### Pre-Commit Checks

```bash
# Run before committing
pytest tests/ -x --tb=short
```

### Pre-Push Checks

```bash
# Run before pushing
pytest tests/ --cov=library_management_system --cov-fail-under=80
```

## Debugging Failed Tests

### Verbose Output
```bash
pytest tests/test_domain.py -v --tb=long
```

### PDB on Failure
```bash
pytest tests/ --pdb
```

### Show Locals
```bash
pytest tests/ --showlocals
```

## Test Documentation

Each test file should have a module docstring:

```python
"""Tests for the domain layer.

This module contains tests for:
- Book and BookCopy entities
- Member and Librarian entities
- Loan and Reservation entities
- Fine value objects

All tests use in-memory storage and frozen time where applicable.
"""
```

## Maintenance Guidelines

1. **Keep Tests Fast**: Each test should complete in < 100ms
2. **Keep Tests Independent**: No shared mutable state between tests
3. **Update Tests with Code**: Tests are documentation; keep them current
4. **Delete Obsolete Tests**: Remove tests for removed features
5. **Refactor Test Code**: Apply the same standards to test code as production code

---

*Testing is not about finding bugs—it's about preventing them.*
