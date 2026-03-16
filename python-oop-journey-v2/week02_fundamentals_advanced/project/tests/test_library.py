"""Tests for the Week 2 Procedural Library System.

This test suite covers all modules:
- exceptions: Custom exception classes
- book: Book data operations
- storage: File persistence
- library: Main library API
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

# Import from reference solution for testing
from week02_fundamentals_advanced.project.reference_solution.exceptions import (
    LibraryError,
    BookNotFoundError,
    BookAlreadyExistsError,
    BookNotAvailableError,
    BookAlreadyAvailableError,
    StorageError,
    InvalidISBNError,
)
from week02_fundamentals_advanced.project.reference_solution.book import (
    is_valid_isbn,
    normalize_isbn,
    create_book,
    format_book_display,
    get_book_status,
    book_matches_query,
)
from week02_fundamentals_advanced.project.reference_solution.storage import (
    save_library,
    load_library,
    library_exists,
    backup_library,
)
from week02_fundamentals_advanced.project.reference_solution.library import (
    add_book,
    find_book,
    get_book,
    search_books,
    list_all_books,
    list_available_books,
    list_checked_out_books,
    is_book_available,
    checkout_book,
    return_book,
    remove_book,
    get_library_stats,
    clear_library,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def empty_library() -> dict:
    """Return an empty library dictionary."""
    return {}


@pytest.fixture
def sample_book() -> dict:
    """Return a sample book dictionary."""
    return {
        "isbn": "9780134685991",
        "title": "Effective Python",
        "author": "Brett Slatkin",
        "available": True,
        "checked_out_at": None,
    }


@pytest.fixture
def populated_library(empty_library) -> dict:
    """Return a library with some books."""
    add_book(empty_library, "Effective Python", "Brett Slatkin", "9780134685991")
    add_book(empty_library, "Clean Code", "Robert Martin", "9780132350884")
    add_book(empty_library, "The Pragmatic Programmer", "Andy Hunt", "9780201616224")
    return empty_library


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file tests."""
    test_dir = tempfile.mkdtemp(prefix="library_test_")
    yield test_dir
    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)


# =============================================================================
# Exception Tests
# =============================================================================

class TestExceptions:
    """Tests for custom exception classes."""
    
    def test_library_error_base_class(self):
        """Test LibraryError base exception."""
        exc = LibraryError("Test message")
        assert str(exc) == "Test message"
        assert isinstance(exc, Exception)
    
    def test_book_not_found_error(self):
        """Test BookNotFoundError stores ISBN."""
        exc = BookNotFoundError("9781234567890")
        assert exc.isbn == "9781234567890"
        assert "9781234567890" in str(exc)
        assert isinstance(exc, LibraryError)
    
    def test_book_already_exists_error(self):
        """Test BookAlreadyExistsError stores ISBN."""
        exc = BookAlreadyExistsError("9781234567890")
        assert exc.isbn == "9781234567890"
        assert isinstance(exc, LibraryError)
    
    def test_book_not_available_error(self):
        """Test BookNotAvailableError stores ISBN and title."""
        exc = BookNotAvailableError("9781234567890", "Test Book")
        assert exc.isbn == "9781234567890"
        assert exc.title == "Test Book"
        assert "Test Book" in str(exc)
    
    def test_book_not_available_error_without_title(self):
        """Test BookNotAvailableError without title."""
        exc = BookNotAvailableError("9781234567890")
        assert exc.isbn == "9781234567890"
        assert "9781234567890" in str(exc)
    
    def test_book_already_available_error(self):
        """Test BookAlreadyAvailableError."""
        exc = BookAlreadyAvailableError("9781234567890", "Test Book")
        assert exc.isbn == "9781234567890"
        assert exc.title == "Test Book"
    
    def test_storage_error(self):
        """Test StorageError stores filepath."""
        exc = StorageError("Read failed", "/path/to/file")
        assert exc.filepath == "/path/to/file"
        assert "Read failed" in str(exc)
        assert "/path/to/file" in str(exc)
    
    def test_invalid_isbn_error(self):
        """Test InvalidISBNError stores ISBN and reason."""
        exc = InvalidISBNError("bad-isbn", "Invalid length")
        assert exc.isbn == "bad-isbn"
        assert exc.reason == "Invalid length"
        assert "Invalid length" in str(exc)


