# Library Management System - Requirements

## Functional Requirements

### 1. Book Management

#### 1.1 Book Catalog
- **FR-1.1.1**: The system shall store book catalog information including:
  - ISBN (unique identifier)
  - Title
  - Author(s)
  - Publisher
  - Publication year
  - Genre/Category
  - Page count

#### 1.2 Book Copies
- **FR-1.2.1**: Each book in the catalog may have multiple physical copies
- **FR-1.2.2**: Each copy shall have a unique barcode
- **FR-1.2.3**: Copy status shall be one of: AVAILABLE, BORROWED, RESERVED, MAINTENANCE, LOST
- **FR-1.2.4**: The system shall track which branch holds each copy

### 2. Member Management

#### 2.1 Member Registration
- **FR-2.1.1**: The system shall allow registration of library members
- **FR-2.1.2**: Each member shall have:
  - Unique member ID
  - Full name
  - Email address
  - Phone number
  - Registration date
  - Membership status (ACTIVE, SUSPENDED, EXPIRED)

#### 2.2 Membership Rules
- **FR-2.2.1**: Active members may borrow up to 5 books simultaneously
- **FR-2.2.2**: Members with overdue books or unpaid fines cannot borrow
- **FR-2.2.3**: Membership expires after 1 year without renewal

### 3. Loan Management

#### 3.1 Check Out
- **FR-3.1.1**: Librarians can check out available books to active members
- **FR-3.1.2**: Each loan shall have:
  - Unique loan ID
  - Book copy reference
  - Member reference
  - Checkout date
  - Due date (14 days from checkout)
  - Return date (null until returned)
  - Status (ACTIVE, RETURNED, OVERDUE, LOST)

#### 3.2 Check In
- **FR-3.2.1**: Librarians can check in borrowed books
- **FR-3.2.2**: Upon check-in, the system calculates any overdue fines
- **FR-3.2.3**: The system updates book copy status to AVAILABLE or RESERVED

#### 3.3 Renewals
- **FR-3.3.1**: Members may renew loans if:
  - No other member has reserved the book
  - The loan is not already overdue
  - Maximum 2 renewals per loan
- **FR-3.3.2**: Each renewal extends the due date by 14 days

### 4. Reservation System

#### 4.1 Placing Reservations
- **FR-4.1.1**: Members can reserve books that are currently borrowed
- **FR-4.1.2**: Each reservation shall have:
  - Unique reservation ID
  - Book reference (not specific copy)
  - Member reference
  - Reservation date
  - Status (PENDING, FULFILLED, CANCELLED, EXPIRED)

#### 4.2 Reservation Fulfillment
- **FR-4.2.1**: When a reserved book is returned, status changes to AVAILABLE (reserved)
- **FR-4.2.2**: The system notifies the next member in the reservation queue
- **FR-4.2.3**: Reserved books are held for 3 days before being released

### 5. Fine Management

#### 5.1 Fine Calculation
- **FR-5.1.1**: Overdue books accrue fines based on configurable policy
- **FR-5.1.2**: Default fine: $0.50 per day overdue
- **FR-5.1.3**: Maximum fine per book: $20.00

#### 5.2 Fine Policies
- **FR-5.2.1**: The system supports multiple fine calculation strategies:
  - Standard: Fixed daily rate
  - Tiered: Increasing rate based on days overdue
  - Grace Period: No fine for first 3 days

#### 5.3 Fine Payment
- **FR-5.3.1**: The system tracks fine balances per member
- **FR-5.3.2**: Members can pay fines partially or in full
- **FR-5.3.3**: Paid fines are marked as resolved with payment date

### 6. Reporting

#### 6.1 Operational Reports
- **FR-6.1.1**: Overdue books report
- **FR-6.1.2**: Active loans by member
- **FR-6.1.3**: Popular books report
- **FR-6.1.4**: Financial summary (fines collected)

## Non-Functional Requirements

### 1. Performance
- **NFR-1.1**: System shall handle lookups in under 100ms for catalogs up to 100,000 books
- **NFR-1.2**: Search operations shall complete in under 500ms

### 2. Reliability
- **NFR-2.1**: Data consistency shall be maintained for all transactions
- **NFR-2.2**: No data loss shall occur during normal operations

### 3. Maintainability
- **NFR-3.1**: Code coverage shall be at least 80%
- **NFR-3.2**: All public APIs shall have type hints
- **NFR-3.3**: All modules shall have docstrings

### 4. Extensibility
- **NFR-4.1**: New fine policies can be added without modifying existing code
- **NFR-4.2**: New notification channels can be added via observer pattern
- **NFR-4.3**: Repository layer abstraction allows different storage backends

## Constraints

- **C-1**: System is implemented in Python 3.10+
- **C-2**: No external database required (in-memory with optional file persistence)
- **C-3**: Command-line interface only (no GUI)
- **C-4**: Single-library deployment (no distributed requirements)

## User Stories

### As a Member
1. I want to borrow books so I can read them at home
2. I want to see my current loans and due dates
3. I want to renew books to extend my reading time
4. I want to reserve popular books that are currently checked out
5. I want to see my fine balance and payment history

### As a Librarian
1. I want to check out books quickly for members
2. I want to check in returned books and process any fines
3. I want to see which books are overdue
4. I want to add new books to the catalog
5. I want to manage member accounts

### As an Administrator
1. I want to configure fine policies for different book types
2. I want to generate usage reports
3. I want to track system activity

## Domain Invariants

The following conditions must always remain true:

1. **INV-1**: A book copy can have at most one active loan
2. **INV-2**: A member can have at most 5 active loans
3. **INV-3**: A book with active reservations cannot be borrowed by non-reservers
4. **INV-4**: Fine amounts are always non-negative
5. **INV-5**: Due dates are always after checkout dates
6. **INV-6**: Only active members can borrow books
7. **INV-7**: Suspended members cannot place reservations

## Acceptance Criteria

### Book Checkout
```gherkin
Given a member with no overdue books or fines
And an available book copy
When the librarian checks out the book to the member
Then the loan is created with a due date 14 days from today
And the book copy status changes to BORROWED
And the member's active loan count increases by 1
```

### Overdue Fine Calculation
```gherkin
Given a loan that is 5 days overdue
And a standard fine policy of $0.50 per day
When the book is returned
Then a fine of $2.50 is assessed to the member
```

### Reservation Queue
```gherkin
Given a book with two pending reservations (Member A, then Member B)
When the book is returned
Then Member A's reservation is marked FULFILLED
And the book is held for Member A
And Member B remains in the queue
```
