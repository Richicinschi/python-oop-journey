"""Problem 06: Book and EBook

Topic: Media Inheritance with Format Differences
Difficulty: Medium

Create a Book base class with EBook and PrintedBook subclasses,
demonstrating format-specific behaviors.
"""

from __future__ import annotations


class Book:
    """Base class for all books.
    
    Attributes:
        title: Book title
        author: Book author
        isbn: International Standard Book Number
        publication_year: Year of publication
        genre: Book genre/category
    """
    
    def __init__(self, title: str, author: str, isbn: str, 
                 publication_year: int, genre: str) -> None:
        """Initialize a Book.
        
        Args:
            title: Book title
            author: Book author
            isbn: ISBN identifier
            publication_year: Year published
            genre: Book genre
        """
        raise NotImplementedError("Implement Book.__init__")
    
    def get_book_info(self) -> str:
        """Return formatted book information.
        
        Returns:
            Multi-line string with book details
        """
        raise NotImplementedError("Implement Book.get_book_info")
    
    def get_format(self) -> str:
        """Return the book format.
        
        Returns:
            "Unknown"
        """
        raise NotImplementedError("Implement Book.get_format")
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        """Estimate reading time in minutes.
        
        Args:
            words_per_minute: Reading speed (default 250)
            
        Returns:
            Estimated minutes to read (base implementation returns 0)
        """
        raise NotImplementedError("Implement Book.calculate_reading_time")
    
    def is_available(self) -> bool:
        """Check if book is available for reading.
        
        Returns:
            True by default
        """
        raise NotImplementedError("Implement Book.is_available")


class EBook(Book):
    """An electronic book.
    
    Additional Attributes:
        file_size_mb: Size of the ebook file in MB
        file_format: Format (e.g., "EPUB", "PDF", "MOBI")
        has_drm: Whether DRM protection is enabled
        download_count: Number of times downloaded
    """
    
    def __init__(self, title: str, author: str, isbn: str,
                 publication_year: int, genre: str, file_size_mb: float,
                 file_format: str, has_drm: bool = False) -> None:
        """Initialize an EBook.
        
        Args:
            title: Book title
            author: Book author
            isbn: ISBN identifier
            publication_year: Year published
            genre: Book genre
            file_size_mb: File size in megabytes
            file_format: File format (EPUB, PDF, etc.)
            has_drm: Whether DRM is enabled
        """
        raise NotImplementedError("Implement EBook.__init__")
    
    def get_book_info(self) -> str:
        """Override: Include digital format details.
        
        Returns:
            Base info + "Format: X, Size: Y MB, DRM: Z"
        """
        raise NotImplementedError("Implement EBook.get_book_info")
    
    def get_format(self) -> str:
        """Override: Return "Digital".
        
        Returns:
            "Digital"
        """
        raise NotImplementedError("Implement EBook.get_format")
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        """Override: Estimate based on file size.
        
        Assumes approximately 500 words per MB for ebooks.
        
        Args:
            words_per_minute: Reading speed
            
        Returns:
            Estimated reading time in minutes
        """
        raise NotImplementedError("Implement EBook.calculate_reading_time")
    
    def download(self) -> str:
        """EBook-specific: Simulate downloading.
        
        Increments download_count.
        
        Returns:
            Download success message with file size
        """
        raise NotImplementedError("Implement EBook.download")
    
    def remove_drm(self) -> bool:
        """EBook-specific: Attempt to remove DRM.
        
        Returns:
            True if DRM was present and removed
            False if no DRM was present
        """
        raise NotImplementedError("Implement EBook.remove_drm")


class PrintedBook(Book):
    """A physical printed book.
    
    Additional Attributes:
        page_count: Number of pages
        cover_type: "hardcover" or "paperback"
        weight_grams: Weight in grams
        is_checked_out: Whether book is currently borrowed
        condition: "new", "good", "fair", or "poor"
    """
    
    def __init__(self, title: str, author: str, isbn: str,
                 publication_year: int, genre: str, page_count: int,
                 cover_type: str, weight_grams: float, condition: str = "new") -> None:
        """Initialize a PrintedBook.
        
        Args:
            title: Book title
            author: Book author
            isbn: ISBN identifier
            publication_year: Year published
            genre: Book genre
            page_count: Number of pages
            cover_type: "hardcover" or "paperback"
            weight_grams: Book weight in grams
            condition: Current condition (default "new")
        """
        raise NotImplementedError("Implement PrintedBook.__init__")
    
    def get_book_info(self) -> str:
        """Override: Include physical format details.
        
        Returns:
            Base info + "Pages: X, Cover: Y, Weight: Zg"
        """
        raise NotImplementedError("Implement PrintedBook.get_book_info")
    
    def get_format(self) -> str:
        """Override: Return "Physical".
        
        Returns:
            "Physical"
        """
        raise NotImplementedError("Implement PrintedBook.get_format")
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        """Override: Estimate based on page count.
        
        Assumes approximately 275 words per page for printed books.
        
        Args:
            words_per_minute: Reading speed
            
        Returns:
            Estimated reading time in minutes
        """
        raise NotImplementedError("Implement PrintedBook.calculate_reading_time")
    
    def is_available(self) -> bool:
        """Override: Check if not checked out.
        
        Returns:
            True if not currently checked out
        """
        raise NotImplementedError("Implement PrintedBook.is_available")
    
    def checkout(self) -> bool:
        """PrintedBook-specific: Check out the book.
        
        Returns:
            True if successfully checked out
            False if already checked out
        """
        raise NotImplementedError("Implement PrintedBook.checkout")
    
    def return_book(self) -> None:
        """PrintedBook-specific: Return the book.
        
        Sets is_checked_out to False.
        """
        raise NotImplementedError("Implement PrintedBook.return_book")
    
    def update_condition(self, new_condition: str) -> None:
        """PrintedBook-specific: Update book condition.
        
        Args:
            new_condition: New condition value
        """
        raise NotImplementedError("Implement PrintedBook.update_condition")
