"""Reference solution for Problem 02: Abstract Factory UI."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Button(ABC):
    """Abstract product: Button."""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def on_click(self) -> str:
        pass


class Checkbox(ABC):
    """Abstract product: Checkbox."""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def toggle(self) -> str:
        pass


class TextField(ABC):
    """Abstract product: TextField."""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def set_text(self, text: str) -> str:
        pass


# Concrete Products - Windows Family

class WindowsButton(Button):
    """Windows-style button."""
    
    def render(self) -> str:
        return "Rendering Windows-style button"
    
    def on_click(self) -> str:
        return "Windows button clicked"


class WindowsCheckbox(Checkbox):
    """Windows-style checkbox."""
    
    def render(self) -> str:
        return "Rendering Windows-style checkbox"
    
    def toggle(self) -> str:
        return "Windows checkbox toggled"


class WindowsTextField(TextField):
    """Windows-style text field."""
    
    def render(self) -> str:
        return "Rendering Windows-style text field"
    
    def set_text(self, text: str) -> str:
        return f"Windows text field set to: {text}"


# Concrete Products - Mac Family

class MacButton(Button):
    """Mac-style button."""
    
    def render(self) -> str:
        return "Rendering Mac-style button"
    
    def on_click(self) -> str:
        return "Mac button clicked"


class MacCheckbox(Checkbox):
    """Mac-style checkbox."""
    
    def render(self) -> str:
        return "Rendering Mac-style checkbox"
    
    def toggle(self) -> str:
        return "Mac checkbox toggled"


class MacTextField(TextField):
    """Mac-style text field."""
    
    def render(self) -> str:
        return "Rendering Mac-style text field"
    
    def set_text(self, text: str) -> str:
        return f"Mac text field set to: {text}"


# Concrete Products - Linux Family

class LinuxButton(Button):
    """Linux-style button."""
    
    def render(self) -> str:
        return "Rendering Linux-style button"
    
    def on_click(self) -> str:
        return "Linux button clicked"


class LinuxCheckbox(Checkbox):
    """Linux-style checkbox."""
    
    def render(self) -> str:
        return "Rendering Linux-style checkbox"
    
    def toggle(self) -> str:
        return "Linux checkbox toggled"


class LinuxTextField(TextField):
    """Linux-style text field."""
    
    def render(self) -> str:
        return "Rendering Linux-style text field"
    
    def set_text(self, text: str) -> str:
        return f"Linux text field set to: {text}"


# Abstract Factory

class UIFactory(ABC):
    """Abstract factory interface."""
    
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass


class WindowsUIFactory(UIFactory):
    """Factory for creating Windows UI components."""
    
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()
    
    def create_text_field(self) -> TextField:
        return WindowsTextField()


class MacUIFactory(UIFactory):
    """Factory for creating Mac UI components."""
    
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
    
    def create_text_field(self) -> TextField:
        return MacTextField()


class LinuxUIFactory(UIFactory):
    """Factory for creating Linux UI components."""
    
    def create_button(self) -> Button:
        return LinuxButton()
    
    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()
    
    def create_text_field(self) -> TextField:
        return LinuxTextField()