# =============================================================================
# Book Module Tests
# =============================================================================

class TestIsValidISBN:
    """Tests for is_valid_isbn function."""
    
    def test_valid_isbn_13(self):
        """Test valid 13-character ISBN."""
        assert is_valid_isbn("9780134685991") is True
    
    def test_valid_isbn_10(self):
        """Test valid 10-character ISBN."""
        assert is_valid_isbn("020161622X") is True
    
    def test_valid_isbn_with_hyphens(self):
        """Test ISBN with hyphens."""
        assert is_valid_isbn("978-0-13-468599-1") is True
    
    def test_invalid_isbn_too_short(self):
        """Test ISBN that's too short."""
        assert is_valid_isbn("123456789") is False
    
    def test_invalid_isbn_too_long(self):
        """Test ISBN that's too long."""
        assert is_valid_isbn("12345678901234") is False
    
    def test_invalid_isbn_no_digits(self):
        """Test ISBN with no digits."""
        assert is_valid_isbn("abcdefghij") is False
    
    def test_invalid_isbn_not_string(self):
        """Test non-string ISBN."""
        assert is_valid_isbn(1234567890) is False
        assert is_valid_isbn(None) is False
    
    def test_invalid_isbn_special_chars(self):
        """Test ISBN with invalid special characters."""
        assert is_valid_isbn("978@01346859") is False


class TestNormalizeISBN:
    """Tests for normalize_isbn function."""
    
    def test_normalize_removes_hyphens(self):
        """Test hyphens are removed."""
        assert normalize_isbn("978-0-13-468599-1") == "9780134685991"
    
    def test_normalize_uppercase(self):
        """Test lowercase letters become uppercase."""
        assert normalize_isbn("020161622x") == "020161622X"
    
    def test_normalize_no_change_needed(self):
        """Test already normalized ISBN."""
        assert normalize_isbn("9780134685991") == "9780134685991"
    
    def test_normalize_non_string_raises(self):
        """Test non-string input raises ValueError."""
        with pytest.raises(ValueError, match="string"):
            normalize_isbn(1234567890)


class TestCreateBook:
    """Tests for create_book function."""
    
    def test_create_book_success(self):
        """Test successful book creation."""
        book = create_book("Test Title", "Test Author", "9780134685991")
        
        assert book["isbn"] == "9780134685991"
        assert book["title"] == "Test Title"
        assert book["author"] == "Test Author"
        assert book["available"] is True
        assert book["checked_out_at"] is None
    
    def test_create_book_normalizes_isbn(self):
        """Test ISBN is normalized during creation."""
        book = create_book("Title", "Author", "978-0-13-468599-1")
        assert book["isbn"] == "9780134685991"
    
    def test_create_book_strips_whitespace(self):
        """Test title and author whitespace is stripped."""
        book = create_book("  Test Title  ", "  Test Author  ", "9780134685991")
        assert book["title"] == "Test Title"
        assert book["author"] == "Test Author"
    
    def test_create_book_empty_title_raises(self):
        """Test empty title raises ValueError."""
        with pytest.raises(ValueError):
            create_book("", "Author", "9780134685991")
    
    def test_create_book_whitespace_title_raises(self):
        """Test whitespace-only title raises ValueError."""
        with pytest.raises(ValueError):
            create_book("   ", "Author", "9780134685991")
    
    def test_create_book_empty_author_raises(self):
        """Test empty author raises ValueError."""
        with pytest.raises(ValueError):
            create_book("Title", "", "9780134685991")
    
    def test_create_book_invalid_isbn_raises(self):
        """Test invalid ISBN raises InvalidISBNError."""
        with pytest.raises(InvalidISBNError):
            create_book("Title", "Author", "bad-isbn")


