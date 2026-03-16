# Week 7 Project: Personal Finance Tracker

## Goal

Build a comprehensive personal finance tracking system that demonstrates real-world OOP practices. By completing this project, you will have implemented a full application with domain models, repositories, services, and reporting - similar to production code you'd find in professional Python applications.

## What You'll Build

A command-line personal finance tracker supporting:

- **Multiple Account Types**: Checking, savings, credit cards, investments
- **Transaction Management**: Income, expenses, transfers with categorization
- **Budget Tracking**: Set budgets by category with alert notifications
- **Financial Reports**: Monthly summaries, category breakdowns, spending trends
- **Data Persistence**: JSON-based storage for accounts and transactions

## Files That Matter Most

```
project/
├── README.md                    # This file - start here
├── starter/                     # Your working directory
│   ├── account.py              # Account domain model
│   ├── category.py             # Transaction categories
│   ├── transaction.py          # Transaction records and transfers
│   ├── budget.py               # Budget tracking
│   └── report.py               # Report generation
├── reference_solution/          # Complete implementation (check after trying)
│   ├── account.py
│   ├── category.py
│   ├── transaction.py
│   ├── budget.py
│   ├── report.py
│   ├── repositories.py         # Repository pattern implementation
│   └── services.py             # Business logic services
└── tests/
    └── test_finance_tracker.py # Test suite to verify your solution
```

## Public Contract

### Domain Models

Your implementation must provide these classes with the specified interfaces:

#### Account
```python
class Account:
    id: str                    # Unique identifier (auto-generated)
    name: str                  # Account name (required)
    account_type: AccountType  # CHECKING, SAVINGS, CREDIT, INVESTMENT
    balance: float            # Current balance
    currency: str             # ISO code (default: "USD")
    created_at: datetime      # Creation timestamp
    is_active: bool           # Account status
    
    def deposit(self, amount: float) -> bool: ...
    def withdraw(self, amount: float) -> bool: ...
    def can_withdraw(self, amount: float) -> bool: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> Account: ...
```

#### Transaction
```python
class Transaction:
    id: str                   # Unique identifier
    account_id: str          # Reference to account
    category_id: str         # Reference to category
    amount: float           # Transaction amount (positive)
    type: TransactionType   # INCOME, EXPENSE, TRANSFER
    description: str        # Transaction description
    date: date             # Transaction date
    tags: list[str]        # Optional organization tags
    
    def is_income(self) -> bool: ...
    def is_expense(self) -> bool: ...
    def is_transfer(self) -> bool: ...
    def signed_amount(self) -> float: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> Transaction: ...
```

#### Category
```python
class Category:
    id: str                  # Unique identifier
    name: str               # Category name (required)
    type: CategoryType      # INCOME or EXPENSE
    color: str             # Hex color code
    icon: str              # Icon identifier
    is_active: bool        # Category status
    
    def is_income(self) -> bool: ...
    def is_expense(self) -> bool: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> Category: ...
```

#### Budget
```python
class Budget:
    id: str                  # Unique identifier
    category_id: str        # Category this budget tracks
    amount: float          # Budget limit (positive)
    period: BudgetPeriod   # MONTHLY, WEEKLY, YEARLY
    alert_threshold: float # Percentage to trigger alert (0-100)
    is_active: bool        # Budget status
    
    def is_alert_triggered(self, spent: float) -> bool: ...
    def get_remaining(self, spent: float) -> float: ...
    def get_utilization_percentage(self, spent: float) -> float: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> Budget: ...
```

### Repositories (Required for Full Implementation)

```python
class InMemoryRepository(Generic[T]):
    def get(self, id: str) -> T | None: ...
    def get_all(self) -> list[T]: ...
    def add(self, entity: T) -> T: ...
    def update(self, entity: T) -> None: ...
    def delete(self, id: str) -> bool: ...
    def count(self) -> int: ...
    def clear(self) -> None: ...

class AccountRepository(InMemoryRepository[Account]):
    def get_by_type(self, account_type: AccountType) -> list[Account]: ...
    def get_active(self) -> list[Account]: ...
    def get_total_balance(self) -> float: ...
    def save_to_file(self, filepath: str) -> None: ...
    def load_from_file(self, filepath: str) -> None: ...

class TransactionRepository(InMemoryRepository[Transaction]):
    def get_by_account(self, account_id: str) -> list[Transaction]: ...
    def get_by_category(self, category_id: str) -> list[Transaction]: ...
    def get_by_date_range(self, start: date, end: date) -> list[Transaction]: ...
    def get_by_type(self, type_: TransactionType) -> list[Transaction]: ...

class CategoryRepository(InMemoryRepository[Category]):
    def get_by_type(self, category_type: CategoryType) -> list[Category]: ...
    def find_by_name(self, name: str) -> Category | None: ...

class BudgetRepository(InMemoryRepository[Budget]):
    def get_by_category(self, category_id: str) -> Budget | None: ...
    def get_active_budgets(self) -> list[Budget]: ...
```

