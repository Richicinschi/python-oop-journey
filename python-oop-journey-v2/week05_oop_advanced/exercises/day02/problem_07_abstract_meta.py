"""Problem 07: Abstract Method Enforcement Metaclass

Topic: Metaclasses
Difficulty: Hard

Implement a metaclass that enforces abstract methods at class creation time,
similar to ABC but with custom error messages and additional validation.

Classes to implement:
- AbstractMeta: Metaclass that enforces abstract methods
- MustImplement: Decorator to mark methods as abstract
- BaseComponent: Base class with abstract methods
- Concrete implementations

Requirements:
- Mark methods with @MustImplement decorator
- Verify all abstract methods are implemented at class creation
- Provide clear error messages about missing methods
- Support inherited abstract methods
- Allow abstract classes (classes with abstract methods but not all implemented)
"""

from __future__ import annotations

from typing import Any, Callable


class MustImplement:
    """Decorator to mark a method as abstract/must-implement.
    
    Usage:
        class Base(metaclass=AbstractMeta):
            @MustImplement
            def required_method(self):
                pass
    """
    
    def __init__(self, method: Callable[..., Any]) -> None:
        """Mark the method as required.
        
        Args:
            method: The method to mark as abstract
        """
        raise NotImplementedError("Implement __init__")
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Track the name this descriptor is assigned to."""
        raise NotImplementedError("Implement __set_name__")


class AbstractMeta(type):
    """Metaclass that enforces abstract methods at class creation.
    
    Methods marked with @MustImplement must be implemented by concrete
    (non-abstract) classes. The metaclass validates this at class creation
time, not at instantiation.
    
    A class is considered abstract if:
    - It directly defines methods marked with @MustImplement
    - It inherits abstract methods that are not implemented
    
    A class is concrete (must implement all abstracts) if:
    - It has no unimplemented abstract methods
    - It doesn't explicitly mark itself as abstract
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class after validating abstract methods.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class
            
        Raises:
            TypeError: If a concrete class has unimplemented abstract methods
        """
        raise NotImplementedError("Implement __new__")
    
    @staticmethod
    def _get_abstract_methods(bases: tuple[type, ...]) -> set[str]:
        """Collect all abstract method names from base classes.
        
        Args:
            bases: Base classes to inspect
            
        Returns:
            Set of abstract method names
        """
        raise NotImplementedError("Implement _get_abstract_methods")
    
    @staticmethod
    def _is_abstract_method(method: Any) -> bool:
        """Check if a method is marked as abstract.
        
        Args:
            method: The method to check
            
        Returns:
            True if the method is marked with MustImplement
        """
        raise NotImplementedError("Implement _is_abstract_method")


class BaseComponent(metaclass=AbstractMeta):
    """Base component with abstract methods.
    
    Subclasses must implement:
    - initialize(): Setup the component
    - execute(): Run the component's main logic
    """
    
    @MustImplement
    def initialize(self) -> None:
        """Initialize the component. Must be implemented by subclasses."""
        pass
    
    @MustImplement
    def execute(self) -> str:
        """Execute component logic. Must be implemented by subclasses.
        
        Returns:
            Execution result
        """
        pass
    
    def cleanup(self) -> None:
        """Cleanup method with default implementation."""
        pass


class DataProcessor(BaseComponent):
    """Abstract base for data processors.
    
    Extends BaseComponent with additional abstract method.
    """
    
    @MustImplement
    def validate_input(self, data: Any) -> bool:
        """Validate input data."""
        pass
    
    def execute(self) -> str:
        """Default execute implementation."""
        return "DataProcessor executing"


class CSVProcessor(DataProcessor):
    """Concrete implementation for CSV processing.
    
    Must implement all abstract methods from BaseComponent and DataProcessor.
    """
    
    def __init__(self) -> None:
        """Initialize CSV processor."""
        raise NotImplementedError("Implement __init__")
    
    def initialize(self) -> None:
        """Initialize CSV processor."""
        raise NotImplementedError("Implement initialize")
    
    def validate_input(self, data: Any) -> bool:
        """Validate CSV data."""
        raise NotImplementedError("Implement validate_input")
    
    def process_row(self, row: list[str]) -> dict[str, str]:
        """Process a single CSV row."""
        raise NotImplementedError("Implement process_row")


class JSONProcessor(DataProcessor):
    """Concrete implementation for JSON processing."""
    
    def __init__(self) -> None:
        """Initialize JSON processor."""
        raise NotImplementedError("Implement __init__")
    
    def initialize(self) -> None:
        """Initialize JSON processor."""
        raise NotImplementedError("Implement initialize")
    
    def validate_input(self, data: Any) -> bool:
        """Validate JSON data."""
        raise NotImplementedError("Implement validate_input")
    
    def parse_json(self, json_str: str) -> dict[str, Any]:
        """Parse JSON string."""
        raise NotImplementedError("Implement parse_json")


# Hints for Abstract Method Enforcement Metaclass (Hard):
# 
# Hint 1 - Conceptual nudge:
# You need to inspect the class being created AND all its base classes. Look for
# methods marked with a special attribute that your @MustImplement decorator adds.
#
# Hint 2 - Structural plan:
# - @MustImplement should set a flag attribute on the function (e.g., func._must_implement = True)
# - In AbstractMeta.__new__, collect all abstract methods from bases using
#   _get_abstract_methods
# - Check if the current class implements any of them
# - If any abstracts remain unimplemented, raise TypeError
#
# Hint 3 - Edge-case warning:
# A class with unimplemented abstract methods is itself abstract and should be allowed.
# Only concrete classes (no unimplemented abstracts) should raise errors. Consider
# how to mark a class as "explicitly abstract" if needed.