class TestFormatBookDisplay:
    """Tests for format_book_display function."""
    
    def test_format_available_book(self):
        """Test formatting an available book."""
        book = {
            "title": "Effective Python",
            "author": "Brett Slatkin",
            "isbn": "9780134685991",
            "available": True,
        }
        result = format_book_display(book)
        assert "Effective Python" in result
        assert "Brett Slatkin" in result
        assert "9780134685991" in result
        assert "Available" in result
    
    def test_format_checked_out_book(self):
        """Test formatting a checked out book."""
        book = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "isbn": "9780132350884",
            "available": False,
        }
        result = format_book_display(book)
        assert "Clean Code" in result
        assert "Checked Out" in result
    
    def test_format_missing_fields(self):
        """Test formatting with missing optional fields."""
        book = {"title": "Test"}
        result = format_book_display(book)
        assert "Test" in result


class TestGetBookStatus:
    """Tests for get_book_status function."""
    
    def test_status_available(self):
        """Test available book returns 'available'."""
        book = {"available": True}
        assert get_book_status(book) == "available"
    
    def test_status_checked_out(self):
        """Test checked out book returns 'checked_out'."""
        book = {"available": False}
        assert get_book_status(book) == "checked_out"
    
    def test_status_defaults_to_available(self):
        """Test missing available key defaults to available."""
        book = {}
        assert get_book_status(book) == "available"


class TestBookMatchesQuery:
    """Tests for book_matches_query function."""
    
    def test_match_in_title(self):
        """Test matching title."""
        book = {"title": "Effective Python", "author": "Brett Slatkin", "isbn": "123"}
        assert book_matches_query(book, "Effective") is True
    
    def test_match_in_author(self):
        """Test matching author."""
        book = {"title": "Effective Python", "author": "Brett Slatkin", "isbn": "123"}
        assert book_matches_query(book, "Slatkin") is True
    
    def test_match_in_isbn(self):
        """Test matching ISBN."""
        book = {"title": "Effective Python", "author": "Brett Slatkin", "isbn": "9780134685991"}
        assert book_matches_query(book, "4685991") is True
    
    def test_case_insensitive_match(self):
        """Test case-insensitive matching."""
        book = {"title": "EFFECTIVE PYTHON", "author": "Author", "isbn": "123"}
        assert book_matches_query(book, "effective") is True
    
    def test_no_match(self):
        """Test non-matching query."""
        book = {"title": "Effective Python", "author": "Brett Slatkin", "isbn": "123"}
        assert book_matches_query(book, "JavaScript") is False
    
    def test_empty_query_matches_all(self):
        """Test empty query matches all books."""
        book = {"title": "Any Book"}
        assert book_matches_query(book, "") is True


# =============================================================================
# Storage Module Tests
# =============================================================================

class TestSaveLibrary:
    """Tests for save_library function."""
    
    def test_save_and_load_roundtrip(self, empty_library, temp_dir):
        """Test saving and loading preserves data."""
        filepath = os.path.join(temp_dir, "test_library.json")
        add_book(empty_library, "Test Book", "Test Author", "9780134685991")
        
        save_library(empty_library, filepath)
        loaded = load_library(filepath)
        
        assert len(loaded) == 1
        assert "9780134685991" in loaded
        assert loaded["9780134685991"]["title"] == "Test Book"
    
    def test_save_creates_directory(self, empty_library, temp_dir):
        """Test save creates parent directories."""
        nested_path = os.path.join(temp_dir, "nested", "dir", "library.json")
        save_library(empty_library, nested_path)
        assert os.path.exists(nested_path)
    
    def test_save_overwrites_existing(self, empty_library, temp_dir):
        """Test save overwrites existing file."""
        filepath = os.path.join(temp_dir, "library.json")
        add_book(empty_library, "Book 1", "Author 1", "9780134685991")
        save_library(empty_library, filepath)
        
        empty_library.clear()
        add_book(empty_library, "Book 2", "Author 2", "9780201616224")
        save_library(empty_library, filepath)
        
        loaded = load_library(filepath)
        assert len(loaded) == 1
        assert "9780201616224" in loaded


