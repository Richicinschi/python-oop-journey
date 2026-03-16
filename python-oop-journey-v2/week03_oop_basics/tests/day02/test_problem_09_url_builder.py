"""Tests for Problem 09: URL Builder."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day02.problem_09_url_builder import URLBuilder


class TestBuild:
    """Test suite for build static method."""
    
    def test_build_https(self) -> None:
        """Test building HTTPS URL."""
        result = URLBuilder.build("api.example.com", "/users")
        assert result == "https://api.example.com/users"
    
    def test_build_http(self) -> None:
        """Test building HTTP URL."""
        result = URLBuilder.build("api.example.com", "/users", secure=False)
        assert result == "http://api.example.com/users"
    
    def test_build_path_without_leading_slash(self) -> None:
        """Test build with path missing leading slash."""
        result = URLBuilder.build("api.example.com", "users")
        assert result == "https://api.example.com/users"
    
    def test_build_nested_path(self) -> None:
        """Test build with nested path."""
        result = URLBuilder.build("api.example.com", "/v1/users/123")
        assert result == "https://api.example.com/v1/users/123"


class TestAddQueryParam:
    """Test suite for add_query_param static method."""
    
    def test_add_first_param(self) -> None:
        """Test adding first query parameter."""
        result = URLBuilder.add_query_param("/users", "page", "1")
        assert result == "/users?page=1"
    
    def test_add_second_param(self) -> None:
        """Test adding second query parameter."""
        result = URLBuilder.add_query_param("/users?page=1", "limit", "10")
        assert result == "/users?page=1&limit=10"
    
    def test_add_to_full_url(self) -> None:
        """Test adding param to full URL."""
        result = URLBuilder.add_query_param("https://api.com/users", "id", "123")
        assert result == "https://api.com/users?id=123"
    
    def test_add_multiple_params(self) -> None:
        """Test adding multiple params."""
        url = "/users"
        url = URLBuilder.add_query_param(url, "page", "1")
        url = URLBuilder.add_query_param(url, "limit", "10")
        url = URLBuilder.add_query_param(url, "sort", "name")
        assert url == "/users?page=1&limit=10&sort=name"


class TestJoinPaths:
    """Test suite for join_paths static method."""
    
    def test_join_simple(self) -> None:
        """Test joining simple paths."""
        result = URLBuilder.join_paths("api", "v1", "users")
        assert result == "api/v1/users"
    
    def test_join_with_slashes(self) -> None:
        """Test joining paths with slashes."""
        result = URLBuilder.join_paths("/api/", "/v1/", "/users")
        assert result == "/api/v1/users"
    
    def test_join_mixed(self) -> None:
        """Test joining mixed paths."""
        result = URLBuilder.join_paths("/api/v1", "users", "123/")
        assert result == "/api/v1/users/123"
    
    def test_join_single(self) -> None:
        """Test joining single path."""
        result = URLBuilder.join_paths("/users")
        assert result == "/users"
    
    def test_join_empty(self) -> None:
        """Test joining no paths."""
        result = URLBuilder.join_paths()
        assert result == ""


class TestNormalize:
    """Test suite for normalize static method."""
    
    def test_normalize_double_slashes(self) -> None:
        """Test normalizing double slashes."""
        result = URLBuilder.normalize("//api.example.com//users//")
        assert result == "api.example.com/users"
    
    def test_normalize_leading_slash(self) -> None:
        """Test normalizing leading slash."""
        result = URLBuilder.normalize("/users/123")
        assert result == "users/123"
    
    def test_normalize_trailing_slash(self) -> None:
        """Test normalizing trailing slash."""
        result = URLBuilder.normalize("users/123/")
        assert result == "users/123"
    
    def test_normalize_multiple_internal(self) -> None:
        """Test normalizing multiple internal slashes."""
        result = URLBuilder.normalize("api///v1//users")
        assert result == "api/v1/users"
    
    def test_normalize_simple(self) -> None:
        """Test normalizing already clean path."""
        result = URLBuilder.normalize("api/v1/users")
        assert result == "api/v1/users"


class TestCombinedOperations:
    """Test combined URL building operations."""
    
    def test_complex_url_construction(self) -> None:
        """Test building a complex URL step by step."""
        path = URLBuilder.join_paths("/api", "v1", "users")
        url = URLBuilder.build("example.com", path)
        url = URLBuilder.add_query_param(url, "page", "1")
        url = URLBuilder.add_query_param(url, "limit", "10")
        assert url == "https://example.com/api/v1/users?page=1&limit=10"
