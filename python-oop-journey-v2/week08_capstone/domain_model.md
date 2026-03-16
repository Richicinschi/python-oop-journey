# Library Management System - Domain Model

## Domain Overview

The Library Management System domain consists of entities representing the physical and conceptual objects in a library ecosystem. The model follows Domain-Driven Design principles with clear entity boundaries and aggregate roots.

## Core Entities

### 1. Book (Aggregate Root)

The `Book` entity represents a title in the library's catalog. It is the aggregate root for book-related operations.

**Attributes:**
- `isbn: str` - International Standard Book Number (unique identifier)
- `title: str` - Book title
- `authors: tuple[str, ...]` - Author names (immutable tuple)
- `publisher: str` - Publishing house
- `publication_year: int` - Year of publication
- `genre: str` - Book category/genre
- `page_count: int | None` - Number of pages (optional)

**Invariants:**
- ISBN must be valid format (10 or 13 digits)
- Title cannot be empty
- At least one author must be specified
- Publication year cannot be in the future

**Relationships:**
- One-to-Many with `BookCopy` (a book has multiple copies)
- One-to-Many with `Reservation` (a book can have multiple reservations)

---

### 2. BookCopy (Entity)

The `BookCopy` entity represents a physical instance of a book in the library.

**Attributes:**
- `barcode: str` - Unique identifier for this physical copy
- `book_isbn: str` - Reference to the catalog entry
- `branch_id: str` - Location identifier
- `acquisition_date: date` - When the library acquired this copy
- `status: CopyStatus` - Current availability status
- `condition: Condition` - Physical condition rating

**Status Enum:**
```python
class CopyStatus(Enum):
    AVAILABLE = "available"       # Ready for checkout
    BORROWED = "borrowed"         # Currently on loan
    RESERVED = "reserved"         # On hold for a member
    MAINTENANCE = "maintenance"   # Being repaired/cleaned
    LOST = "lost"                 # Missing copy
```

**Invariants:**
- Barcode must be unique across the system
- Only one active loan per copy at any time
- Status transitions must follow valid workflow:
  - AVAILABLE → BORROWED, RESERVED, MAINTENANCE
  - BORROWED → AVAILABLE, RESERVED, LOST
  - RESERVED → AVAILABLE, BORROWED
  - MAINTENANCE → AVAILABLE
  - LOST → AVAILABLE (if found)

---

### 3. Member (Aggregate Root)

The `Member` entity represents a library patron with borrowing privileges.

**Attributes:**
- `member_id: str` - Unique identifier
- `name: str` - Full name
- `email: str` - Contact email (unique)
- `phone: str | None` - Contact phone
- `address: str | None` - Physical address
- `registration_date: date` - When membership started
- `status: MembershipStatus` - Current membership state
- `_active_loans: list[Loan]` - Currently borrowed books
- `_fines: list[Fine]` - Outstanding and paid fines

**MembershipStatus Enum:**
```python
class MembershipStatus(Enum):
    ACTIVE = "active"           # Can borrow and reserve
    SUSPENDED = "suspended"     # Cannot borrow (overdue/fines)
    EXPIRED = "expired"         # Membership lapsed
```

**Invariants:**
- Member ID must be unique
- Email must be valid format
- Maximum 5 active loans
- Cannot borrow if status is not ACTIVE
- Cannot borrow if outstanding fines exceed $20

**Business Rules:**
- Membership expires after 365 days of inactivity
- Suspension lifted when all overdues returned and fines paid

---

### 4. Librarian (Entity)

The `Librarian` entity represents library staff with administrative privileges.

**Attributes:**
- `staff_id: str` - Unique identifier
- `name: str` - Full name
- `email: str` - Contact email
- `role: StaffRole` - Position level
- `permissions: set[Permission]` - Granted permissions

**StaffRole Enum:**
```python
class StaffRole(Enum):
    ASSISTANT = "assistant"     # Basic checkout/checkin
    LIBRARIAN = "librarian"     # Full circulation + member management
    MANAGER = "manager"         # All permissions + configuration
```

**Permissions:**
- `CHECKOUT` - Check out books to members
- `CHECKIN` - Process book returns
- `MANAGE_MEMBERS` - Add/edit member accounts
- `MANAGE_CATALOG` - Add/edit book catalog
- `MANAGE_FINES` - Adjust fine amounts
- `GENERATE_REPORTS` - Access reporting functions

---

### 5. Loan (Entity)

The `Loan` entity represents a book borrowing transaction.

**Attributes:**
- `loan_id: str` - Unique identifier
- `copy_barcode: str` - Reference to borrowed copy
- `member_id: str` - Reference to borrowing member
- `checkout_date: date` - When book was borrowed
- `due_date: date` - When book must be returned
- `return_date: date | None` - When book was returned (null if active)
- `renewal_count: int` - Number of times renewed (max 2)
- `status: LoanStatus` - Current state

**LoanStatus Enum:**
```python
class LoanStatus(Enum):
    ACTIVE = "active"           # Currently borrowed
    RETURNED = "returned"       # Successfully returned
    OVERDUE = "overdue"         # Past due date, not returned
    LOST = "lost"               # Declared lost by member
```

**Invariants:**
- Due date must be after checkout date
- Return date must be after checkout date (if set)
- Maximum 2 renewals per loan
- Only ACTIVE loans can be renewed
- Status automatically transitions to OVERDUE when due_date < today

**Business Rules:**
- Standard loan period: 14 days
- Each renewal adds 14 days to due date
- Cannot renew if book has pending reservations

