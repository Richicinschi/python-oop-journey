"""Tests for Problem 06: Renderable Clickable Widgets."""

from __future__ import annotations

from abc import ABC

import pytest

from week04_oop_intermediate.solutions.day04.problem_06_renderable_clickable_widgets import (
    Button,
    Clickable,
    Drawable,
    Icon,
    Panel,
)


class TestDrawable:
    """Tests for the Drawable abstract base class."""
    
    def test_drawable_is_abstract(self) -> None:
        """Test that Drawable is an abstract class."""
        assert issubclass(Drawable, ABC)
    
    def test_drawable_init(self) -> None:
        """Test Drawable initialization."""
        
        class TestDrawable(Drawable):
            def draw(self) -> str:
                return "test"
        
        obj = TestDrawable(10, 20, 100, 50)
        assert obj.x == 10
        assert obj.y == 20
        assert obj.width == 100
        assert obj.height == 50
    
    def test_drawable_get_bounds(self) -> None:
        """Test getting bounds."""
        
        class TestDrawable(Drawable):
            def draw(self) -> str:
                return "test"
        
        obj = TestDrawable(10, 20, 100, 50)
        assert obj.get_bounds() == (10, 20, 100, 50)
    
    def test_drawable_area(self) -> None:
        """Test calculating area."""
        
        class TestDrawable(Drawable):
            def draw(self) -> str:
                return "test"
        
        obj = TestDrawable(0, 0, 100, 50)
        assert obj.area() == 5000
    
    def test_drawable_cannot_instantiate_directly(self) -> None:
        """Test that Drawable cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Drawable(0, 0, 10, 10)


class TestClickable:
    """Tests for the Clickable abstract base class."""
    
    def test_clickable_is_abstract(self) -> None:
        """Test that Clickable is an abstract class."""
        assert issubclass(Clickable, ABC)
    
    def test_clickable_is_hit_true(self) -> None:
        """Test is_hit returns True when point is within bounds."""
        
        class TestClickable(Clickable, Drawable):
            def draw(self) -> str:
                return "test"
            
            def on_click(self) -> str:
                return "clicked"
        
        obj = TestClickable(10, 20, 100, 50)
        
        # Corner cases
        assert obj.is_hit(10, 20) is True  # Top-left
        assert obj.is_hit(110, 70) is True  # Bottom-right
        assert obj.is_hit(60, 45) is True  # Center
    
    def test_clickable_is_hit_false(self) -> None:
        """Test is_hit returns False when point is outside bounds."""
        
        class TestClickable(Clickable, Drawable):
            def draw(self) -> str:
                return "test"
            
            def on_click(self) -> str:
                return "clicked"
        
        obj = TestClickable(10, 20, 100, 50)
        
        assert obj.is_hit(5, 20) is False   # Left of bounds
        assert obj.is_hit(115, 20) is False  # Right of bounds
        assert obj.is_hit(10, 15) is False  # Above bounds
        assert obj.is_hit(10, 75) is False  # Below bounds
    
    def test_clickable_cannot_instantiate_directly(self) -> None:
        """Test that Clickable cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Clickable()


class TestButton:
    """Tests for the Button class."""
    
    def test_button_init(self) -> None:
        """Test Button initialization."""
        button = Button(10, 20, 100, 30, "Click Me")
        
        assert button.x == 10
        assert button.y == 20
        assert button.width == 100
        assert button.height == 30
        assert button.label == "Click Me"
    
    def test_button_is_drawable(self) -> None:
        """Test that Button is Drawable."""
        button = Button(0, 0, 10, 10, "Test")
        assert isinstance(button, Drawable)
    
    def test_button_is_clickable(self) -> None:
        """Test that Button is Clickable."""
        button = Button(0, 0, 10, 10, "Test")
        assert isinstance(button, Clickable)
    
    def test_button_draw(self) -> None:
        """Test Button draw method."""
        button = Button(0, 0, 12, 3, "OK")
        result = button.draw()
        
        lines = result.split("\n")
        # Check structure
        assert lines[0].startswith("+") and lines[0].endswith("+")
        assert lines[-1].startswith("+") and lines[-1].endswith("+")
        # Check label is present
        assert any("OK" in line for line in lines)
    
    def test_button_draw_long_label(self) -> None:
        """Test Button draw with long label."""
        button = Button(0, 0, 20, 3, "Submit")
        result = button.draw()
        
        assert "Submit" in result
    
    def test_button_on_click(self) -> None:
        """Test Button on_click method."""
        button = Button(0, 0, 10, 10, "Submit")
        
        result = button.on_click()
        
        assert "Submit" in result
        assert "clicked" in result.lower()
    
    def test_button_is_hit(self) -> None:
        """Test Button hit detection."""
        button = Button(10, 20, 100, 30, "Test")
        
        assert button.is_hit(10, 20) is True
        assert button.is_hit(110, 50) is True
        assert button.is_hit(5, 20) is False
    
    def test_button_mro(self) -> None:
        """Test Button's MRO."""
        expected_mro = (Button, Drawable, Clickable, ABC, object)
        # Note: ABC appears in MRO from Drawable and Clickable
        # The actual MRO includes object for the ABCs
        assert Button.__mro__[0] == Button
        assert Drawable in Button.__mro__
        assert Clickable in Button.__mro__


