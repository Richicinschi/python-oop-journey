# Day 1: API Design with Classes

## Learning Objectives

By the end of this day, you will be able to:

1. Design clean, intuitive APIs using Python classes
2. Implement the Repository pattern for data access abstraction
3. Create fluent interfaces for method chaining
4. Build response wrappers that provide metadata and context
5. Design hierarchical configuration systems with validation
6. Apply pagination patterns for handling large datasets

---

## Key Concepts

### 1. Why API Design Matters

Good API design is about creating interfaces that are:
- **Intuitive**: Users can guess how to use it correctly
- **Consistent**: Similar operations work in similar ways
- **Discoverable**: Users can find what they need
- **Safe**: Hard to misuse, easy to debug

| Quality | Good API | Bad API |
|---------|----------|---------|
| Naming | `user.activate()` | `user.set_status(1)` |
| Discovery | Tab-completion friendly | Magic strings everywhere |
| Safety | Type hints, validation | Silent failures |
| Composability | Chainable methods | God objects |

### 2. The Repository Pattern

The Repository pattern abstracts data access, allowing your application to work with domain objects without knowing how they're stored.

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')

class Repository(ABC, Generic[T, K]):
    """Abstract base for repositories."""
    
    @abstractmethod
    def get(self, id_: K) -> T | None:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update existing entity."""
        pass
    
    @abstractmethod
    def delete(self, id_: K) -> bool:
        """Delete entity by ID."""
        pass
```

**Benefits:**
- Swappable storage (in-memory, database, API)
- Testable code (mock repositories)
- Single point of change for data access logic

### 3. Fluent Interface (Method Chaining)

Fluent interfaces make code read like natural language by returning `self` from methods.

```python
from __future__ import annotations
from typing import Self

class QueryBuilder:
    """Example of fluent interface."""
    
    def __init__(self) -> None:
        self._table = ""
        self._where: list[str] = []
        self._order_by: list[str] = []
        self._limit: int | None = None
    
    def from_table(self, table: str) -> Self:
        self._table = table
        return self
    
    def where(self, condition: str) -> Self:
        self._where.append(condition)
        return self
    
    def order_by(self, field: str, direction: str = "ASC") -> Self:
        self._order_by.append(f"{field} {direction}")
        return self
    
    def limit(self, n: int) -> Self:
        self._limit = n
        return self
    
    def build(self) -> str:
        query = f"SELECT * FROM {self._table}"
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Usage reads like English
query = (QueryBuilder()
    .from_table("users")
    .where("age > 18")
    .where("active = true")
    .order_by("name")
    .limit(10)
    .build())
```

### 4. Response Wrappers

Wrappers add context and metadata to API responses without cluttering domain data.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class APIResponse(Generic[T]):
    """Generic API response wrapper."""
    data: T
    success: bool = True
    message: str = ""
    pagination: PaginationInfo | None = None
    meta: dict[str, str] | None = None

@dataclass
class PaginationInfo:
    """Pagination metadata."""
    page: int
    per_page: int
    total: int
    total_pages: int
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        return self.page > 1
```

### 5. Pagination Patterns

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Page:
    """A single page of results."""
    items: list[dict]
    page_number: int
    total_pages: int
    total_items: int
    
    @property
    def is_first(self) -> bool:
        return self.page_number == 1
    
    @property
    def is_last(self) -> bool:
        return self.page_number >= self.total_pages

class PaginatedClient:
    """Client that handles pagination automatically."""
    
    def __init__(self, api_client: APIClient) -> None:
        self._client = api_client
    
    def get_all_pages(self, endpoint: str) -> Iterator[Page]:
        """Yield all pages from the endpoint."""
        page_num = 1
        while True:
            page = self._client.get_page(endpoint, page_num)
            yield page
            if page.is_last:
                break
            page_num += 1
    
    def get_all_items(self, endpoint: str) -> Iterator[dict]:
        """Flatten all pages into individual items."""
        for page in self.get_all_pages(endpoint):
            yield from page.items
```

### 6. Hierarchical Configuration

```python
from __future__ import annotations
from typing import Any

class ConfigSection:
    """A section in the configuration hierarchy."""
    
    def __init__(self, name: str, data: dict[str, Any]) -> None:
        self._name = name
        self._data = data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if key in self._data:
            return self._data[key]
        return default
    
    def require(self, key: str) -> Any:
        """Get a required configuration value."""
        if key not in self._data:
            raise ConfigError(f"Required key '{key}' missing in section '{self._name}'")
        return self._data[key]
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a nested configuration section."""
        if name not in self._data:
            raise ConfigError(f"Section '{name}' not found in '{self._name}'")
        if not isinstance(self._data[name], dict):
            raise ConfigError(f"'{name}' in '{self._name}' is not a section")
        return ConfigSection(name, self._data[name])

