"""Command-line interface for the Library Management System."""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Optional

from ..domain.book import Book, BookCopy
from ..domain.member import Member
from ..repositories.book_repository import InMemoryBookRepository
from ..repositories.loan_repository import InMemoryLoanRepository
from ..repositories.member_repository import InMemoryMemberRepository
from ..services.catalog_service import CatalogService
from ..services.circulation_service import CirculationService, CirculationEvent
from ..services.fine_service import FineService
from ..services.reservation_service import ReservationService


class LibraryCLI:
    """Command-line interface for library operations.

    Provides an interactive menu system for managing the library.
    """

    def __init__(self) -> None:
        # Initialize repositories
        self._book_repo = InMemoryBookRepository()
        self._member_repo = InMemoryMemberRepository()
        self._loan_repo = InMemoryLoanRepository()

        # Initialize services
        self._catalog = CatalogService(self._book_repo)
        self._circulation = CirculationService(
            self._book_repo, self._member_repo, self._loan_repo
        )
        self._reservations = ReservationService(
            self._book_repo, self._member_repo, self._loan_repo
        )
        self._fines = FineService(self._member_repo, self._loan_repo)

        # Set up event listener
        self._circulation.event_bus.on("checkout", self._on_checkout)
        self._circulation.event_bus.on("return", self._on_return)

        self._running = False

    def _on_checkout(self, event: CirculationEvent) -> None:
        """Handle checkout event."""
        # Could log to file or send notifications
        pass

    def _on_return(self, event: CirculationEvent) -> None:
        """Handle return event - check for reservations."""
        # Check if this return can fulfill any reservations
        loan = self._loan_repo.find_by_id(event.loan_id or "")
        if loan:
            copy = self._book_repo.find_copy_by_barcode(loan.copy_barcode)
            if copy:
                # Find the book this copy belongs to
                from ..repositories.book_repository import InMemoryBookRepository
                if isinstance(self._book_repo, InMemoryBookRepository):
                    for book in self._book_repo.get_all_books():
                        if book.isbn == copy.book_isbn:
                            # Get pending reservations for this book
                            pending = self._reservations.get_pending_reservations(book.isbn)
                            if pending:
                                # Fulfill the first reservation
                                res = pending[0]
                                self._reservations.fulfill_reservation(res.reservation_id)
                                member = self._member_repo.find_by_id(res.member_id)
                                print(
                                    f"\n[Notification] Reservation ready for {member.name if member else 'Unknown'}"
                                )
                            break

    def run(self) -> None:
        """Run the CLI main loop."""
        self._running = True
        self._print_welcome()

        while self._running:
            try:
                self._show_main_menu()
                choice = input("\nEnter choice: ").strip()
                self._handle_main_choice(choice)
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _print_welcome(self) -> None:
        """Print welcome message."""
        print("=" * 60)
        print("    Library Management System")
        print("    Week 8 Capstone - OOP Journey")
        print("=" * 60)

    def _show_main_menu(self) -> None:
        """Display main menu."""
        print("\n--- Main Menu ---")
        print("1. Book Catalog")
        print("2. Member Management")
        print("3. Circulation (Checkout/Return)")
        print("4. Reservations")
        print("5. Fines & Payments")
        print("6. Reports")
        print("7. Demo: Setup Sample Data")
        print("0. Exit")

    def _handle_main_choice(self, choice: str) -> None:
        """Handle main menu choice."""
        if choice == "1":
            self._catalog_menu()
        elif choice == "2":
            self._member_menu()
        elif choice == "3":
            self._circulation_menu()
        elif choice == "4":
            self._reservation_menu()
        elif choice == "5":
            self._fines_menu()
        elif choice == "6":
            self._reports_menu()
        elif choice == "7":
            self._setup_demo_data()
        elif choice == "0":
            print("\nGoodbye!")
            self._running = False
        else:
            print("Invalid choice")

    def _catalog_menu(self) -> None:
        """Book catalog submenu."""
        while True:
            print("\n--- Book Catalog ---")
            print("1. List all books")
            print("2. Search books")
            print("3. Add new book")
            print("4. View book details")
            print("5. Add book copy")
            print("6. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self._list_books()
            elif choice == "2":
                self._search_books()
            elif choice == "3":
                self._add_book()
            elif choice == "4":
                self._view_book_details()
            elif choice == "5":
                self._add_book_copy()
            elif choice == "6":
                break

    def _list_books(self) -> None:
        """List all books."""
        books = self._catalog.list_all_books()
        if not books:
            print("\nNo books in catalog.")
            return

        print(f"\n{'ISBN':<18} {'Title':<35} {'Available':<12} {'Copies':<10}")
        print("-" * 80)
        for book in books:
            title = book.title[:33] + ".." if len(book.title) > 35 else book.title
            print(
                f"{book.isbn:<18} {title:<35} {book.available_copy_count:<12} {book.copy_count}"
            )

    def _search_books(self) -> None:
        """Search books."""
        query = input("Enter search query: ").strip()
        if not query:
            return

        results = self._catalog.search(query)
        if not results:
            print("\nNo books found.")
            return

        print(f"\n{'ISBN':<18} {'Title':<35} {'Authors':<25}")
        print("-" * 80)
        for result in results[:10]:  # Limit to top 10
            book = result.book
            title = book.title[:33] + ".." if len(book.title) > 35 else book.title
            authors = ", ".join(book.authors[:2])
            authors = authors[:23] + ".." if len(authors) > 25 else authors
            print(f"{book.isbn:<18} {title:<35} {authors:<25}")

    def _add_book(self) -> None:
        """Add a new book to catalog."""
        print("\n--- Add New Book ---")
        isbn = input("ISBN: ").strip()
        title = input("Title: ").strip()
        authors_str = input("Authors (comma-separated): ").strip()
        publisher = input("Publisher: ").strip()

        try:
            year = int(input("Publication Year: ").strip())
        except ValueError:
            print("Invalid year")
            return

        genre = input("Genre: ").strip()
        description = input("Description: ").strip()

        authors = [a.strip() for a in authors_str.split(",") if a.strip()]

        book = Book(
            isbn=isbn,
            title=title,
            authors=authors,
            publisher=publisher,
            publication_year=year,
            genre=genre,
            description=description,
        )

        self._catalog.add_book(book)
        print(f"\nBook added successfully! ID: {book.id[:8]}")

    def _view_book_details(self) -> None:
        """View book details."""
        isbn = input("Enter ISBN: ").strip()
        book = self._catalog.get_book(isbn)

        if not book:
            print("Book not found.")
            return

        print(f"\n{'='*50}")
        print(f"Title: {book.title}")
        print(f"Authors: {', '.join(book.authors)}")
        print(f"ISBN: {book.isbn}")
        print(f"Publisher: {book.publisher}")
        print(f"Year: {book.publication_year}")
        print(f"Genre: {book.genre}")
        print(f"Copies: {book.available_copy_count} available / {book.copy_count} total")

        copies = self._catalog.get_copies_for_book(book.isbn)
        if copies:
            print(f"\n--- Copies ---")
            for copy in copies:
                print(f"  {copy.barcode} - {copy.status.value}")

    def _add_book_copy(self) -> None:
        """Add a copy to an existing book."""
        isbn = input("Enter ISBN: ").strip()
        barcode = input("Enter copy barcode: ").strip()
        branch = input("Enter branch ID (default: MAIN): ").strip() or "MAIN"
        
        from ..domain.book import BookCopy
        copy = BookCopy(barcode=barcode, book_isbn=isbn, branch_id=branch)
        result = self._catalog.add_copy(isbn, copy)

        if result:
            print(f"Copy added successfully! Barcode: {result.barcode}")
        else:
            print("Book not found.")

    def _member_menu(self) -> None:
        """Member management submenu."""
        while True:
            print("\n--- Member Management ---")
            print("1. List all members")
            print("2. Search members")
            print("3. Add new member")
            print("4. View member details")
            print("5. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self._list_members()
            elif choice == "2":
                self._search_members()
            elif choice == "3":
                self._add_member()
            elif choice == "4":
                self._view_member_details()
            elif choice == "5":
                break

    def _list_members(self) -> None:
        """List all members."""
        members = self._member_repo.get_all()
        if not members:
            print("\nNo members registered.")
            return

        print(f"\n{'ID':<12} {'Name':<25} {'Status':<12} {'Loans':<8} {'Fines':<10}")
        print("-" * 75)
        for m in members:
            name = m.name[:23] + ".." if len(m.name) > 25 else m.name
            print(
                f"{m.member_id:<12} {name:<25} {m.status.value:<12} {m.active_loan_count:<8} ${float(m.total_outstanding_fines):<9.2f}"
            )

    def _search_members(self) -> None:
        """Search members by name."""
        name = input("Enter name to search: ").strip()
        members = self._member_repo.find_by_name(name)

        if not members:
            print("No members found.")
            return

        for m in members:
            print(f"{m.member_number}: {m.name} ({m.email})")

    def _add_member(self) -> None:
        """Add a new member."""
        print("\n--- Add New Member ---")
        member_id = input("Member ID: ").strip()
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        address = input("Address: ").strip()

        member = Member(
            member_id=member_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
        )

        self._member_repo.save(member)
        print(f"\nMember added! Member ID: {member.member_id}")

    def _view_member_details(self) -> None:
        """View member details."""
        member_id = input("Enter member ID: ").strip()

        member = self._member_repo.find_by_id(member_id)

        if not member:
            print("Member not found.")
            return

        print(f"\n{'='*50}")
        print(f"Name: {member.name}")
        print(f"Member ID: {member.member_id}")
        print(f"Email: {member.email}")
        print(f"Phone: {member.phone}")
        print(f"Address: {member.address}")
        print(f"Status: {member.status.value}")
        print(f"Registered: {member.registration_date}")
        print(f"Current Loans: {member.active_loan_count}")
        print(f"Outstanding Fines: ${float(member.total_outstanding_fines):.2f}")

        # Show active loans
        active_loans = self._circulation.get_active_loans(member.member_id)
        if active_loans:
            print(f"\n--- Active Loans ---")
            for loan in active_loans:
                copy = self._book_repo.find_copy_by_barcode(loan.copy_barcode)
                book = None
                if copy:
                    book = self._book_repo.find_book_by_isbn(copy.book_isbn)
                title = book.title if book else "Unknown"
                status = "OVERDUE" if loan.is_overdue() else "Active"
                print(f"  {title[:30]:<30} Due: {loan.due_date} [{status}]")

    def _circulation_menu(self) -> None:
        """Circulation submenu."""
        while True:
            print("\n--- Circulation ---")
            print("1. Checkout book")
            print("2. Return book")
            print("3. Renew loan")
            print("4. View overdue loans")
            print("5. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self._checkout_book()
            elif choice == "2":
                self._return_book()
            elif choice == "3":
                self._renew_loan()
            elif choice == "4":
                self._view_overdue()
            elif choice == "5":
                break

    def _checkout_book(self) -> None:
        """Checkout a book."""
        copy_barcode = input("Enter book copy barcode: ").strip()
        member_id = input("Enter member ID: ").strip()

        success, message, loan = self._circulation.checkout(copy_barcode, member_id)
        print(f"\n{message}")
        if loan:
            print(f"Due date: {loan.due_date}")

    def _return_book(self) -> None:
        """Return a book."""
        copy_barcode = input("Enter book copy barcode: ").strip()

        success, message, loan = self._circulation.return_book(copy_barcode)
        print(f"\n{message}")
        if loan and loan.status.value == "overdue":
            # Calculate potential fine
            days = loan.days_overdue()
            fine = days * 0.50  # $0.50 per day
            print(f"Book was {days} days overdue. Fine: ${fine:.2f}")

    def _renew_loan(self) -> None:
        """Renew a loan."""
        loan_id = input("Enter loan ID: ").strip()

        success, message = self._circulation.renew(loan_id)
        print(f"\n{message}")
        if success:
            loan = self._loan_repo.find_by_id(loan_id)
            if loan:
                print(f"New due date: {loan.due_date}")

    def _view_overdue(self) -> None:
        """View overdue loans."""
        overdue = self._circulation.get_overdue_loans()
        if not overdue:
            print("\nNo overdue loans.")
            return

        print(f"\n{'Member':<20} {'Book Copy':<12} {'Days Overdue':<15} {'Est. Fine':<10}")
        print("-" * 65)
        for loan in overdue:
            member = self._member_repo.find_by_id(loan.member_id)
            member_name = member.name[:18] if member else "Unknown"
            days = loan.days_overdue()
            fine = days * 0.50  # Estimate at $0.50/day
            print(f"{member_name:<20} {loan.copy_barcode:<12} {days:<15} ${fine:.2f}")

    def _reservation_menu(self) -> None:
        """Reservations submenu."""
        while True:
            print("\n--- Reservations ---")
            print("1. Create reservation")
            print("2. Cancel reservation")
            print("3. View member reservations")
            print("4. View book reservations")
            print("5. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self._create_reservation()
            elif choice == "2":
                self._cancel_reservation()
            elif choice == "3":
                self._view_member_reservations()
            elif choice == "4":
                self._view_book_reservations()
            elif choice == "5":
                break

    def _create_reservation(self) -> None:
        """Create a reservation."""
        isbn = input("Enter book ISBN: ").strip()
        member_id = input("Enter member ID: ").strip()

        success, message, reservation = self._reservations.create_reservation(
            isbn, member_id
        )
        print(f"\n{message}")
        if reservation:
            print(f"Reservation ID: {reservation.reservation_id}")
            print(f"Queue position: {reservation.queue_position}")

    def _cancel_reservation(self) -> None:
        """Cancel a reservation."""
        reservation_id = input("Enter reservation ID: ").strip()

        success, message = self._reservations.cancel_reservation(reservation_id)
        print(f"\n{message}")

    def _view_member_reservations(self) -> None:
        """View reservations for a member."""
        member_id = input("Enter member ID: ").strip()

        reservations = self._reservations.get_member_reservations(member_id)
        if not reservations:
            print("\nNo reservations found.")
            return

        print(f"\n{'ISBN':<18} {'Status':<12} {'Position':<10} {'Created':<15}")
        print("-" * 60)
        for r in reservations:
            created = r.reservation_date.strftime("%Y-%m-%d")
            position = r.queue_position if r.queue_position else "-"
            print(f"{r.book_isbn:<18} {r.status.value:<12} {position:<10} {created:<15}")

    def _view_book_reservations(self) -> None:
        """View reservations for a book."""
        isbn = input("Enter book ISBN: ").strip()

        reservations = self._reservations.get_book_reservations(isbn)
        if not reservations:
            print("\nNo reservations found.")
            return

        print(f"\n{'Member':<20} {'Status':<12} {'Position':<10}")
        print("-" * 45)
        for r in reservations:
            member = self._member_repo.find_by_id(r.member_id)
            name = member.name[:18] if member else "Unknown"
            position = r.queue_position if r.queue_position else "-"
            print(f"{name:<20} {r.status.value:<12} {position:<10}")

    def _fines_menu(self) -> None:
        """Fines submenu."""
        while True:
            print("\n--- Fines & Payments ---")
            print("1. View member fines")
            print("2. Process payment")
            print("3. Waive fines (librarian)")
            print("4. Fine statistics")
            print("5. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                self._view_member_fines()
            elif choice == "2":
                self._process_payment()
            elif choice == "3":
                self._waive_fines()
            elif choice == "4":
                self._fine_statistics()
            elif choice == "5":
                break

    def _view_member_fines(self) -> None:
        """View fines for a member."""
        member_id = input("Enter member ID: ").strip()

        member = self._member_repo.find_by_id(member_id)
        if not member:
            print("Member not found.")
            return

        fines = member.outstanding_fines
        print(f"\nMember: {member.name}")
        print(f"Total outstanding fines: ${float(member.total_outstanding_fines):.2f}")

        if fines:
            print(f"\n--- Outstanding Fines ---")
            for fine in fines:
                print(f"Fine {fine.fine_id}: ${float(fine.amount):.2f} - {fine.reason}")

    def _process_payment(self) -> None:
        """Process a payment."""
        member_id = input("Enter member ID: ").strip()
        fine_id = input("Enter fine ID: ").strip()

        try:
            amount = float(input("Payment amount: $"))
        except ValueError:
            print("Invalid amount")
            return

        success, message, remaining = self._fines.process_payment(member_id, fine_id, amount)
        print(f"\n{message}")

    def _waive_fines(self) -> None:
        """Waive a fine (requires librarian permissions in real system)."""
        member_id = input("Enter member ID: ").strip()
        fine_id = input("Enter fine ID to waive: ").strip()
        librarian_id = input("Enter your librarian ID: ").strip()

        member = self._member_repo.find_by_id(member_id)
        if not member:
            print("Member not found.")
            return

        # Find the fine and waive it
        for fine in member.outstanding_fines:
            if fine.fine_id == fine_id:
                try:
                    waived_fine = fine.waive(librarian_id)
                    # In a real system, we'd save the waived fine back
                    print(f"\nFine {fine_id} waived by {librarian_id}")
                    return
                except Exception as e:
                    print(f"\nError: {e}")
                    return
        
        print(f"Fine {fine_id} not found for this member.")

    def _fine_statistics(self) -> None:
        """Show fine statistics."""
        stats = self._fines.get_fine_statistics()

        print(f"\n--- Fine Statistics ---")
        print(f"Total outstanding fines: ${stats['total_outstanding_fines']}")
        print(f"Members with fines: {stats['members_with_fines']}")
        print(f"Average fine per member: ${stats['average_fine_per_member']}")

    def _reports_menu(self) -> None:
        """Reports submenu."""
        while True:
            print("\n--- Reports ---")
            print("1. Catalog statistics")
            print("2. Member statistics")
            print("3. Circulation statistics")
            print("4. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                stats = self._catalog.get_catalog_statistics()
                print(f"\n--- Catalog Statistics ---")
                for key, value in stats.items():
                    print(f"  {key}: {value}")

            elif choice == "2":
                members = self._member_repo.get_all()
                print(f"\nTotal members: {len(members)}")
                print(f"Active: {sum(1 for m in members if m.status.name == 'ACTIVE')}")
                print(f"Suspended: {sum(1 for m in members if m.status.name == 'SUSPENDED')}")

            elif choice == "3":
                loans = self._loan_repo.get_all()
                active = sum(1 for l in loans if l.status.name == "ACTIVE")
                returned = sum(1 for l in loans if l.status.name == "RETURNED")
                overdue = sum(1 for l in loans if l.status.name == "OVERDUE")

                print(f"\n--- Circulation Statistics ---")
                print(f"Total loans: {len(loans)}")
                print(f"Active: {active}")
                print(f"Returned: {returned}")
                print(f"Overdue: {overdue}")

            elif choice == "4":
                break

    def _setup_demo_data(self) -> None:
        """Set up sample data for demonstration."""
        print("\n--- Setting up demo data ---")

        # Add books
        books_data = [
            ("978-0-13-110362-7", "The C Programming Language", ["Brian Kernighan", "Dennis Ritchie"], "Prentice Hall", 1988, "Programming"),
            ("978-0-13-468599-1", "Clean Code", ["Robert C. Martin"], "Prentice Hall", 2008, "Programming"),
            ("978-0-201-63361-0", "Design Patterns", ["Gang of Four"], "Addison-Wesley", 1994, "Programming"),
            ("978-0-13-235088-4", "Clean Architecture", ["Robert C. Martin"], "Prentice Hall", 2017, "Programming"),
            ("978-0-321-75627-3", "Python Cookbook", ["David Beazley", "Brian Jones"], "O'Reilly", 2013, "Programming"),
        ]

        copies_added = 0
        for isbn, title, authors, publisher, year, genre in books_data:
            book = Book(
                isbn=isbn,
                title=title,
                authors=authors,
                publisher=publisher,
                publication_year=year,
                genre=genre,
                description=f"A book about {genre}",
            )
            self._catalog.add_book(book)
            # Add 2-3 copies of each book
            for _ in range(2):
                self._catalog.add_copy(book.id)
                copies_added += 1

        # Add members
        members_data = [
            ("Alice Johnson", "alice@example.com", "555-0101", "123 Main St"),
            ("Bob Smith", "bob@example.com", "555-0102", "456 Oak Ave"),
            ("Carol White", "carol@example.com", "555-0103", "789 Pine Rd"),
            ("David Brown", "david@example.com", "555-0104", "321 Elm St"),
        ]

        for name, email, phone, address in members_data:
            member = Member(
                name=name,
                email=email,
                phone=phone,
                address=address,
            )
            self._member_repo.save(member)

        print(f"Added {len(books_data)} books with {copies_added} copies")
        print(f"Added {len(members_data)} members")
        print("\nDemo data ready! Try:")
        print("  1. Book Catalog > List all books")
        print("  2. Member Management > List all members")
        print("  3. Circulation > Checkout book")


def main() -> int:
    """Main entry point for the CLI."""
    cli = LibraryCLI()
    cli.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