### Services (Required for Full Implementation)

```python
class FinanceService:
    def create_account(self, name: str, account_type: str, 
                       initial_balance: float = 0.0) -> Account: ...
    def get_account(self, account_id: str) -> Account | None: ...
    def create_category(self, name: str, type_: str, 
                        color: str = "", icon: str = "") -> Category: ...
    def record_transaction(self, account_id: str, category_id: str,
                          amount: float, type_: str, 
                          description: str = "") -> Transaction: ...
    def transfer_between_accounts(self, from_id: str, to_id: str,
                                  amount: float, description: str = "") -> tuple[Transaction, Transaction]: ...
    def generate_monthly_summary(self, year: int, month: int) -> MonthlySummary: ...
    def export_transactions_to_csv(self, filepath: str) -> bool: ...

class BudgetService:
    def create_budget(self, category_id: str, amount: float,
                      period: str = "monthly", 
                      alert_threshold: float = 80.0) -> Budget: ...
    def calculate_spent_for_budget(self, budget: Budget) -> float: ...
    def check_budget_alerts(self) -> list[BudgetAlert]: ...
```

## How to Approach the Starter

### Step-by-Step Implementation Guide

#### Phase 1: Domain Models (Days 1-2)

Start with the simplest components - the data models:

1. **Account** (`starter/account.py`)
   - Implement the dataclass with validation in `__post_init__`
   - Add deposit/withdraw logic (remember credit accounts work differently!)
   - Implement to_dict/from_dict for serialization
   - Run tests: `pytest project/tests/test_finance_tracker.py::TestAccount -v`

2. **Category** (`starter/category.py`)
   - Implement the dataclass
   - Add is_income/is_expense methods
   - Implement serialization

3. **Transaction** (`starter/transaction.py`)
   - Implement Transaction dataclass
   - signed_amount() should return positive for income, negative for expense
   - Implement Transfer class for account-to-account transfers
   - Transfer creates two transactions (outgoing and incoming)

4. **Budget** (`starter/budget.py`)
   - Implement Budget dataclass
   - Add alert threshold logic
   - Implement utilization calculations

#### Phase 2: Repositories (Day 3-4)

Add data persistence layer:

1. **InMemoryRepository** - Generic base with CRUD operations
2. **Specialized Repositories** - Account, Transaction, Category, Budget
3. **Add filtering methods** - get_by_type, get_by_date_range, etc.
4. **Add persistence** - save_to_file/load_from_file using JSON

#### Phase 3: Services (Day 5)

Implement business logic:

1. **FinanceService** - Orchestrates accounts, transactions, categories
2. **BudgetService** - Handles budget tracking and alerts
3. **Connect everything** - Services use repositories, repositories store models

#### Phase 4: Reports (Day 6)

Add reporting capabilities:

1. **Monthly Summary** - Income, expenses, net flow
2. **Category Breakdown** - Spending by category
3. **CSV Export** - Export transactions for external use

### Verification at Each Phase

```bash
# Test domain models
pytest project/tests/test_finance_tracker.py::TestAccount -v
pytest project/tests/test_finance_tracker.py::TestCategory -v
pytest project/tests/test_finance_tracker.py::TestTransaction -v
pytest project/tests/test_finance_tracker.py::TestBudget -v

# Test repositories
pytest project/tests/test_finance_tracker.py::TestInMemoryRepository -v
pytest project/tests/test_finance_tracker.py::TestAccountRepository -v

# Test services
pytest project/tests/test_finance_tracker.py::TestFinanceService -v
pytest project/tests/test_finance_tracker.py::TestBudgetService -v

# All tests
pytest project/tests/ -v
```

## Final Behavior

When complete, you should be able to:

```python
from project.starter.services import FinanceService, BudgetService
from project.starter.repositories import (
    AccountRepository, TransactionRepository, CategoryRepository, BudgetRepository
)

# Initialize repositories
account_repo = AccountRepository()
transaction_repo = TransactionRepository()
category_repo = CategoryRepository()
budget_repo = BudgetRepository()

# Create service
service = FinanceService(account_repo, transaction_repo, category_repo)

# Create accounts
checking = service.create_account("My Checking", "checking", 1000.00)
savings = service.create_account("My Savings", "savings", 5000.00)
credit = service.create_account("Credit Card", "credit", 0.0)

# Create categories
food = service.create_category("Food", "expense", "#FF0000")
salary = service.create_category("Salary", "income", "#00FF00")

# Record transactions
service.record_transaction(
    account_id=checking.id,
    category_id=salary.id,
    amount=3000.00,
    type="income",
    description="Monthly salary"
)

service.record_transaction(
    account_id=checking.id,
    category_id=food.id,
    amount=150.00,
    type="expense",
    description="Grocery shopping"
)

# Transfer between accounts
service.transfer_between_accounts(
    checking.id, savings.id, 500.00, "Monthly savings"
)

# Generate reports
report = service.generate_monthly_summary(2024, 1)
print(report.summary())  # "Profitable: $1,850.00 net flow"

# Budget tracking
budget_service = BudgetService(budget_repo, category_repo, transaction_repo)
food_budget = budget_service.create_budget(food.id, 500.00, "monthly", 80.0)
alerts = budget_service.check_budget_alerts()

# Export data
service.export_transactions_to_csv("transactions.csv")
```

### Expected Test Results

When you run `pytest project/tests/ -v`, all tests should pass:

```
============================= test session starts =============================
project/tests/test_finance_tracker.py .................................. [ 35%]
...................................................................... [100%]

============================= 94 passed in 0.5s ==============================
```

## Connection to Daily Lessons

This project reinforces concepts from each day:

### Day 1: API Design with Classes
- **Domain models** with clean interfaces (Account, Transaction, Category, Budget)
- **Validation** in `__post_init__` methods
- **Serialization** with to_dict/from_dict methods
- **Factory functions** like create_account()

### Day 2: Testing OOP Code
- Write **unit tests** for each domain model
- Use **pytest fixtures** for test data setup
- Test **state transitions** (account balance changes)
- Mock repositories when testing services

### Day 3: Refactoring Procedural to OOP
- Notice how we moved from procedural data manipulation to **encapsulated objects**
- **Extract Class**: Separated concerns into Account, Transaction, etc.
- **Repository Pattern**: Abstracted data access from business logic

### Day 4: Data Processing with OOP
- **Report generation** processes transaction data
- **Filtering and aggregation** in repositories
- **CSV export** as data transformation

### Day 5: Service-Oriented OOP
- **FinanceService** and **BudgetService** encapsulate business logic
- **Dependency injection**: Services receive repositories
- **Repository pattern**: Data access abstraction
- **Separation of concerns**: Models, repositories, services

### Day 6: Performance and Optimization
- **Lazy loading** for expensive operations
- **Efficient queries** in repositories (filter before returning)
- **Caching** for frequently accessed data

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │FinanceService│  │BudgetService │  │ ReportService   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Repository Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │AccountRepository│ │TransactionRepository│ │CategoryRepository│ │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Domain Models                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Account  │  │Transaction│  │ Category │  │ Budget   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Tips for Success

1. **Start with domain models** - Get Account, Category, Transaction, and Budget working first
2. **Use type hints** - Make your interfaces clear and catch errors early
3. **Test incrementally** - Write tests as you build each component
4. **Validate inputs** - Check for negative amounts, invalid dates, etc.
5. **Keep services stateless** - Business logic should not depend on global state
6. **Repositories handle persistence** - Keep I/O separate from business logic
7. **Follow the tests** - The test file shows expected behavior

## Running Tests

```bash
# From the project root (python-oop-journey-v2/)
pytest week07_real_world/project/tests/ -v

# Or run all tests
pytest
```

## Stretch Goals

After completing the core requirements:

- **Recurring transactions** - Schedule monthly bills
- **Budget rollovers** - Carry over unused budget
- **Spending projections** - Predict future spending
- **Multi-currency support** - Handle different currencies with exchange rates
- **Data visualization** - Generate ASCII charts for spending trends
