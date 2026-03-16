"""Problem 05: Configure Settings - Solution."""

from __future__ import annotations


def configure_settings(
    theme: str = "light",
    font_size: int = 12,
    show_line_numbers: bool = True,
    auto_save: bool = False,
) -> dict[str, str | int | bool]:
    """Create application settings configuration.

    Args:
        theme: UI theme ("light" or "dark"). Default is "light".
        font_size: Font size in points. Default is 12.
        show_line_numbers: Whether to show line numbers. Default is True.
        auto_save: Whether to auto-save changes. Default is False.

    Returns:
        Dictionary containing all settings.
    """
    return {
        "theme": theme,
        "font_size": font_size,
        "show_line_numbers": show_line_numbers,
        "auto_save": auto_save,
    }
