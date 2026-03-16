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

Hints:
    Hint 1: Button and Icon use multiple inheritance (Drawable AND Clickable).
    In Button.__init__, call Drawable.__init__(self, x, y, width, height) to
    initialize the drawable part. Don't call Clickable.__init__ (it doesn't need it).
    
    Hint 2: For is_hit() in Clickable, use get_bounds() which returns (x, y, w, h).
    A point (px, py) is inside if: x <= px <= x+width AND y <= py <= y+height.
    Remember that (x, y) is the top-left corner.
    
    Hint 3: Button.draw() should create an ASCII box like:
        +----------+
        | Click Me |
        +----------+
    Use self.label.center(self.width - 2) to center the text. Panel should
    include the title in the top border if title exists: +--Title----+.
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
        # TODO: Set x, y, width, height attributes
        raise NotImplementedError("Initialize drawable")
    
    @abstractmethod
    def draw(self) -> str:
        """Draw the object and return its string representation.
        
        Returns:
            String representation of the object.
        """
        # TODO: Abstract method - subclasses must implement
        raise NotImplementedError("Subclasses must implement draw()")
    
    def get_bounds(self) -> tuple[int, int, int, int]:
        """Get the bounding box.
        
        Returns:
            Tuple of (x, y, width, height).
        """
        # TODO: Return (self.x, self.y, self.width, self.height)
        raise NotImplementedError("Return bounds")
    
    def area(self) -> int:
        """Calculate the area.
        
        Returns:
            Width * height.
        """
        # TODO: Return self.width * self.height
        raise NotImplementedError("Calculate area")


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
        # TODO: Abstract method - subclasses must implement
        raise NotImplementedError("Subclasses must implement on_click()")
    
    def is_hit(self, x: int, y: int) -> bool:
        """Check if point (x, y) hits this object.
        
        Requires the object to have get_bounds() method.
        
        Args:
            x: X-coordinate of the point.
            y: Y-coordinate of the point.
        
        Returns:
            True if point is within bounds.
        """
        # TODO: Check if x and y are within bounds (use get_bounds())
        raise NotImplementedError("Check if point hits")


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
        # TODO: Call Drawable's __init__ with x, y, width, height, set label
        raise NotImplementedError("Initialize button")
    
    def draw(self) -> str:
        """Draw the button.
        
        Returns:
            ASCII representation of the button.
        """
        # TODO: Return formatted string like:
        # +----------+
        # |  label   |
        # +----------+
        raise NotImplementedError("Draw button")
    
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            Click response message.
        """
        # TODO: Return f"Button '{self.label}' was clicked!"
        raise NotImplementedError("Handle click")


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
        # TODO: Call Drawable's __init__ with x, y, size, size, set icon_name
        raise NotImplementedError("Initialize icon")
    
    def draw(self) -> str:
        """Draw the icon.
        
        Returns:
            Icon representation as [icon_name].
        """
        # TODO: Return f"[{self.icon_name}]"
        raise NotImplementedError("Draw icon")
    
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            Click response message.
        """
        # TODO: Return f"Icon '{self.icon_name}' clicked at ({self.x}, {self.y})"
        raise NotImplementedError("Handle click")


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
        # TODO: Call Drawable's __init__ with x, y, width, height, set title
        raise NotImplementedError("Initialize panel")
    
    def draw(self) -> str:
        """Draw the panel.
        
        Returns:
            ASCII representation of the panel.
        """
        # TODO: If title exists, include it in the top border
        # Otherwise draw simple rectangle
        raise NotImplementedError("Draw panel")
