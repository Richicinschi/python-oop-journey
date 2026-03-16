# Library Management System - Architecture

## Overview

The Library Management System follows a **Layered Architecture** with clear separation of concerns between the domain logic, application services, and infrastructure concerns. This architecture supports testability, maintainability, and future extensibility.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                         (CLI)                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│              (Services, Workflows, DTOs)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                             │
│         (Entities, Value Objects, Domain Services)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                        │
│            (Repositories, External Services)                 │
└─────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer

**Location:** `library_management_system/domain/`

**Responsibilities:**
- Define domain entities and their behavior
- Enforce business rules and invariants
- Define value objects
- Provide domain services for complex operations

**Key Components:**
- `Book`, `BookCopy` - Catalog management
- `Member`, `Librarian` - User management
- `Loan`, `Reservation` - Circulation management
- `Fine` - Financial penalties

**Design Principles:**
- No external dependencies
- Pure business logic
- Rich domain models (behavior in entities)
- Immutable value objects

### 2. Application Layer

**Location:** `library_management_system/services/`

**Responsibilities:**
- Orchestrate domain objects to fulfill use cases
- Coordinate transactions
- Apply cross-cutting concerns (logging, validation)
- Translate between domain and presentation

**Key Components:**
- `CirculationService` - Checkout, checkin, renew workflows
- `ReservationService` - Reservation lifecycle management
- `FineService` - Fine calculation and payment
- `CatalogService` - Book catalog operations

**Design Principles:**
- Thin services that delegate to domain
- No business logic (only coordination)
- Repository abstraction for persistence

### 3. Infrastructure Layer

**Location:** `library_management_system/repositories/`

**Responsibilities:**
- Data persistence and retrieval
- External service integration
- File I/O operations

**Key Components:**
- `BookRepository` (interface + implementations)
- `MemberRepository` (interface + implementations)
- `LoanRepository` (interface + implementations)
- `InMemoryRepository` - For testing
- `JsonFileRepository` - For file persistence

**Design Principles:**
- Repository pattern abstracts storage
- Interface segregation
- Dependency inversion (depend on abstractions)

### 4. Presentation Layer

**Location:** `library_management_system/cli/`

**Responsibilities:**
- User interface (command-line)
- Input validation and parsing
- Output formatting
- Command routing

**Key Components:**
- `LibraryCLI` - Main CLI interface
- `CommandParser` - Argument parsing
- `OutputFormatter` - Result display

## Design Patterns

### 1. Repository Pattern

**Purpose:** Abstract data access for testability and flexibility.

**Implementation:**
```python
from abc import ABC, abstractmethod

class Repository[T](ABC):
    @abstractmethod
    def get(self, id: str) -> T | None: ...
    
    @abstractmethod
    def save(self, entity: T) -> None: ...
    
    @abstractmethod
    def delete(self, id: str) -> None: ...
    
    @abstractmethod
    def list_all(self) -> list[T]: ...
```

**Benefits:**
- Test in-memory, run with files
- Swap storage without changing business logic
- Unit tests don't require database setup

### 2. Strategy Pattern

**Purpose:** Make fine calculation algorithms interchangeable.

**Implementation:**
```python
class FinePolicy(ABC):
    @abstractmethod
    def calculate(self, days_overdue: int) -> Decimal: ...

class StandardFinePolicy(FinePolicy): ...
class TieredFinePolicy(FinePolicy): ...
class GracePeriodFinePolicy(FinePolicy): ...
```

**Benefits:**
- Add new fine policies without modifying existing code
- Configure policies per book type or member category
- Test policies in isolation

### 3. Factory Pattern

**Purpose:** Encapsulate object creation with validation.

**Implementation:**
```python
class BookFactory:
    @staticmethod
    def create(isbn: str, title: str, authors: list[str]) -> Book:
        # Validate ISBN format
        # Validate authors list
        # Create and return Book
        ...
```

**Benefits:**
- Centralize validation logic
- Ensure invariants at creation
- Support different creation scenarios

### 4. Observer Pattern

**Purpose:** Notify interested parties of domain events.

