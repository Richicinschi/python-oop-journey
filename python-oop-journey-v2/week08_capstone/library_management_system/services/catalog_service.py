"""Catalog service with Strategy pattern for search."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..domain.book import Book, BookCopy
from ..domain.enums import CopyStatus
from ..repositories.book_repository import BookRepository


@dataclass
class SearchResult:
    """Result of a catalog search."""

    book: Book
    score: float  # Relevance score (higher is better)


class SearchStrategy(ABC):
    """Abstract strategy for book searching.

    Strategy Pattern: Allows interchangeable search algorithms.
    """

    @abstractmethod
    def search(self, query: str, books: list[Book]) -> list[SearchResult]:
        """Execute search strategy."""
        raise NotImplementedError


class TitleSearchStrategy(SearchStrategy):
    """Search books by title."""

    def search(self, query: str, books: list[Book]) -> list[SearchResult]:
        """Search for books where title contains the query."""
        query_lower = query.lower()
        results = []
        for book in books:
            title_lower = book.title.lower()
            if query_lower in title_lower:
                # Calculate relevance score
                score = self._calculate_score(query_lower, title_lower)
                results.append(SearchResult(book=book, score=score))
        return sorted(results, key=lambda r: r.score, reverse=True)

    def _calculate_score(self, query: str, title: str) -> float:
        """Calculate relevance score based on match quality."""
        if query == title:
            return 1.0
        if title.startswith(query):
            return 0.8
        # Word boundary match
        words = title.split()
        for word in words:
            if word.startswith(query):
                return 0.6
        return 0.4


class AuthorSearchStrategy(SearchStrategy):
    """Search books by author."""

    def search(self, query: str, books: list[Book]) -> list[SearchResult]:
        """Search for books where any author matches the query."""
        query_lower = query.lower()
        results = []
        for book in books:
            for author in book.authors:
                author_lower = author.lower()
                if query_lower in author_lower:
                    score = self._calculate_score(query_lower, author_lower)
                    results.append(SearchResult(book=book, score=score))
                    break  # Only count each book once
        return sorted(results, key=lambda r: r.score, reverse=True)

    def _calculate_score(self, query: str, author: str) -> float:
        """Calculate relevance score based on match quality."""
        if query == author:
            return 1.0
        if author.startswith(query):
            return 0.8
        return 0.5


class GenreSearchStrategy(SearchStrategy):
    """Search books by genre."""

    def search(self, query: str, books: list[Book]) -> list[SearchResult]:
        """Search for books matching the genre."""
        query_lower = query.lower()
        results = []
        for book in books:
            if query_lower in book.genre.lower():
                # Genre matches are all equal weight
                results.append(SearchResult(book=book, score=0.7))
        return results


class CompoundSearchStrategy(SearchStrategy):
    """Search using multiple strategies and combine results."""

    def __init__(self, strategies: Optional[list[SearchStrategy]] = None) -> None:
        self.strategies = strategies or [
            TitleSearchStrategy(),
            AuthorSearchStrategy(),
            GenreSearchStrategy(),
        ]

    def search(self, query: str, books: list[Book]) -> list[SearchResult]:
        """Search using all strategies and merge results."""
        all_results: dict[str, SearchResult] = {}

        for strategy in self.strategies:
            results = strategy.search(query, books)
            for result in results:
                if result.book.isbn in all_results:
                    # Merge scores (take higher score)
                    existing = all_results[result.book.isbn]
                    if result.score > existing.score:
                        existing.score = result.score
                else:
                    all_results[result.book.isbn] = result

        return sorted(all_results.values(), key=lambda r: r.score, reverse=True)


class CatalogService:
    """Service for managing the book catalog.

    Uses Strategy Pattern for flexible search capabilities.
    """

    def __init__(
        self,
        book_repository: BookRepository,
        search_strategy: Optional[SearchStrategy] = None,
    ) -> None:
        self._repo = book_repository
        self._search_strategy = search_strategy or CompoundSearchStrategy()

    def add_book(self, book: Book) -> Book:
        """Add a new book to the catalog."""
        return self._repo.save_book(book)

    def get_book(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        return self._repo.find_book_by_isbn(isbn)

    def add_copy(self, book_isbn: str, copy: BookCopy) -> Optional[BookCopy]:
        """Add a copy to an existing book."""
        book = self._repo.find_book_by_isbn(book_isbn)
        if book:
            book.add_copy(copy)
            return self._repo.save_copy(copy)
        return None

    def get_copy(self, barcode: str) -> Optional[BookCopy]:
        """Get a book copy by barcode."""
        return self._repo.find_copy_by_barcode(barcode)

    def get_copies_for_book(self, isbn: str) -> list[BookCopy]:
        """Get all copies of a specific book."""
        return self._repo.find_copies_by_isbn(isbn)

    def get_available_copies(self, isbn: str) -> list[BookCopy]:
        """Get available copies of a specific book."""
        return self._repo.find_available_copies_by_isbn(isbn)

    def is_book_available(self, isbn: str) -> bool:
        """Check if any copy of the book is available."""
        copies = self._repo.find_available_copies_by_isbn(isbn)
        return len(copies) > 0

    def search(self, query: str) -> list[SearchResult]:
        """Search the catalog using the current search strategy."""
        all_books = self._repo.get_all_books()
        return self._search_strategy.search(query, all_books)

    def search_by_title(self, title: str) -> list[Book]:
        """Search books by title."""
        return self._repo.find_books_by_title(title)

    def search_by_author(self, author: str) -> list[Book]:
        """Search books by author."""
        return self._repo.find_books_by_author(author)

    def search_by_genre(self, genre: str) -> list[Book]:
        """Search books by genre."""
        return self._repo.find_books_by_genre(genre)

    def set_search_strategy(self, strategy: SearchStrategy) -> None:
        """Change the search strategy (Strategy Pattern)."""
        self._search_strategy = strategy

    def list_all_books(self) -> list[Book]:
        """List all books in the catalog."""
        return self._repo.get_all_books()

    def remove_book(self, isbn: str) -> bool:
        """Remove a book and all its copies from the catalog."""
        return self._repo.delete_book(isbn)

    def remove_copy(self, barcode: str) -> bool:
        """Remove a specific book copy."""
        return self._repo.delete_copy(barcode)

    def get_catalog_statistics(self) -> dict:
        """Get statistics about the catalog."""
        books = self._repo.get_all_books()
        copies = self._repo.get_all_copies()

        available_copies = sum(1 for c in copies if c.status == CopyStatus.AVAILABLE)

        return {
            "total_books": len(books),
            "total_copies": len(copies),
            "available_copies": available_copies,
            "checked_out_copies": len(copies) - available_copies,
        }
