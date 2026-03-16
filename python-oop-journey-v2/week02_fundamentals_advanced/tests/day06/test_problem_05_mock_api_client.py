"""Tests for Problem 05: Mock API Client."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
import requests

from week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client import (
    APIClient,
    APIError,
)


class TestAPIClientInit:
    """Tests for APIClient initialization."""

    def test_init_without_api_key(self) -> None:
        """Test initialization without API key."""
        client = APIClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        assert client.api_key is None

    def test_init_with_api_key(self) -> None:
        """Test initialization with API key sets authorization header."""
        client = APIClient("https://api.example.com", api_key="secret123")
        assert client.api_key == "secret123"
        assert client.session.headers["Authorization"] == "Bearer secret123"

    def test_init_trailing_slash_removed(self) -> None:
        """Test that trailing slash is removed from base_url."""
        client = APIClient("https://api.example.com/")
        assert client.base_url == "https://api.example.com"


class TestGetUser:
    """Tests for get_user method."""

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_get_user_success(self, mock_get) -> None:
        """Test successful user fetch."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = APIClient("https://api.example.com")
        user = client.get_user(1)

        assert user["name"] == "Alice"
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_get_user_not_found(self, mock_get) -> None:
        """Test user not found raises APIError."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        client = APIClient("https://api.example.com")
        with pytest.raises(APIError, match="Failed to fetch user"):
            client.get_user(999)

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_get_user_network_error(self, mock_get) -> None:
        """Test network error raises APIError."""
        mock_get.side_effect = requests.RequestException("Connection refused")

        client = APIClient("https://api.example.com")
        with pytest.raises(APIError, match="Request failed"):
            client.get_user(1)

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_get_user_with_api_key(self, mock_get) -> None:
        """Test that API key is used in session headers."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "name": "Alice"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = APIClient("https://api.example.com", api_key="my_key")
        client.get_user(1)

        # Verify the request was made
        mock_get.assert_called_once()


class TestCreatePost:
    """Tests for create_post method."""

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.post")
    def test_create_post_success(self, mock_post) -> None:
        """Test successful post creation."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "title": "Test", "body": "Content"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = APIClient("https://api.example.com")
        post = client.create_post({"title": "Test", "body": "Content"})

        assert post["title"] == "Test"
        mock_post.assert_called_once_with(
            "https://api.example.com/posts",
            json={"title": "Test", "body": "Content"}
        )

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.post")
    def test_create_post_api_error(self, mock_post) -> None:
        """Test API error during post creation."""
        mock_post.side_effect = requests.RequestException("Server error")

        client = APIClient("https://api.example.com")
        with pytest.raises(APIError, match="Failed to create post"):
            client.create_post({"title": "Test"})


class TestDeletePost:
    """Tests for delete_post method."""

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.delete")
    def test_delete_post_success(self, mock_delete) -> None:
        """Test successful post deletion."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        client = APIClient("https://api.example.com")
        result = client.delete_post(1)

        assert result is True
        mock_delete.assert_called_once_with("https://api.example.com/posts/1")

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.delete")
    def test_delete_post_not_found(self, mock_delete) -> None:
        """Test deleting non-existent post raises APIError."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_delete.return_value = mock_response

        client = APIClient("https://api.example.com")
        with pytest.raises(APIError, match="Failed to delete post"):
            client.delete_post(999)


class TestSearchUsers:
    """Tests for search_users method."""

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_search_users_success(self, mock_get) -> None:
        """Test successful user search."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Alex"},
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = APIClient("https://api.example.com")
        users = client.search_users("al")

        assert len(users) == 2
        mock_get.assert_called_once_with(
            "https://api.example.com/users",
            params={"q": "al"}
        )

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_search_users_empty_results(self, mock_get) -> None:
        """Test search returning no results."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        client = APIClient("https://api.example.com")
        users = client.search_users("xyz")

        assert users == []

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session.get")
    def test_search_users_network_error(self, mock_get) -> None:
        """Test network error during search."""
        mock_get.side_effect = requests.RequestException("Timeout")

        client = APIClient("https://api.example.com")
        with pytest.raises(APIError, match="Failed to search users"):
            client.search_users("test")


class TestAPIClientIntegration:
    """Integration-style tests with multiple mocked operations."""

    @patch("week02_fundamentals_advanced.solutions.day06.problem_05_mock_api_client.requests.Session")
    def test_multiple_operations_same_session(self, mock_session_class) -> None:
        """Test that multiple operations use the same session."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        # Setup successful responses
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response

        client = APIClient("https://api.example.com")

        # Make multiple requests
        client.get_user(1)
        client.get_user(2)

        # Session should be reused
        assert mock_session.get.call_count == 2

    def test_api_error_is_exception_subclass(self) -> None:
        """Test that APIError is a proper Exception subclass."""
        assert issubclass(APIError, Exception)
        err = APIError("test message")
        assert str(err) == "test message"
