"""Reference solution for Problem 06: Book and EBook."""

from __future__ import annotations


class Book:
    """Base class for all books."""
    
    def __init__(self, title: str, author: str, isbn: str, 
                 publication_year: int, genre: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.genre = genre
    
    def get_book_info(self) -> str:
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"ISBN: {self.isbn}\n"
                f"Year: {self.publication_year}\n"
                f"Genre: {self.genre}")
    
    def get_format(self) -> str:
        return "Unknown"
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        return 0
    
    def is_available(self) -> bool:
        return True


class EBook(Book):
    """An electronic book."""
    
    def __init__(self, title: str, author: str, isbn: str,
                 publication_year: int, genre: str, file_size_mb: float,
                 file_format: str, has_drm: bool = False) -> None:
        super().__init__(title, author, isbn, publication_year, genre)
        self.file_size_mb = file_size_mb
        self.file_format = file_format
        self.has_drm = has_drm
        self._download_count = 0
    
    def get_book_info(self) -> str:
        base = super().get_book_info()
        return (f"{base}\n"
                f"Format: Digital ({self.file_format})\n"
                f"Size: {self.file_size_mb} MB\n"
                f"DRM: {'Yes' if self.has_drm else 'No'}")
    
    def get_format(self) -> str:
        return "Digital"
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        estimated_words = self.file_size_mb * 500
        return int(estimated_words / words_per_minute)
    
    def download(self) -> str:
        self._download_count += 1
        return f"Downloading {self.title} ({self.file_size_mb} MB)..."
    
    def remove_drm(self) -> bool:
        if self.has_drm:
            self.has_drm = False
            return True
        return False


class PrintedBook(Book):
    """A physical printed book."""
    
    def __init__(self, title: str, author: str, isbn: str,
                 publication_year: int, genre: str, page_count: int,
                 cover_type: str, weight_grams: float, condition: str = "new") -> None:
        super().__init__(title, author, isbn, publication_year, genre)
        self.page_count = page_count
        self.cover_type = cover_type
        self.weight_grams = weight_grams
        self.condition = condition
        self._is_checked_out = False
    
    def get_book_info(self) -> str:
        base = super().get_book_info()
        return (f"{base}\n"
                f"Format: Physical\n"
                f"Pages: {self.page_count}\n"
                f"Cover: {self.cover_type}\n"
                f"Weight: {self.weight_grams}g")
    
    def get_format(self) -> str:
        return "Physical"
    
    def calculate_reading_time(self, words_per_minute: int = 250) -> int:
        estimated_words = self.page_count * 275
        return int(estimated_words / words_per_minute)
    
    def is_available(self) -> bool:
        return not self._is_checked_out
    
    def checkout(self) -> bool:
        if not self._is_checked_out:
            self._is_checked_out = True
            return True
        return False
    
    def return_book(self) -> None:
        self._is_checked_out = False
    
    def update_condition(self, new_condition: str) -> None:
        self.condition = new_condition
