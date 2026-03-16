"""Problem 02: Decorator Text Formatting

Topic: Decorator Pattern
Difficulty: Medium

Implement a flexible text formatting system using the Decorator pattern.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class TextComponent(ABC):
    """Component interface - defines the interface for text objects.
    
    Both concrete components and decorators implement this interface.
    """
    
    @abstractmethod
    def render(self) -> str:
        """Return the formatted text content.
        
        Returns:
            The text content as a string
        """
        raise NotImplementedError("Implement render")
    
    @abstractmethod
    def get_length(self) -> int:
        """Return the length of the raw text (without formatting).
        
        Returns:
            Number of characters in the raw text
        """
        raise NotImplementedError("Implement get_length")


class PlainText(TextComponent):
    """Concrete component - represents simple unformatted text.
    
    This is the base object that decorators will wrap.
    """
    
    def __init__(self, text: str) -> None:
        """Initialize with plain text.
        
        Args:
            text: The raw text content
        """
        raise NotImplementedError("Implement __init__")
    
    def render(self) -> str:
        """Return the plain text as-is."""
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return the length of the plain text."""
        raise NotImplementedError("Implement get_length")


class TextDecorator(TextComponent, ABC):
    """Base decorator class - wraps a TextComponent.
    
    Maintains a reference to a wrapped component and delegates operations to it.
    """
    
    def __init__(self, wrapped: TextComponent) -> None:
        """Initialize with component to wrap.
        
        Args:
            wrapped: The TextComponent to decorate
        """
        raise NotImplementedError("Implement __init__")


class BoldDecorator(TextDecorator):
    """Concrete decorator - adds bold formatting.
    
    Wraps text with ** markers to indicate bold.
    """
    
    def render(self) -> str:
        """Return text wrapped in bold markers.
        
        Returns:
            Text wrapped with '**' on both sides
        """
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        raise NotImplementedError("Implement get_length")


class ItalicDecorator(TextDecorator):
    """Concrete decorator - adds italic formatting.
    
    Wraps text with * markers to indicate italic.
    """
    
    def render(self) -> str:
        """Return text wrapped in italic markers.
        
        Returns:
            Text wrapped with '*' on both sides
        """
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        raise NotImplementedError("Implement get_length")


class UnderlineDecorator(TextDecorator):
    """Concrete decorator - adds underline formatting.
    
    Wraps text with __ markers to indicate underline.
    """
    
    def render(self) -> str:
        """Return text wrapped in underline markers.
        
        Returns:
            Text wrapped with '__' on both sides
        """
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        raise NotImplementedError("Implement get_length")


class ColorDecorator(TextDecorator):
    """Concrete decorator - adds color formatting.
    
    Wraps text with [color:name]...[/color] tags.
    """
    
    def __init__(self, wrapped: TextComponent, color: str) -> None:
        """Initialize with wrapped component and color.
        
        Args:
            wrapped: The TextComponent to decorate
            color: The color name (e.g., 'red', 'blue')
        """
        raise NotImplementedError("Implement __init__")
    
    def render(self) -> str:
        """Return text wrapped in color tags.
        
        Returns:
            Text wrapped with [color:X]...[/color] tags
        """
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        raise NotImplementedError("Implement get_length")


class StrikethroughDecorator(TextDecorator):
    """Concrete decorator - adds strikethrough formatting.
    
    Wraps text with ~~ markers to indicate strikethrough.
    """
    
    def render(self) -> str:
        """Return text wrapped in strikethrough markers.
        
        Returns:
            Text wrapped with '~~' on both sides
        """
        raise NotImplementedError("Implement render")
    
    def get_length(self) -> int:
        """Return length of wrapped component's raw text."""
        raise NotImplementedError("Implement get_length")


class TextFormatter:
    """Utility class for building formatted text.
    
    Provides a fluent interface for applying multiple decorators.
    """
    
    def __init__(self, text: str) -> None:
        """Initialize with plain text.
        
        Args:
            text: The initial plain text
        """
        raise NotImplementedError("Implement __init__")
    
    def bold(self) -> TextFormatter:
        """Apply bold formatting and return self for chaining.
        
        Returns:
            self for method chaining
        """
        raise NotImplementedError("Implement bold")
    
    def italic(self) -> TextFormatter:
        """Apply italic formatting and return self for chaining.
        
        Returns:
            self for method chaining
        """
        raise NotImplementedError("Implement italic")
    
    def underline(self) -> TextFormatter:
        """Apply underline formatting and return self for chaining.
        
        Returns:
            self for method chaining
        """
        raise NotImplementedError("Implement underline")
    
    def color(self, color_name: str) -> TextFormatter:
        """Apply color formatting and return self for chaining.
        
        Args:
            color_name: The color to apply
            
        Returns:
            self for method chaining
        """
        raise NotImplementedError("Implement color")
    
    def strikethrough(self) -> TextFormatter:
        """Apply strikethrough formatting and return self for chaining.
        
        Returns:
            self for method chaining
        """
        raise NotImplementedError("Implement strikethrough")
    
    def build(self) -> TextComponent:
        """Return the fully decorated text component.
        
        Returns:
            The TextComponent with all decorators applied
        """
        raise NotImplementedError("Implement build")
    
    def render(self) -> str:
        """Convenience method to render the formatted text.
        
        Returns:
            The fully formatted text string
        """
        raise NotImplementedError("Implement render")
