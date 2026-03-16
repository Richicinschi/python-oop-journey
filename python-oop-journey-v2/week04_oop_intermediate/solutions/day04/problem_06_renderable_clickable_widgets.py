"""Problem 06: Renderable Clickable Widgets.

Implement abstract base classes and mixins for UI widgets.

Classes to implement:
- Drawable: Abstract base for drawable objects
- Clickable: Abstract base for clickable objects  
- Button: A button that is both drawable and clickable
- Icon: A clickable icon
- Panel: A drawable panel (not clickable)

Example:
    >>> button = Button(10, 20, 100, 30, "Click Me")
    >>> button.draw()
    '+----------+\\n| Click Me |\\n+----------+'
    >>> button.on_click()
    "Button 'Click Me' was clicked!"
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Drawable(ABC):
    """Abstract base class for drawable objects.
    
    Subclasses must implement draw() and get_bounds().
    
    Attributes:
        x: X-coordinate.
        y: Y-coordinate.
        width: Width of the drawable.
        height: Height of the drawable.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """Initialize a drawable object.
        
        Args:
            x: X-coordinate.
            y: Y-coordinate.
            width: Width of the drawable.
            height: Height of the drawable.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @abstractmethod
    def draw(self) -> str:
        """Draw the object and return its string representation.
        
        Returns:
            String representation of the object.
        """
        pass
    
    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get the bounding box.
        
        Returns:
            Tuple of (x, y, width, height).
        """
        return (self.x, self.y, self.width, self.height)
    
    def area(self) -> int:
        """Calculate the area.
        
        Returns:
            Width * height.
        """
        return self.width * self.height


class Clickable(ABC):
    """Abstract base class for clickable objects.
    
    Subclasses must implement on_click().
    """
    
    @abstractmethod
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            Response message.
        """
        pass
    
    def is_hit(self, x: int, y: int) -> bool:
        """Check if point (x, y) hits this object.
        
        Requires the object to have get_bounds() method.
        
        Args:
            x: X-coordinate of the point.
            y: Y-coordinate of the point.
        
        Returns:
            True if point is within bounds.
        """
        bx, by, bw, bh = self.get_bounds()  # type: ignore[attr-defined]
        return bx <= x <= bx + bw and by <= y <= by + bh


class Button(Drawable, Clickable):
    """A button that can be drawn and clicked.
    
    The button is drawn as:
    +----------+
    | label    |
    +----------+
    
    Attributes:
        x: X-coordinate.
        y: Y-coordinate.
        width: Width of the button.
        height: Height of the button.
        label: Button label text.
    
    Args:
        x: X-coordinate.
        y: Y-coordinate.
        width: Width of the button.
        height: Height of the button.
        label: Button label.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, label: str) -> None:
        """Initialize a button.
        
        Args:
            x: X-coordinate.
            y: Y-coordinate.
            width: Width of the button.
            height: Height of the button.
            label: Button label.
        """
        super().__init__(x, y, width, height)
        self.label = label
    
    def draw(self) -> str:
        """Draw the button.
        
        Returns:
            ASCII representation of the button.
        """
        # Create a simple ASCII button
        label_width = len(self.label)
        # Ensure minimum width for the button
        inner_width = max(label_width, self.width - 2)
        
        # Build the button
        top_bottom = "+" + "-" * inner_width + "+"
        label_padded = self.label.center(inner_width)
        middle = f"|{label_padded}|"
        
        # Create height by adding empty lines if needed
        lines = [top_bottom]
        
        # Add middle section lines to match height
        content_height = self.height - 2  # Subtract top and bottom borders
        if content_height < 1:
            content_height = 1
        
        # Place label in middle of content area
        for i in range(content_height):
            if i == content_height // 2:
                lines.append(middle)
            else:
                lines.append("|" + " " * inner_width + "|")
        
        lines.append(top_bottom)
        
        return "\n".join(lines)
    
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            Click response message.
        """
        return f"Button '{self.label}' was clicked!"


class Icon(Drawable, Clickable):
    """A clickable icon.
    
    Drawn as a simple [icon_name] representation.
    
    Attributes:
        x: X-coordinate.
        y: Y-coordinate.
        size: Size of the icon (width and height).
        icon_name: Name of the icon.
    
    Args:
        x: X-coordinate.
        y: Y-coordinate.
        size: Size of the icon.
        icon_name: Name of the icon.
    """
    
    def __init__(self, x: int, y: int, size: int, icon_name: str) -> None:
        """Initialize an icon.
        
        Args:
            x: X-coordinate.
            y: Y-coordinate.
            size: Size of the icon.
            icon_name: Name of the icon.
        """
        super().__init__(x, y, size, size)
        self.icon_name = icon_name
    
    def draw(self) -> str:
        """Draw the icon.
        
        Returns:
            Icon representation as [icon_name].
        """
        return f"[{self.icon_name}]"
    
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            Click response message.
        """
        return f"Icon '{self.icon_name}' clicked at ({self.x}, {self.y})"


class Panel(Drawable):
    """A drawable panel (not clickable).
    
    Drawn as a bordered rectangle.
    
    Attributes:
        x: X-coordinate.
        y: Y-coordinate.
        width: Width of the panel.
        height: Height of the panel.
        title: Panel title.
    
    Args:
        x: X-coordinate.
        y: Y-coordinate.
        width: Width of the panel.
        height: Height of the panel.
        title: Panel title (default "").
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str = ""
    ) -> None:
        """Initialize a panel.
        
        Args:
            x: X-coordinate.
            y: Y-coordinate.
            width: Width of the panel.
            height: Height of the panel.
            title: Panel title (default "").
        """
        super().__init__(x, y, width, height)
        self.title = title
    
    def draw(self) -> str:
        """Draw the panel.
        
        Returns:
            ASCII representation of the panel.
        """
        inner_width = max(0, self.width - 2)
        
        if self.title:
            # Title in top border: +--[ Title ]--+
            title_part = f"[ {self.title} ]"
            remaining = inner_width - len(title_part)
            if remaining < 0:
                # Title too long, just show what fits
                title_part = title_part[:inner_width]
                remaining = 0
            left_pad = remaining // 2
            right_pad = remaining - left_pad
            top = "+" + "-" * left_pad + title_part + "-" * right_pad + "+"
        else:
            top = "+" + "-" * inner_width + "+"
        
        middle = "|" + " " * inner_width + "|"
        bottom = "+" + "-" * inner_width + "+"
        
        # Build panel with proper height
        content_height = self.height - 2  # Subtract top and bottom
        if content_height < 0:
            content_height = 0
        
        lines = [top]
        for _ in range(content_height):
            lines.append(middle)
        lines.append(bottom)
        
        return "\n".join(lines)
