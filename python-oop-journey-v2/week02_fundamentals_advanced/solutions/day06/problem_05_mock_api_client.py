"""Reference solution for Problem 05: Mock API Client."""

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
        url = f"{self.base_url}/users/{user_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise APIError(f"Failed to fetch user {user_id}: {e}") from e
        except requests.RequestException as e:
            raise APIError(f"Request failed: {e}") from e

    def create_post(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Create a new post.

        Args:
            data: Dictionary with 'title' and 'body' keys.

        Returns:
            Dictionary containing the created post.

        Raises:
            APIError: If the request fails.
        """
        url = f"{self.base_url}/posts"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to create post: {e}") from e

    def delete_post(self, post_id: int) -> bool:
        """Delete a post by ID.

        Args:
            post_id: The ID of the post to delete.

        Returns:
            True if deletion was successful.

        Raises:
            APIError: If the request fails.
        """
        url = f"{self.base_url}/posts/{post_id}"
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            raise APIError(f"Failed to delete post {post_id}: {e}") from e

    def search_users(self, query: str) -> list[Dict[str, Any]]:
        """Search for users by name.

        Args:
            query: Search query string.

        Returns:
            List of user dictionaries matching the query.

        Raises:
            APIError: If the request fails.
        """
        url = f"{self.base_url}/users"
        try:
            response = self.session.get(url, params={"q": query})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to search users: {e}") from e
