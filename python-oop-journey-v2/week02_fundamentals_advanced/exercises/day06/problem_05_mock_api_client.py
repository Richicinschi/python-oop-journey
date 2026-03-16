"""Problem 05: Mock API Client

Topic: Mocking external dependencies with unittest.mock
Difficulty: Medium

Create an API client class and test it using mocks to avoid real network calls.

Your task:
    1. Implement the API client methods
    2. Write tests that mock the requests library
    3. Verify the client handles responses and errors correctly

Example:
    >>> client = APIClient("https://api.example.com")
    >>> user = client.get_user(123)  # Makes HTTP GET request
    >>> client.create_post({"title": "Hello", "body": "World"})

Hints:
    * Hint 1: Mocking replaces real objects with test doubles. Use
      @patch('module.Class.method') to replace the method during the test.
      The mock is passed as an argument to your test function.
    
    * Hint 2: Create a Mock response object and configure it:
      - mock_response.json.return_value = {"id": 1, "name": "Alice"}
      - mock_response.raise_for_status.return_value = None (for success)
      - Or use side_effect to raise exceptions for error testing
      - Assign: mock_get.return_value = mock_response
    
    * Hint 3: To test error handling:
      - HTTP errors: mock_response.raise_for_status.side_effect = HTTPError(...)
      - Network errors: mock_get.side_effect = RequestException(...)
      - Assert your APIError is raised with pytest.raises(APIError)

Debugging Tips:
    - "Mock not called": Check your patch path - it must match where
      the object is USED, not where it's defined
    - "Wrong URL format": Ensure base_url doesn't have trailing slash
      when you concatenate with endpoint paths
    - "Response has no json method": You need to set return_value on
      the mock method, not the Mock class itself
    - Tests making real HTTP calls: Your patch isn't working - verify
      the import path matches exactly where requests is called
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests


class APIError(Exception):
    """Raised when API request fails."""
    pass


class APIClient:
    """Client for making API requests.

    This client wraps the requests library and provides
    a higher-level interface for API operations.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None) -> None:
        """Initialize the API client.

        Args:
            base_url: The base URL for the API.
            api_key: Optional API key for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Fetch a user by ID.

        Args:
            user_id: The ID of the user to fetch.

        Returns:
            Dictionary containing user data.

        Raises:
            APIError: If the request fails or user not found.
        """
        # TODO: Implement GET request for user
        raise NotImplementedError("Implement get_user")

    def create_post(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Create a new post.

        Args:
            data: Dictionary with 'title' and 'body' keys.

        Returns:
            Dictionary containing the created post.

        Raises:
            APIError: If the request fails.
        """
        # TODO: Implement POST request for creating a post
        raise NotImplementedError("Implement create_post")

    def delete_post(self, post_id: int) -> bool:
        """Delete a post by ID.

        Args:
            post_id: The ID of the post to delete.

        Returns:
            True if deletion was successful.

        Raises:
            APIError: If the request fails.
        """
        # TODO: Implement DELETE request for post
        raise NotImplementedError("Implement delete_post")

    def search_users(self, query: str) -> list[Dict[str, Any]]:
        """Search for users by name.

        Args:
            query: Search query string.

        Returns:
            List of user dictionaries matching the query.

        Raises:
            APIError: If the request fails.
        """
        # TODO: Implement GET request for user search
        raise NotImplementedError("Implement search_users")


# TODO: Write tests using unittest.mock to mock requests
# Use @patch('requests.Session.get') or @patch('requests.Session.request')
# to avoid making real HTTP calls in tests.
#
# Example:
# @patch('requests.Session.get')
# def test_get_user_success(mock_get):
#     mock_response = Mock()
#     mock_response.json.return_value = {"id": 1, "name": "Alice"}
#     mock_response.raise_for_status.return_value = None
#     mock_get.return_value = mock_response
#     
#     client = APIClient("https://api.example.com")
#     user = client.get_user(1)
#     assert user["name"] == "Alice"
