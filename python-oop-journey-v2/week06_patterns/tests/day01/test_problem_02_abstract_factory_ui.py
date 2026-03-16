"""Tests for Problem 02: Abstract Factory UI."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day01.problem_02_abstract_factory_ui import (
    Button, Checkbox, TextField,
    WindowsButton, WindowsCheckbox, WindowsTextField,
    MacButton, MacCheckbox, MacTextField,
    LinuxButton, LinuxCheckbox, LinuxTextField,
    UIFactory, WindowsUIFactory, MacUIFactory, LinuxUIFactory,
)


class TestWindowsButton:
    """Tests for WindowsButton class."""
    
    def test_render(self) -> None:
        button = WindowsButton()
        assert button.render() == "Rendering Windows-style button"
    
    def test_on_click(self) -> None:
        button = WindowsButton()
        assert button.on_click() == "Windows button clicked"
    
    def test_isinstance_of_button(self) -> None:
        button = WindowsButton()
        assert isinstance(button, Button)


class TestWindowsCheckbox:
    """Tests for WindowsCheckbox class."""
    
    def test_render(self) -> None:
        checkbox = WindowsCheckbox()
        assert checkbox.render() == "Rendering Windows-style checkbox"
    
    def test_toggle(self) -> None:
        checkbox = WindowsCheckbox()
        assert checkbox.toggle() == "Windows checkbox toggled"
    
    def test_isinstance_of_checkbox(self) -> None:
        checkbox = WindowsCheckbox()
        assert isinstance(checkbox, Checkbox)


class TestWindowsTextField:
    """Tests for WindowsTextField class."""
    
    def test_render(self) -> None:
        text_field = WindowsTextField()
        assert text_field.render() == "Rendering Windows-style text field"
    
    def test_set_text(self) -> None:
        text_field = WindowsTextField()
        assert text_field.set_text("Hello") == "Windows text field set to: Hello"
    
    def test_isinstance_of_text_field(self) -> None:
        text_field = WindowsTextField()
        assert isinstance(text_field, TextField)


class TestMacButton:
    """Tests for MacButton class."""
    
    def test_render(self) -> None:
        button = MacButton()
        assert button.render() == "Rendering Mac-style button"
    
    def test_on_click(self) -> None:
        button = MacButton()
        assert button.on_click() == "Mac button clicked"
    
    def test_isinstance_of_button(self) -> None:
        button = MacButton()
        assert isinstance(button, Button)


class TestMacCheckbox:
    """Tests for MacCheckbox class."""
    
    def test_render(self) -> None:
        checkbox = MacCheckbox()
        assert checkbox.render() == "Rendering Mac-style checkbox"
    
    def test_toggle(self) -> None:
        checkbox = MacCheckbox()
        assert checkbox.toggle() == "Mac checkbox toggled"
    
    def test_isinstance_of_checkbox(self) -> None:
        checkbox = MacCheckbox()
        assert isinstance(checkbox, Checkbox)


class TestMacTextField:
    """Tests for MacTextField class."""
    
    def test_render(self) -> None:
        text_field = MacTextField()
        assert text_field.render() == "Rendering Mac-style text field"
    
    def test_set_text(self) -> None:
        text_field = MacTextField()
        assert text_field.set_text("Hello") == "Mac text field set to: Hello"
    
    def test_isinstance_of_text_field(self) -> None:
        text_field = MacTextField()
        assert isinstance(text_field, TextField)


class TestLinuxButton:
    """Tests for LinuxButton class."""
    
    def test_render(self) -> None:
        button = LinuxButton()
        assert button.render() == "Rendering Linux-style button"
    
    def test_on_click(self) -> None:
        button = LinuxButton()
        assert button.on_click() == "Linux button clicked"
    
    def test_isinstance_of_button(self) -> None:
        button = LinuxButton()
        assert isinstance(button, Button)


class TestLinuxCheckbox:
    """Tests for LinuxCheckbox class."""
    
    def test_render(self) -> None:
        checkbox = LinuxCheckbox()
        assert checkbox.render() == "Rendering Linux-style checkbox"
    
    def test_toggle(self) -> None:
        checkbox = LinuxCheckbox()
        assert checkbox.toggle() == "Linux checkbox toggled"
    
    def test_isinstance_of_checkbox(self) -> None:
        checkbox = LinuxCheckbox()
        assert isinstance(checkbox, Checkbox)


class TestLinuxTextField:
    """Tests for LinuxTextField class."""
    
    def test_render(self) -> None:
        text_field = LinuxTextField()
        assert text_field.render() == "Rendering Linux-style text field"
    
    def test_set_text(self) -> None:
        text_field = LinuxTextField()
        assert text_field.set_text("Hello") == "Linux text field set to: Hello"
    
    def test_isinstance_of_text_field(self) -> None:
        text_field = LinuxTextField()
        assert isinstance(text_field, TextField)


class TestWindowsUIFactory:
    """Tests for WindowsUIFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = WindowsUIFactory()
        assert isinstance(factory, UIFactory)
    
    def test_create_button(self) -> None:
        factory = WindowsUIFactory()
        button = factory.create_button()
        assert isinstance(button, WindowsButton)
    
    def test_create_checkbox(self) -> None:
        factory = WindowsUIFactory()
        checkbox = factory.create_checkbox()
        assert isinstance(checkbox, WindowsCheckbox)
    
    def test_create_text_field(self) -> None:
        factory = WindowsUIFactory()
        text_field = factory.create_text_field()
        assert isinstance(text_field, WindowsTextField)


