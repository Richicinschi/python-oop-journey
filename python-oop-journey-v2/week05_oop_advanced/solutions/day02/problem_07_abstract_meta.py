"""Problem 07: Abstract Method Enforcement Metaclass - Solution.

Enforces abstract methods at class creation time with custom error
messages and additional validation.
"""

from __future__ import annotations

from typing import Any, Callable
from functools import wraps


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
        self.method = method
        self.name = method.__name__
        wraps(method)(self)
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Track the name this descriptor is assigned to."""
        self.name = name
    
    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Return the method when accessed."""
        if obj is None:
            return self
        # Bind the method to the instance
        return self.method.__get__(obj, objtype)


class AbstractMeta(type):
    """Metaclass that enforces abstract methods at class creation.
    
    Methods marked with @MustImplement must be implemented by concrete
    (non-abstract) classes. The metaclass validates this at class creation	time, not at instantiation.
    
    How it works:
    1. Collects abstract methods from all base classes (inherited abstracts)
    2. Finds new abstract methods defined in the current class
    3. Finds implemented methods in the current class (excluding MustImplement markers)
    4. Determines which abstract methods remain unimplemented
    5. If a concrete class has unimplemented abstracts, raises TypeError
    6. If a class defines new abstracts, it's considered abstract itself
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
        # Step 1: Collect abstract methods from all base classes
        # This handles inheritance - if Base has abstract methods, Child knows about them
        abstract_from_bases = mcs._get_abstract_methods(bases)
        
        # Step 2: Find abstract methods defined in the current class namespace
        # These are methods wrapped with @MustImplement
        current_abstract: set[str] = set()
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, MustImplement):
                current_abstract.add(attr_name)
        
        # Step 3: Combine inherited and current abstract methods
        all_abstract = abstract_from_bases | current_abstract
        
        # Step 4: Find which abstract methods are being implemented in this class
        # A method "implements" an abstract if it's callable and not a MustImplement marker
        implemented: set[str] = set()
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not isinstance(attr_value, MustImplement):
                if attr_name in all_abstract:
                    implemented.add(attr_name)
        
        # Step 5: Determine which abstract methods remain unimplemented
        unimplemented = all_abstract - implemented
        
        # Step 6: Check if this class defines new abstract methods
        # If so, it's an abstract class itself and doesn't need to implement all methods
        defines_abstract = len(current_abstract) > 0
        
        # Step 7: Error if concrete class has unimplemented abstract methods
        # A class is "concrete" if it doesn't define new abstract methods
        if unimplemented and not defines_abstract:
            missing_list = sorted(unimplemented)
            raise TypeError(
                f"Class '{name}' must implement abstract methods: "
                f"{', '.join(missing_list)}"
            )
        
        # Step 8: Store remaining abstract methods for subclasses to check against
        # This preserves the chain of abstract method inheritance
        namespace['_abstract_methods'] = unimplemented if defines_abstract else set()
        
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def _get_abstract_methods(bases: tuple[type, ...]) -> set[str]:
        """Collect all abstract method names from base classes.
        
        This method walks through all base classes to find:
        1. Methods stored in _abstract_methods set (inherited abstracts)
        2. MustImplement descriptor instances (abstract markers)
        
        Args:
            bases: Base classes to inspect
            
        Returns:
            Set of abstract method names
        """
        abstract: set[str] = set()
        for base in bases:
            # Check for inherited abstract methods stored by this metaclass
            if hasattr(base, '_abstract_methods'):
                abstract.update(base._abstract_methods)
            # Also check for MustImplement instances in the class
            for attr_name in dir(base):
                if not attr_name.startswith('_'):
                    attr = getattr(base, attr_name, None)
                    if isinstance(attr, MustImplement):
                        abstract.add(attr_name)
        return abstract
    
    @staticmethod
    def _is_abstract_method(method: Any) -> bool:
        """Check if a method is marked as abstract.
        
        Args:
            method: The method to check
            
        Returns:
            True if the method is marked with MustImplement
        """
        return isinstance(method, MustImplement)


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
    Note: This class provides a default execute() implementation but
    adds a new abstract method validate_input(), so it's still abstract.
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
    Since DataProcessor already provides execute(), we only need to implement
    initialize() (from BaseComponent) and validate_input() (from DataProcessor).
    """
    
    def __init__(self) -> None:
        """Initialize CSV processor."""
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize CSV processor."""
        self._initialized = True
    
    def validate_input(self, data: Any) -> bool:
        """Validate CSV data."""
        return isinstance(data, str) and ',' in data
    
    def process_row(self, row: list[str]) -> dict[str, str]:
        """Process a single CSV row."""
        return {'data': ','.join(row)}


class JSONProcessor(DataProcessor):
    """Concrete implementation for JSON processing."""
    
    def __init__(self) -> None:
        """Initialize JSON processor."""
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize JSON processor."""
        self._initialized = True
    
    def validate_input(self, data: Any) -> bool:
        """Validate JSON data."""
        return isinstance(data, str) and data.strip().startswith(('{', '['))
    
    def parse_json(self, json_str: str) -> dict[str, Any]:
        """Parse JSON string."""
        import json
        return json.loads(json_str)