class TestLoadLibrary:
    """Tests for load_library function."""
    
    def test_load_nonexistent_returns_empty(self, temp_dir):
        """Test loading non-existent file returns empty dict."""
        result = load_library(os.path.join(temp_dir, "nonexistent.json"))
        assert result == {}
    
    def test_load_invalid_json_raises(self, temp_dir):
        """Test loading invalid JSON raises StorageError."""
        bad_file = os.path.join(temp_dir, "bad.json")
        with open(bad_file, "w") as f:
            f.write("not valid json{")
        
        with pytest.raises(StorageError):
            load_library(bad_file)
    
    def test_load_non_dict_json_raises(self, temp_dir):
        """Test loading JSON that's not an object raises StorageError."""
        list_file = os.path.join(temp_dir, "list.json")
        with open(list_file, "w") as f:
            json.dump([1, 2, 3], f)
        
        with pytest.raises(StorageError):
            load_library(list_file)


class TestLibraryExists:
    """Tests for library_exists function."""
    
    def test_exists_true(self, temp_dir):
        """Test detecting existing file."""
        existing = os.path.join(temp_dir, "exists.json")
        with open(existing, "w") as f:
            f.write("{}")
        assert library_exists(existing) is True
    
    def test_exists_false(self, temp_dir):
        """Test non-existing file."""
        assert library_exists(os.path.join(temp_dir, "nonexistent.json")) is False
    
    def test_exists_directory_false(self, temp_dir):
        """Test directory returns False."""
        dir_path = os.path.join(temp_dir, "adir")
        os.makedirs(dir_path)
        assert library_exists(dir_path) is False


class TestBackupLibrary:
    """Tests for backup_library function."""
    
    def test_backup_creates_copy(self, empty_library, temp_dir):
        """Test backup creates a copy of the file."""
        filepath = os.path.join(temp_dir, "library.json")
        add_book(empty_library, "Test Book", "Test Author", "9780134685991")
        save_library(empty_library, filepath)
        
        backup_path = backup_library(filepath)
        
        assert os.path.exists(backup_path)
        loaded = load_library(backup_path)
        assert len(loaded) == 1
    
    def test_backup_nonexistent_raises(self, temp_dir):
        """Test backing up non-existent file raises StorageError."""
        with pytest.raises(StorageError):
            backup_library(os.path.join(temp_dir, "nonexistent.json"))


# =============================================================================
# Library Module Tests
# =============================================================================

class TestAddBook:
    """Tests for add_book function."""
    
    def test_add_book_success(self, empty_library):
        """Test successfully adding a book."""
        book = add_book(empty_library, "Test Title", "Test Author", "9780134685991")
        
        assert book["title"] == "Test Title"
        assert "9780134685991" in empty_library
    
    def test_add_book_invalid_isbn_raises(self, empty_library):
        """Test adding with invalid ISBN raises error."""
        with pytest.raises(InvalidISBNError):
            add_book(empty_library, "Title", "Author", "bad")
    
    def test_add_duplicate_isbn_raises(self, empty_library):
        """Test adding duplicate ISBN raises error."""
        add_book(empty_library, "Book 1", "Author 1", "9780134685991")
        
        with pytest.raises(BookAlreadyExistsError) as exc_info:
            add_book(empty_library, "Book 2", "Author 2", "9780134685991")
        
        assert exc_info.value.isbn == "9780134685991"
    
    def test_add_book_isbn_normalization(self, empty_library):
        """Test ISBN is normalized when adding."""
        add_book(empty_library, "Title", "Author", "978-0-13-468599-1")
        assert "9780134685991" in empty_library


class TestFindBook:
    """Tests for find_book function."""
    
    def test_find_existing_book(self, populated_library):
        """Test finding an existing book."""
        book = find_book(populated_library, "9780134685991")
        assert book is not None
        assert book["title"] == "Effective Python"
    
    def test_find_nonexistent_book(self, populated_library):
        """Test finding a book that doesn't exist."""
        book = find_book(populated_library, "9999999999999")
        assert book is None
    
    def test_find_with_hyphens_in_isbn(self, populated_library):
        """Test finding with hyphens in ISBN."""
        book = find_book(populated_library, "978-0-1346-8599-1")
        assert book is not None
        assert book["title"] == "Effective Python"