class Configuration:
    """Root configuration object with validation."""
    
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self._validate()
    
    def _validate(self) -> None:
        """Override to implement validation logic."""
        pass
    
    def get_section(self, name: str) -> ConfigSection:
        """Get a top-level configuration section."""
        if name not in self._data:
            raise ConfigError(f"Section '{name}' not found")
        return ConfigSection(name, self._data[name])
```

---

## Common Mistakes

### 1. Breaking Fluent Interface

```python
# Wrong - method doesn't return self
class BadBuilder:
    def set_name(self, name: str) -> None:
        self.name = name  # Returns None!

# Right - returns self for chaining
class GoodBuilder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self
```

### 2. Exposing Implementation Details

```python
# Wrong - caller knows it's a dict
user._data["name"]  # Direct access to internal structure

# Right - abstracted access
user.get_name()  # Implementation can change
```

### 3. Inconsistent Return Types

```python
# Wrong - sometimes returns None, sometimes raises
repo.get(id)  # Might return None
repo.get(id)  # Might raise NotFoundError

# Right - consistent behavior
repo.get(id)        # Always returns Optional[T]
repo.get_or_raise(id)  # Always returns T or raises
```

### 4. Not Validating Early

```python
# Wrong - validation scattered throughout
config = Config(raw_data)  # Accepts anything
# Validation happens lazily, causing confusing errors

# Right - validate at construction
config = Config(raw_data)  # Validates immediately, clear error messages
```

---

## Connection to Exercises

Today's exercises implement real-world API design patterns:

| Problem | Pattern | Skills Practiced |
|---------|---------|------------------|
| 01. Pagination API Client | Iterator + Wrapper | Auto-pagination, lazy loading |
| 02. Repository Service Layer | Repository Pattern | Data access abstraction, testing |
| 03. Fluent Query Builder | Fluent Interface | Method chaining, readable APIs |
| 04. Response Wrapper | Generic Wrapper | Metadata, context, type safety |
| 05. Configuration Object | Hierarchical Config | Validation, nested access |

---

## Weekly Project Connection

The Week 7 project is the **Personal Finance Tracker**. Day 1's patterns are essential because:

- **Repository Pattern**: Abstracts data access for accounts, transactions, and categories
- **Fluent Interface**: Builds complex financial queries naturally (e.g., filtering transactions by date range, category, and amount)
- **Response Wrappers**: Adds metadata to query results like pagination info for transaction history
- **Configuration**: Manages database paths, currency settings, and alert thresholds
- **Pagination**: Handles large transaction histories gracefully when generating reports

---

## Quick Reference

```python
from __future__ import annotations
from typing import Self, Generic, TypeVar

# Repository Pattern
class Repository(ABC, Generic[T, K]):
    @abstractmethod
    def get(self, id_: K) -> T | None: pass

# Fluent Interface
class Builder:
    def step(self) -> Self:
        return self

# Response Wrapper
@dataclass
class Response(Generic[T]):
    data: T
    meta: dict[str, Any]

# Pagination
class Paginator:
    def __iter__(self) -> Iterator[Page]: pass

# Configuration
class Config:
    def get(self, key: str) -> Any: pass
    def require(self, key: str) -> Any: pass
```

---

## Next Steps

After completing today's exercises:
1. Compare the patterns and their use cases
2. Think about how you'd combine them in a real API client
3. Preview Day 2: **Testing and Mocking**