class TestMacUIFactory:
    """Tests for MacUIFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = MacUIFactory()
        assert isinstance(factory, UIFactory)
    
    def test_create_button(self) -> None:
        factory = MacUIFactory()
        button = factory.create_button()
        assert isinstance(button, MacButton)
    
    def test_create_checkbox(self) -> None:
        factory = MacUIFactory()
        checkbox = factory.create_checkbox()
        assert isinstance(checkbox, MacCheckbox)
    
    def test_create_text_field(self) -> None:
        factory = MacUIFactory()
        text_field = factory.create_text_field()
        assert isinstance(text_field, MacTextField)


class TestLinuxUIFactory:
    """Tests for LinuxUIFactory class."""
    
    def test_isinstance_of_factory(self) -> None:
        factory = LinuxUIFactory()
        assert isinstance(factory, UIFactory)
    
    def test_create_button(self) -> None:
        factory = LinuxUIFactory()
        button = factory.create_button()
        assert isinstance(button, LinuxButton)
    
    def test_create_checkbox(self) -> None:
        factory = LinuxUIFactory()
        checkbox = factory.create_checkbox()
        assert isinstance(checkbox, LinuxCheckbox)
    
    def test_create_text_field(self) -> None:
        factory = LinuxUIFactory()
        text_field = factory.create_text_field()
        assert isinstance(text_field, LinuxTextField)


class TestFamilyCompatibility:
    """Tests demonstrating product family compatibility."""
    
    def test_windows_family_consistency(self) -> None:
        factory = WindowsUIFactory()
        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_field = factory.create_text_field()
        
        assert "Windows" in button.render()
        assert "Windows" in checkbox.render()
        assert "Windows" in text_field.render()
    
    def test_mac_family_consistency(self) -> None:
        factory = MacUIFactory()
        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_field = factory.create_text_field()
        
        assert "Mac" in button.render()
        assert "Mac" in checkbox.render()
        assert "Mac" in text_field.render()
    
    def test_linux_family_consistency(self) -> None:
        factory = LinuxUIFactory()
        button = factory.create_button()
        checkbox = factory.create_checkbox()
        text_field = factory.create_text_field()
        
        assert "Linux" in button.render()
        assert "Linux" in checkbox.render()
        assert "Linux" in text_field.render()


class TestPolymorphism:
    """Tests demonstrating polymorphic behavior across factories."""
    
    def test_uniform_interface(self) -> None:
        factories: list[UIFactory] = [
            WindowsUIFactory(),
            MacUIFactory(),
            LinuxUIFactory(),
        ]
        
        for factory in factories:
            button = factory.create_button()
            checkbox = factory.create_checkbox()
            text_field = factory.create_text_field()
            
            assert isinstance(button, Button)
            assert isinstance(checkbox, Checkbox)
            assert isinstance(text_field, TextField)
    
    def test_render_works_on_all_products(self) -> None:
        factories: list[UIFactory] = [
            WindowsUIFactory(),
            MacUIFactory(),
            LinuxUIFactory(),
        ]
        
        for factory in factories:
            assert factory.create_button().render()
            assert factory.create_checkbox().render()
            assert factory.create_text_field().render()