class TestGetBook:
    """Tests for get_book function."""
    
    def test_get_existing_book(self, populated_library):
        """Test getting an existing book."""
        book = get_book(populated_library, "9780134685991")
        assert book["title"] == "Effective Python"
    
    def test_get_nonexistent_book_raises(self, populated_library):
        """Test getting non-existent book raises BookNotFoundError."""
        with pytest.raises(BookNotFoundError):
            get_book(populated_library, "9999999999999")


class TestSearchBooks:
    """Tests for search_books function."""
    
    def test_search_by_title(self, populated_library):
        """Test searching by title."""
        results = search_books(populated_library, "Effective")
        assert len(results) == 1
        assert results[0]["title"] == "Effective Python"
    
    def test_search_by_author(self, populated_library):
        """Test searching by author."""
        results = search_books(populated_library, "Robert Martin")
        assert len(results) == 1
        assert results[0]["title"] == "Clean Code"
    
    def test_search_case_insensitive(self, populated_library):
        """Test search is case insensitive."""
        # Search for "CODE" should match "Clean Code" (case insensitive)
        results = search_books(populated_library, "CODE")
        titles = [r["title"] for r in results]
        assert "Clean Code" in titles
        
        # Search for "brett" should match "Brett Slatkin" (author search, case insensitive)
        results = search_books(populated_library, "brett")
        titles = [r["title"] for r in results]
        assert "Effective Python" in titles
    
    def test_search_no_matches(self, populated_library):
        """Test search with no matches."""
        results = search_books(populated_library, "JavaScript")
        assert results == []
    
    def test_search_empty_query_returns_all(self, populated_library):
        """Test empty query returns all books sorted."""
        results = search_books(populated_library, "")
        assert len(results) == 3
        assert results[0]["title"] == "Clean Code"  # Alphabetically first


class TestListBooks:
    """Tests for list functions."""
    
    def test_list_all_books_sorted(self, populated_library):
        """Test all books are returned sorted by title."""
        books = list_all_books(populated_library)
        titles = [b["title"] for b in books]
        assert titles == sorted(titles)
    
    def test_list_available_books(self, populated_library):
        """Test listing available books."""
        checkout_book(populated_library, "9780134685991")
        
        available = list_available_books(populated_library)
        assert len(available) == 2
        assert all(b["available"] for b in available)
    
    def test_list_checked_out_books(self, populated_library):
        """Test listing checked out books."""
        checkout_book(populated_library, "9780134685991")
        
        checked_out = list_checked_out_books(populated_library)
        assert len(checked_out) == 1
        assert checked_out[0]["isbn"] == "9780134685991"


class TestIsBookAvailable:
    """Tests for is_book_available function."""
    
    def test_available_book(self, populated_library):
        """Test available book returns True."""
        assert is_book_available(populated_library, "9780134685991") is True
    
    def test_checked_out_book(self, populated_library):
        """Test checked out book returns False."""
        checkout_book(populated_library, "9780134685991")
        assert is_book_available(populated_library, "9780134685991") is False
    
    def test_nonexistent_book(self, populated_library):
        """Test non-existent book returns False."""
        assert is_book_available(populated_library, "9999999999999") is False


class TestCheckoutBook:
    """Tests for checkout_book function."""
    
    def test_checkout_success(self, populated_library):
        """Test successful checkout."""
        book = checkout_book(populated_library, "9780134685991")
        
        assert book["available"] is False
        assert book["checked_out_at"] is not None
    
    def test_checkout_nonexistent_raises(self, populated_library):
        """Test checkout of non-existent book raises error."""
        with pytest.raises(BookNotFoundError):
            checkout_book(populated_library, "9999999999999")
    
    def test_checkout_unavailable_raises(self, populated_library):
        """Test checkout of unavailable book raises error."""
        checkout_book(populated_library, "9780134685991")
        
        with pytest.raises(BookNotAvailableError) as exc_info:
            checkout_book(populated_library, "9780134685991")
        
        assert exc_info.value.isbn == "9780134685991"


