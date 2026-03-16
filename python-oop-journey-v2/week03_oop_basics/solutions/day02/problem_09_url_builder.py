"""Solution for Problem 09: URL Builder."""

from __future__ import annotations


class URLBuilder:
    """Utility class for building and manipulating URLs."""
    
    @staticmethod
    def build(host: str, path: str, secure: bool = True) -> str:
        """Build a complete URL from host and path.
        
        Args:
            host: The host (e.g., "api.example.com")
            path: The path (e.g., "/users")
            secure: Whether to use HTTPS (default) or HTTP
            
        Returns:
            Complete URL
        """
        protocol = "https" if secure else "http"
        # Normalize path to start with /
        if not path.startswith("/"):
            path = "/" + path
        return f"{protocol}://{host}{path}"
    
    @staticmethod
    def add_query_param(url: str, key: str, value: str) -> str:
        """Add a query parameter to a URL.
        
        Args:
            url: Base URL or path
            key: Query parameter key
            value: Query parameter value
            
        Returns:
            URL with added query parameter
        """
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{key}={value}"
    
    @staticmethod
    def join_paths(*parts: str) -> str:
        """Join path parts with slashes.
        
        Handles leading/trailing slashes to avoid double slashes.
        
        Args:
            *parts: Path parts to join
            
        Returns:
            Joined path
        """
        if not parts:
            return ""
        
        # Normalize each part by stripping slashes
        normalized = []
        for i, part in enumerate(parts):
            if i == 0:
                # Keep leading slash for first part if present
                if part.startswith("/"):
                    normalized.append("/" + part.strip("/"))
                else:
                    normalized.append(part.strip("/"))
            else:
                normalized.append(part.strip("/"))
        
        # Join with /
        result = "/".join(normalized)
        
        # Ensure leading slash if first part had one
        return result
    
    @staticmethod
    def normalize(url: str) -> str:
        """Normalize a URL by removing extra slashes.
        
        Removes leading/trailing slashes and duplicate internal slashes.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        # Split by // and filter out empty strings, then rejoin with /
        parts = [p for p in url.split("/") if p]
        return "/".join(parts)