class TestIcon:
    """Tests for the Icon class."""
    
    def test_icon_init(self) -> None:
        """Test Icon initialization."""
        icon = Icon(10, 20, 32, "home")
        
        assert icon.x == 10
        assert icon.y == 20
        assert icon.width == 32
        assert icon.height == 32
        assert icon.icon_name == "home"
    
    def test_icon_is_drawable(self) -> None:
        """Test that Icon is Drawable."""
        icon = Icon(0, 0, 16, "test")
        assert isinstance(icon, Drawable)
    
    def test_icon_is_clickable(self) -> None:
        """Test that Icon is Clickable."""
        icon = Icon(0, 0, 16, "test")
        assert isinstance(icon, Clickable)
    
    def test_icon_draw(self) -> None:
        """Test Icon draw method."""
        icon = Icon(0, 0, 16, "home")
        result = icon.draw()
        
        assert result == "[home]"
    
    def test_icon_on_click(self) -> None:
        """Test Icon on_click method."""
        icon = Icon(10, 20, 16, "home")
        
        result = icon.on_click()
        
        assert "home" in result
        assert "(10, 20)" in result
    
    def test_icon_is_hit(self) -> None:
        """Test Icon hit detection."""
        icon = Icon(10, 20, 32, "test")
        
        assert icon.is_hit(10, 20) is True
        assert icon.is_hit(42, 52) is True
        assert icon.is_hit(5, 20) is False


class TestPanel:
    """Tests for the Panel class."""
    
    def test_panel_init(self) -> None:
        """Test Panel initialization."""
        panel = Panel(10, 20, 200, 100)
        
        assert panel.x == 10
        assert panel.y == 20
        assert panel.width == 200
        assert panel.height == 100
        assert panel.title == ""
    
    def test_panel_init_with_title(self) -> None:
        """Test Panel initialization with title."""
        panel = Panel(0, 0, 100, 50, "Settings")
        
        assert panel.title == "Settings"
    
    def test_panel_is_drawable(self) -> None:
        """Test that Panel is Drawable."""
        panel = Panel(0, 0, 10, 10)
        assert isinstance(panel, Drawable)
    
    def test_panel_is_not_clickable(self) -> None:
        """Test that Panel is not Clickable."""
        panel = Panel(0, 0, 10, 10)
        assert not isinstance(panel, Clickable)
    
    def test_panel_draw_without_title(self) -> None:
        """Test Panel draw without title."""
        panel = Panel(0, 0, 10, 3, "")
        result = panel.draw()
        
        lines = result.split("\n")
        assert lines[0] == "+--------+"  # Top border
        assert lines[-1] == "+--------+"  # Bottom border
    
    def test_panel_draw_with_title(self) -> None:
        """Test Panel draw with title."""
        panel = Panel(0, 0, 20, 3, "Test")
        result = panel.draw()
        
        assert "Test" in result
        lines = result.split("\n")
        assert lines[0].startswith("+")  # Top border with title
    
    def test_panel_draw_minimal(self) -> None:
        """Test Panel draw with minimal dimensions."""
        panel = Panel(0, 0, 2, 2, "")
        result = panel.draw()
        
        lines = result.split("\n")
        assert len(lines) == 2
        assert all(line.startswith("+") and line.endswith("+") for line in lines)


class TestWidgetInteractions:
    """Tests for widget interactions."""
    
    def test_button_area(self) -> None:
        """Test button area calculation."""
        button = Button(0, 0, 100, 50, "Test")
        assert button.area() == 5000
    
    def test_icon_area(self) -> None:
        """Test icon area calculation."""
        icon = Icon(0, 0, 32, "test")
        assert icon.area() == 1024
    
    def test_panel_area(self) -> None:
        """Test panel area calculation."""
        panel = Panel(0, 0, 200, 100)
        assert panel.area() == 20000
    
    def test_multiple_widgets_can_coexist(self) -> None:
        """Test that different widget types can coexist."""
        button = Button(10, 10, 80, 30, "OK")
        icon = Icon(100, 10, 32, "save")
        panel = Panel(0, 0, 200, 200, "Main")
        
        # All can be drawn
        assert button.draw() is not None
        assert icon.draw() is not None
        assert panel.draw() is not None
        
        # Button and Icon are clickable
        assert hasattr(button, 'on_click')
        assert hasattr(icon, 'on_click')
        
        # Panel is not clickable
        assert not hasattr(panel, 'on_click') or not callable(getattr(panel, 'on_click', None))