class TestReturnBook:
    """Tests for return_book function."""
    
    def test_return_success(self, populated_library):
        """Test successful return."""
        checkout_book(populated_library, "9780134685991")
        book = return_book(populated_library, "9780134685991")
        
        assert book["available"] is True
        assert book["checked_out_at"] is None
    
    def test_return_nonexistent_raises(self, populated_library):
        """Test return of non-existent book raises error."""
        with pytest.raises(BookNotFoundError):
            return_book(populated_library, "9999999999999")
    
    def test_return_available_raises(self, populated_library):
        """Test return of already available book raises error."""
        with pytest.raises(BookAlreadyAvailableError) as exc_info:
            return_book(populated_library, "9780134685991")
        
        assert exc_info.value.isbn == "9780134685991"


class TestRemoveBook:
    """Tests for remove_book function."""
    
    def test_remove_success(self, populated_library):
        """Test successful removal."""
        removed = remove_book(populated_library, "9780134685991")
        
        assert removed["title"] == "Effective Python"
        assert "9780134685991" not in populated_library
        assert len(populated_library) == 2
    
    def test_remove_nonexistent_raises(self, populated_library):
        """Test removing non-existent book raises error."""
        with pytest.raises(BookNotFoundError):
            remove_book(populated_library, "9999999999999")


class TestGetLibraryStats:
    """Tests for get_library_stats function."""
    
    def test_empty_library_stats(self):
        """Test stats for empty library."""
        stats = get_library_stats({})
        
        assert stats["total_books"] == 0
        assert stats["available_books"] == 0
        assert stats["checked_out_books"] == 0
        assert stats["checkout_rate"] == 0.0
    
    def test_populated_library_stats(self, populated_library):
        """Test stats for library with books."""
        checkout_book(populated_library, "9780134685991")
        
        stats = get_library_stats(populated_library)
        
        assert stats["total_books"] == 3
        assert stats["available_books"] == 2
        assert stats["checked_out_books"] == 1
        assert stats["checkout_rate"] == pytest.approx(1/3)


class TestClearLibrary:
    """Tests for clear_library function."""
    
    def test_clear_empty_library(self):
        """Test clearing empty library."""
        lib = {}
        clear_library(lib)
        assert lib == {}
    
    def test_clear_populated_library(self, populated_library):
        """Test clearing library with books."""
        clear_library(populated_library)
        assert populated_library == {}


# =============================================================================
# Integration Tests
# =============================================================================

class TestLibraryWorkflow:
    """End-to-end workflow tests."""
    
    def test_full_checkout_return_cycle(self, empty_library):
        """Test complete checkout and return cycle."""
        # Add book
        add_book(empty_library, "Test Book", "Test Author", "9780134685991")
        assert is_book_available(empty_library, "9780134685991") is True
        
        # Checkout
        checkout_book(empty_library, "9780134685991")
        assert is_book_available(empty_library, "9780134685991") is False
        assert len(list_checked_out_books(empty_library)) == 1
        
        # Return
        return_book(empty_library, "9780134685991")
        assert is_book_available(empty_library, "9780134685991") is True
        assert len(list_available_books(empty_library)) == 1
    
    def test_persistence_workflow(self, empty_library, temp_dir):
        """Test save and reload preserves state including checkout status."""
        filepath = os.path.join(temp_dir, "workflow_library.json")
        
        # Setup library
        add_book(empty_library, "Book 1", "Author 1", "9780134685991")
        add_book(empty_library, "Book 2", "Author 2", "9780132350884")
        checkout_book(empty_library, "9780134685991")
        
        # Save
        save_library(empty_library, filepath)
        
        # Load into new library
        loaded = load_library(filepath)
        
        # Verify state
        assert len(loaded) == 2
        assert loaded["9780134685991"]["available"] is False
        assert loaded["9780134685991"]["checked_out_at"] is not None
        assert loaded["9780132350884"]["available"] is True
    
    def test_search_and_operations(self, populated_library):
        """Test search results can be used for operations."""
        # Search for Python books
        results = search_books(populated_library, "Python")
        isbn = results[0]["isbn"]
        
        # Checkout using ISBN from search
        checkout_book(populated_library, isbn)
        
        # Verify
        assert not is_book_available(populated_library, isbn)
