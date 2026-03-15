"""API dependencies package.

This package contains FastAPI dependencies for authentication, authorization,
and other cross-cutting concerns.
"""

from .auth import (
    get_current_user_id,
    get_current_user_id_optional,
    require_auth,
    get_current_user,
    get_optional_user,
    verify_token_for_websocket,
)

__all__ = [
    "get_current_user_id",
    "get_current_user_id_optional",
    "require_auth",
    "get_current_user",
    "get_optional_user",
    "verify_token_for_websocket",
]
