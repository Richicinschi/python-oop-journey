"""Demo script for the Library Management System.

Run this script to see the Library Management System in action:
    python demo.py
"""

from __future__ import annotations

"""Demo script for the Library Management System.

Run this script to see the Library Management System in action:
    python demo.py

This demo showcases all major features of the capstone project:
- Book catalog with search
- Member management
- Checkout/return workflows
- Reservation system
- Fine calculation
"""

from library_management_system.domain.book import Book, BookCopy
from library_management_system.domain.member import Member
from library_management_system.repositories.book_repository import InMemoryBookRepository
from library_management_system.repositories.member_repository import InMemoryMemberRepository
from library_management_system.repositories.loan_repository import InMemoryLoanRepository
from library_management_system.services.catalog_service import CatalogService
from library_management_system.services.circulation_service import CirculationService
from library_management_system.services.reservation_service import ReservationService
from library_management_system.services.fine_service import FineService


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n--- {title} ---")


def main() -> int:
    """Run the Library Management System demo."""
    print_header("Library Management System Demo")
    print("Week 8 Capstone - OOP Journey")

    # Initialize repositories
    print_section("Initializing System")
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()
    loan_repo = InMemoryLoanRepository()
    print("✓ Repositories created")

    # Initialize services
    catalog = CatalogService(book_repo)
    circulation = CirculationService(book_repo, member_repo, loan_repo)
    reservations = ReservationService(book_repo, member_repo, loan_repo)
    fines = FineService(member_repo, loan_repo)
    print("✓ Services initialized")

    # Add books to catalog
    print_section("Adding Books to Catalog")
    books_data = [
        ("978-0-13-110362-7", "The C Programming Language", ("Brian Kernighan", "Dennis Ritchie"), "Prentice Hall", 1988, "Programming"),
        ("978-0-13-468599-1", "Clean Code", ("Robert C. Martin",), "Prentice Hall", 2008, "Programming"),
        ("978-0-201-63361-0", "Design Patterns", ("Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"), "Addison-Wesley", 1994, "Programming"),
        ("978-0-13-235088-4", "Clean Architecture", ("Robert C. Martin",), "Prentice Hall", 2017, "Software Architecture"),
        ("978-0-321-75627-3", "Python Cookbook", ("David Beazley", "Brian Jones"), "O'Reilly", 2013, "Python"),
    ]

    saved_books = []
    for isbn, title, authors, publisher, year, genre in books_data:
        book = Book(
            isbn=isbn,
            title=title,
            authors=authors,
            publisher=publisher,
            publication_year=year,
            genre=genre,
        )
        saved = catalog.add_book(book)
        saved_books.append(saved)
        print(f"  Added: {title[:40]:<40} (ISBN: {saved.isbn})")

    # Add copies
    print_section("Adding Book Copies")
    all_copies = []
    for book in saved_books:
        for i in range(2):  # Add 2 copies of each book
            copy = BookCopy(
                barcode=f"CP-{book.isbn[-4:]}-{i+1}",
                book_isbn=book.isbn,
                branch_id="MAIN"
            )
            saved_copy = catalog.add_copy(book.isbn, copy)
            all_copies.append(saved_copy)
        print(f"  Added 2 copies of: {book.title[:35]:<35}")

    # Add members
    print_section("Registering Members")
    members_data = [
        ("MEM001", "Alice Johnson", "alice@example.com", "555-0101", "123 Main St"),
        ("MEM002", "Bob Smith", "bob@example.com", "555-0102", "456 Oak Ave"),
        ("MEM003", "Carol White", "carol@example.com", "555-0103", "789 Pine Rd"),
    ]

    saved_members = []
    for member_id, name, email, phone, address in members_data:
        member = Member(
            member_id=member_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
        )
        saved = member_repo.save(member)
        saved_members.append(saved)
        print(f"  Registered: {name:<25} (ID: {saved.member_id})")

    # Demonstrate search
    print_section("Searching Catalog")
    print("Search for 'Python':")
    results = catalog.search("Python")
    for result in results[:3]:
        print(f"  • {result.book.title} by {', '.join(result.book.authors[:2])}")

    print("\nSearch for 'Robert' (author):")
    results = catalog.search("Robert")
    for result in results[:3]:
        print(f"  • {result.book.title} (Score: {result.score:.2f})")

    # Demonstrate checkout
    print_section("Checking Out Books")
    alice = saved_members[0]
    bob = saved_members[1]

    # Alice checks out a book
    copy1 = all_copies[0]  # First copy of first book
    success, message, loan1 = circulation.checkout(copy1.barcode, alice.member_id, loan_id="LOAN001")
    print(f"  Alice checkout: {message}")
    if loan1:
        print(f"    Due date: {loan1.due_date}")

    # Bob checks out a book
    copy2 = all_copies[2]  # First copy of second book
    success, message, loan2 = circulation.checkout(copy2.barcode, bob.member_id, loan_id="LOAN002")
    print(f"  Bob checkout: {message}")

    # Try to checkout same copy (should fail)
    success, message, _ = circulation.checkout(copy1.barcode, bob.member_id)
    print(f"  Bob tries same book: {message}")

    # Demonstrate reservations
    print_section("Managing Reservations")
    # Carol wants a book that's checked out
    carol = saved_members[2]
    book1 = saved_books[0]

    success, message, reservation = reservations.create_reservation(book1.isbn, carol.member_id, reservation_id="RES001")
    print(f"  Carol reserves '{book1.title[:30]}': {message}")
    if reservation:
        print(f"    Queue position: {reservation.queue_position}")

    # Demonstrate return and reservation fulfillment
    print_section("Returning Books")
    success, message, returned_loan = circulation.return_book(copy1.barcode)
    print(f"  Alice returns book: {message}")

    # Check if Carol's reservation can be fulfilled by looking at pending reservations
    pending = reservations.get_pending_reservations(book1.isbn)
    if pending:
        # Fulfill the first pending reservation
        reservations.fulfill_reservation(pending[0].reservation_id)
        print(f"  Carol's reservation is now ready for pickup!")

    # Demonstrate renewals
    print_section("Renewing Loans")
    success, message = circulation.renew(loan2.loan_id)
    print(f"  Bob renews loan: {message}")

    # Demonstrate catalog statistics
    print_section("Catalog Statistics")
    stats = catalog.get_catalog_statistics()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    # Demonstrate member status
    print_section("Member Status")
    for member in saved_members:
        m = member_repo.find_by_id(member.member_id)
        print(f"  {m.name:<25} Loans: {m.active_loan_count}  Fines: ${float(m.total_outstanding_fines):.2f}")

    # Demonstrate fine service
    print_section("Fine Management")
    fine_stats = fines.get_fine_statistics()
    print(f"  Total outstanding fines: ${fine_stats['total_outstanding_fines']}")
    print(f"  Members with fines: {fine_stats['members_with_fines']}")

    # Summary
    print_header("Demo Complete!")
    print("""
Design Patterns Demonstrated:
  ✓ Repository Pattern - Abstract data access layer
  ✓ Strategy Pattern - Search strategies and fine calculation
  ✓ Observer Pattern - Event bus for circulation events
  ✓ Factory Pattern - Loan creation

Key Features:
  ✓ Book catalog with search
  ✓ Member management
  ✓ Checkout/return/renew workflows
  ✓ Reservation queue management
  ✓ Fine calculation and payment
  ✓ Comprehensive test coverage

Run tests with: pytest library_management_system/tests/ -v
""")

    return 0


if __name__ == "__main__":
    exit(main())