**Implementation:**
```python
class EventBus:
    def subscribe(self, event_type: type, handler: Callable): ...
    def publish(self, event: DomainEvent): ...

@dataclass
class BookReturned:
    book_isbn: str
    member_id: str
    copy_barcode: str
```

**Benefits:**
- Decouple notification logic from business logic
- Support multiple notification channels (email, SMS, in-app)
- Easy to add new event types

## Package Structure

```
library_management_system/
├── __init__.py              # Package initialization
├── domain/                  # Domain layer
│   ├── __init__.py
│   ├── book.py             # Book and BookCopy entities
│   ├── member.py           # Member and Librarian entities
│   ├── loan.py             # Loan and Reservation entities
│   ├── fine.py             # Fine value object
│   └── enums.py            # Domain enumerations
├── interfaces/              # Abstract contracts
│   ├── __init__.py
│   ├── repositories.py     # Repository interfaces
│   └── policies.py         # Policy strategy interfaces
├── services/                # Application layer
│   ├── __init__.py
│   ├── circulation.py      # CirculationService
│   ├── reservation.py      # ReservationService
│   └── fine_service.py     # FineService
├── repositories/            # Infrastructure layer
│   ├── __init__.py
│   ├── memory.py           # InMemoryRepository
│   └── json_repo.py        # JsonFileRepository
└── cli/                     # Presentation layer
    ├── __init__.py
    └── main.py             # CLI entry point
```

## Dependency Rules

```
Domain Layer ◄── Application Layer ◄── Infrastructure Layer
     ▲                    ▲
     │                    │
     └─────────uses───────┘
              (via interfaces)

Presentation Layer ◄── Application Layer
```

**Rules:**
1. Domain has no dependencies on other layers
2. Application depends only on Domain and Interfaces
3. Infrastructure implements Interfaces
4. Presentation depends on Application
5. Dependencies flow inward (Domain is the core)

## Error Handling Strategy

### Domain Exceptions

```python
class DomainError(Exception):
    """Base class for domain errors."""
    pass

class ValidationError(DomainError):
    """Invalid data or state."""
    pass

class BusinessRuleError(DomainError):
    """Business rule violated."""
    pass

class NotFoundError(DomainError):
    """Entity not found."""
    pass
```

### Usage Pattern

```python
def checkout_book(self, copy_id: str, member_id: str) -> Loan:
    member = self._member_repo.get(member_id)
    if member is None:
        raise NotFoundError(f"Member {member_id} not found")
    
    if not member.can_borrow():
        raise BusinessRuleError("Member cannot borrow books")
    
    # ... continue checkout
```

## Testing Strategy

### Unit Tests
- Test domain entities in isolation
- Mock repository interfaces
- Fast, deterministic

### Integration Tests
- Test service layer with real repositories
- Test repository implementations
- Verify data persistence

### Acceptance Tests
- Test use cases end-to-end
- CLI command testing
- Scenario-based tests

## Performance Considerations

### In-Memory Repositories
- O(1) lookups using dictionaries
- Suitable for catalogs up to 100K items
- No I/O overhead

### Future Extensions
- Database-backed repositories (SQLite, PostgreSQL)
- Caching layer for frequently accessed data
- Indexing for complex queries

## Security Considerations

### Input Validation
- Validate all external inputs at boundaries
- Sanitize user-provided data
- Type coercion with error handling

### Authorization
- Librarian roles with permission checks
- Member action validation
- Audit logging for sensitive operations

## Extensibility Points

1. **New Repository Types**: Implement `Repository` interface
2. **New Fine Policies**: Implement `FinePolicy` interface
3. **New Notifications**: Subscribe to domain events
4. **New CLI Commands**: Add to command parser
5. **New Reports**: Extend reporting service

## Technology Stack

- **Language**: Python 3.10+
- **Testing**: pytest, pytest-cov
- **Type Checking**: mypy-compatible type hints
- **Formatting**: black-compatible style
- **Linting**: ruff-compatible code

---

*Architecture follows Domain-Driven Design and Clean Architecture principles.*
