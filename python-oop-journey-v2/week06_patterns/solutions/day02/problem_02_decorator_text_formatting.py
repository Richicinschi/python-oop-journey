"""Reference solution for Problem 02: Decorator Text Formatting."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TextComponent(ABC):
    """Component interface - defines the interface for text objects."""
    
    @abstractmethod
    def render(self) -> str:
        """Return the formatted text content."""
        pass
    
    @abstractmethod
    def get_length(self) -> int:
        """Return the length of the raw text (without formatting)."""
        pass


class PlainText(TextComponent):
    """Concrete component - represents simple unformatted text."""
    
    def __init__(self, text: str) -> None:
        self._text = text
    
    def render(self) -> str:
        """Return the plain text as-is."""
        return self._text
    
    def get_length(self) -> int:
        """Return the length of the plain text."""
        return len(self._text)


class TextDecorator(TextComponent, ABC):
    """Base decorator class - wraps a TextComponent."""
    
    def __init__(self, wrapped: TextComponent) -> None:
        self._wrapped = wrapped


class BoldDecorator(TextDecorator):
    """Concrete decorator - adds bold formatting."""
    
    def render(self) -> str:
        """Return text wrapped in bold markers."""
        return f"**{self._wrapped.render()}**"
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        return self._wrapped.get_length()


class ItalicDecorator(TextDecorator):
    """Concrete decorator - adds italic formatting."""
    
    def render(self) -> str:
        """Return text wrapped in italic markers."""
        return f"*{self._wrapped.render()}*"
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        return self._wrapped.get_length()


class UnderlineDecorator(TextDecorator):
    """Concrete decorator - adds underline formatting."""
    
    def render(self) -> str:
        """Return text wrapped in underline markers."""
        return f"__{self._wrapped.render()}__"
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        return self._wrapped.get_length()


class ColorDecorator(TextDecorator):
    """Concrete decorator - adds color formatting."""
    
    def __init__(self, wrapped: TextComponent, color: str) -> None:
        super().__init__(wrapped)
        self._color = color
    
    def render(self) -> str:
        """Return text wrapped in color tags."""
        return f"[color:{self._color}]{self._wrapped.render()}[/color]"
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        return self._wrapped.get_length()


class StrikethroughDecorator(TextDecorator):
    """Concrete decorator - adds strikethrough formatting."""
    
    def render(self) -> str:
        """Return text wrapped in strikethrough markers."""
        return f"~~{self._wrapped.render()}~~"
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        return self._wrapped.get_length()


class TextFormatter:
    """Utility class for building formatted text."""
    
    def __init__(self, text: str) -> None:
        self._component: TextComponent = PlainText(text)
    
    def bold(self) -> TextFormatter:
        """Apply bold formatting and return self for chaining."""
        self._component = BoldDecorator(self._component)
        return self
    
    def italic(self) -> TextFormatter:
        """Apply italic formatting and return self for chaining."""
        self._component = ItalicDecorator(self._component)
        return self
    
    def underline(self) -> TextFormatter:
        """Apply underline formatting and return self for chaining."""
        self._component = UnderlineDecorator(self._component)
        return self
    
    def color(self, color_name: str) -> TextFormatter:
        """Apply color formatting and return self for chaining."""
        self._component = ColorDecorator(self._component, color_name)
        return self
    
    def strikethrough(self) -> TextFormatter:
        """Apply strikethrough formatting and return self for chaining."""
        self._component = StrikethroughDecorator(self._component)
        return self
    
    def build(self) -> TextComponent:
        """Return the fully decorated text component."""
        return self._component
    
    def render(self) -> str:
        """Convenience method to render the formatted text."""
        return self._component.render()