---

### 6. Reservation (Entity)

The `Reservation` entity represents a member's request to borrow a book when it becomes available.

**Attributes:**
- `reservation_id: str` - Unique identifier
- `book_isbn: str` - Reference to requested book
- `member_id: str` - Reference to requesting member
- `reservation_date: datetime` - When reservation was placed
- `expiry_date: date | None` - When reservation expires
- `status: ReservationStatus` - Current state
- `queue_position: int | None` - Position in FIFO queue

**ReservationStatus Enum:**
```python
class ReservationStatus(Enum):
    PENDING = "pending"         # Waiting for book availability
    FULFILLED = "fulfilled"     # Book available, waiting for pickup
    CANCELLED = "cancelled"     # Cancelled by member
    EXPIRED = "expired"         # Not picked up within hold period
```

**Invariants:**
- Only one PENDING reservation per member per book
- Queue position is sequential (1, 2, 3, ...)
- FULFILLED reservations expire after 3 days

---

### 7. Fine (Value Object)

The `Fine` value object represents a monetary penalty for overdue books.

**Attributes:**
- `fine_id: str` - Unique identifier
- `loan_id: str` - Reference to associated loan
- `member_id: str` - Member responsible for payment
- `amount: Decimal` - Fine amount (always positive)
- `reason: str` - Description of violation
- `issued_date: date` - When fine was assessed
- `paid_date: date | None` - When fine was paid
- `status: FineStatus` - Payment state

**FineStatus Enum:**
```python
class FineStatus(Enum):
    OUTSTANDING = "outstanding"  # Unpaid
    PAID = "paid"                # Fully paid
    WAIVED = "waived"            # Forgiven by librarian
```

**Invariants:**
- Amount must be non-negative
- Paid date must be after issued date (if set)
- Once PAID or WAIVED, amount cannot change

---

### 8. FinePolicy (Strategy Interface)

The `FinePolicy` defines the interface for calculating overdue fines.

**Implementations:**

#### StandardFinePolicy
- Fixed daily rate (e.g., $0.50/day)
- Maximum cap per book (e.g., $20.00)

#### TieredFinePolicy
- Days 1-7: $0.50/day
- Days 8-14: $1.00/day
- Days 15+: $2.00/day
- Maximum cap per book

#### GracePeriodFinePolicy
- No fine for first 3 days
- Standard rate after grace period

---

## Entity Relationship Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│      Book       │────<│    BookCopy      │────<│      Loan       │
│   (Aggregate)   │ 1:M  │    (Entity)      │ 1:M │    (Entity)     │
└────────┬────────┘     └──────────────────┘     └────────┬────────┘
         │                                               │
         │ M:1                                           │ M:1
         ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│  Reservation    │                            │     Member      │
│    (Entity)     │                            │   (Aggregate)   │
└─────────────────┘                            └────────┬────────┘
                                                        │
                                 ┌──────────────────────┼──────────────────────┐
                                 │                      │                      │
                                 ▼                      ▼                      ▼
                         ┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
                         │     Fine      │    │   Librarian     │    │  FinePolicy     │
                         │ (Value Object)│    │    (Entity)     │    │   (Strategy)    │
                         └───────────────┘    └─────────────────┘    └─────────────────┘
```

## Aggregate Boundaries

### Book Aggregate
- Root: `Book`
- Contains: `BookCopy` references (via barcode lookup)
- Invariants:
  - All copies reference the same ISBN
  - Copies are created/removed through the aggregate root

### Member Aggregate
- Root: `Member`
- Contains: `Loan` references, `Fine` references
- Invariants:
  - Member status depends on loans and fines
  - Maximum active loans enforced at aggregate level

## Domain Services

### CirculationService
- `checkout(copy_id, member_id, librarian_id) -> Loan`
- `checkin(loan_id, librarian_id) -> Fine | None`
- `renew(loan_id) -> Loan`

### ReservationService
- `place_reservation(book_isbn, member_id) -> Reservation`
- `cancel_reservation(reservation_id)`
- `fulfill_reservation(book_isbn) -> Reservation | None`

### FineService
- `calculate_fine(loan, policy) -> Decimal`
- `pay_fine(fine_id, amount) -> Fine`
- `waive_fine(fine_id, librarian_id) -> Fine`

## Domain Events

### BookReturned
- Triggered when a loan is completed
- Contains: book_isbn, copy_barcode, member_id, return_date

### ReservationFulfilled
- Triggered when a reserved book becomes available
- Contains: reservation_id, member_id, book_isbn, hold_until_date

### MemberSuspended
- Triggered when member exceeds borrowing limits
- Contains: member_id, reason, suspension_date

### FineAssessed
- Triggered when overdue fine is calculated
- Contains: fine_id, member_id, loan_id, amount

## Value Objects vs Entities

| Concept | Type | Identifier | Mutability |
|---------|------|------------|------------|
| Book | Entity | ISBN | Mutable (copies change) |
| BookCopy | Entity | Barcode | Mutable (status changes) |
| Member | Entity | Member ID | Mutable (loans change) |
| Librarian | Entity | Staff ID | Mutable (permissions change) |
| Loan | Entity | Loan ID | Mutable (status changes) |
| Reservation | Entity | Reservation ID | Mutable (status changes) |
| Fine | Value Object | Fine ID | Immutable after creation |
| Money (amount) | Value Object | None | Immutable |
| Date Range | Value Object | None | Immutable |
