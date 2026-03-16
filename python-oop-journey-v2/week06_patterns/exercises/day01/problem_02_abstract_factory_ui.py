"""Problem 02: Abstract Factory UI

Topic: Abstract Factory Pattern
Difficulty: Medium

Implement the Abstract Factory pattern to create families of UI components.
Each platform (Windows, Mac, Linux) has its own style of buttons, checkboxes, and text fields.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Button(ABC):
    """Abstract product: Button."""
    
    @abstractmethod
    def render(self) -> str:
        """Render the button.
        
        Returns:
            String describing how the button is rendered
        """
        raise NotImplementedError("Implement Button.render")
    
    @abstractmethod
    def on_click(self) -> str:
        """Handle click event.
        
        Returns:
            String describing the click action
        """
        raise NotImplementedError("Implement Button.on_click")


class Checkbox(ABC):
    """Abstract product: Checkbox."""
    
    @abstractmethod
    def render(self) -> str:
        """Render the checkbox.
        
        Returns:
            String describing how the checkbox is rendered
        """
        raise NotImplementedError("Implement Checkbox.render")
    
    @abstractmethod
    def toggle(self) -> str:
        """Toggle the checkbox state.
        
        Returns:
            String describing the toggle action
        """
        raise NotImplementedError("Implement Checkbox.toggle")


class TextField(ABC):
    """Abstract product: TextField."""
    
    @abstractmethod
    def render(self) -> str:
        """Render the text field.
        
        Returns:
            String describing how the text field is rendered
        """
        raise NotImplementedError("Implement TextField.render")
    
    @abstractmethod
    def set_text(self, text: str) -> str:
        """Set text in the field.
        
        Args:
            text: Text to set
            
        Returns:
            String confirming the text was set
        """
        raise NotImplementedError("Implement TextField.set_text")


# Concrete Products - Windows Family

class WindowsButton(Button):
    """Windows-style button."""
    
    def render(self) -> str:
        """Return 'Rendering Windows-style button'."""
        raise NotImplementedError("Implement WindowsButton.render")
    
    def on_click(self) -> str:
        """Return 'Windows button clicked'."""
        raise NotImplementedError("Implement WindowsButton.on_click")


class WindowsCheckbox(Checkbox):
    """Windows-style checkbox."""
    
    def render(self) -> str:
        """Return 'Rendering Windows-style checkbox'."""
        raise NotImplementedError("Implement WindowsCheckbox.render")
    
    def toggle(self) -> str:
        """Return 'Windows checkbox toggled'."""
        raise NotImplementedError("Implement WindowsCheckbox.toggle")


class WindowsTextField(TextField):
    """Windows-style text field."""
    
    def render(self) -> str:
        """Return 'Rendering Windows-style text field'."""
        raise NotImplementedError("Implement WindowsTextField.render")
    
    def set_text(self, text: str) -> str:
        """Return 'Windows text field set to: {text}'."""
        raise NotImplementedError("Implement WindowsTextField.set_text")


# Concrete Products - Mac Family

class MacButton(Button):
    """Mac-style button."""
    
    def render(self) -> str:
        """Return 'Rendering Mac-style button'."""
        raise NotImplementedError("Implement MacButton.render")
    
    def on_click(self) -> str:
        """Return 'Mac button clicked'."""
        raise NotImplementedError("Implement MacButton.on_click")


class MacCheckbox(Checkbox):
    """Mac-style checkbox."""
    
    def render(self) -> str:
        """Return 'Rendering Mac-style checkbox'."""
        raise NotImplementedError("Implement MacCheckbox.render")
    
    def toggle(self) -> str:
        """Return 'Mac checkbox toggled'."""
        raise NotImplementedError("Implement MacCheckbox.toggle")


class MacTextField(TextField):
    """Mac-style text field."""
    
    def render(self) -> str:
        """Return 'Rendering Mac-style text field'."""
        raise NotImplementedError("Implement MacTextField.render")
    
    def set_text(self, text: str) -> str:
        """Return 'Mac text field set to: {text}'."""
        raise NotImplementedError("Implement MacTextField.set_text")


# Concrete Products - Linux Family

class LinuxButton(Button):
    """Linux-style button."""
    
    def render(self) -> str:
        """Return 'Rendering Linux-style button'."""
        raise NotImplementedError("Implement LinuxButton.render")
    
    def on_click(self) -> str:
        """Return 'Linux button clicked'."""
        raise NotImplementedError("Implement LinuxButton.on_click")


class LinuxCheckbox(Checkbox):
    """Linux-style checkbox."""
    
    def render(self) -> str:
        """Return 'Rendering Linux-style checkbox'."""
        raise NotImplementedError("Implement LinuxCheckbox.render")
    
    def toggle(self) -> str:
        """Return 'Linux checkbox toggled'."""
        raise NotImplementedError("Implement LinuxCheckbox.toggle")


class LinuxTextField(TextField):
    """Linux-style text field."""
    
    def render(self) -> str:
        """Return 'Rendering Linux-style text field'."""
        raise NotImplementedError("Implement LinuxTextField.render")
    
    def set_text(self, text: str) -> str:
        """Return 'Linux text field set to: {text}'."""
        raise NotImplementedError("Implement LinuxTextField.set_text")


# Abstract Factory

class UIFactory(ABC):
    """Abstract factory interface.
    
    Declares creation methods for each product type.
    """
    
    @abstractmethod
    def create_button(self) -> Button:
        """Create a button."""
        raise NotImplementedError("Implement UIFactory.create_button")
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox."""
        raise NotImplementedError("Implement UIFactory.create_checkbox")
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        """Create a text field."""
        raise NotImplementedError("Implement UIFactory.create_text_field")


class WindowsUIFactory(UIFactory):
    """Factory for creating Windows UI components."""
    
    def create_button(self) -> Button:
        """Create a WindowsButton."""
        raise NotImplementedError("Implement WindowsUIFactory.create_button")
    
    def create_checkbox(self) -> Checkbox:
        """Create a WindowsCheckbox."""
        raise NotImplementedError("Implement WindowsUIFactory.create_checkbox")
    
    def create_text_field(self) -> TextField:
        """Create a WindowsTextField."""
        raise NotImplementedError("Implement WindowsUIFactory.create_text_field")


class MacUIFactory(UIFactory):
    """Factory for creating Mac UI components."""
    
    def create_button(self) -> Button:
        """Create a MacButton."""
        raise NotImplementedError("Implement MacUIFactory.create_button")
    
    def create_checkbox(self) -> Checkbox:
        """Create a MacCheckbox."""
        raise NotImplementedError("Implement MacUIFactory.create_checkbox")
    
    def create_text_field(self) -> TextField:
        """Create a MacTextField."""
        raise NotImplementedError("Implement MacUIFactory.create_text_field")


class LinuxUIFactory(UIFactory):
    """Factory for creating Linux UI components."""
    
    def create_button(self) -> Button:
        """Create a LinuxButton."""
        raise NotImplementedError("Implement LinuxUIFactory.create_button")
    
    def create_checkbox(self) -> Checkbox:
        """Create a LinuxCheckbox."""
        raise NotImplementedError("Implement LinuxUIFactory.create_checkbox")
    
    def create_text_field(self) -> TextField:
        """Create a LinuxTextField."""
        raise NotImplementedError("Implement LinuxUIFactory.create_text_field")
