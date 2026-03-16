"""Problem 10: Auto-Serialization Metaclass - Solution.

Automatically adds serialization methods based on attributes,
eliminating repetitive to_dict/from_dict boilerplate.
"""

from __future__ import annotations

import json
from typing import Any


class SerializableMeta(type):
    """Metaclass that auto-generates serialization methods.
    
    Classes using this metaclass automatically get:
    - to_dict(): Convert instance to dictionary
    - from_dict(cls, data): Create instance from dictionary
    - to_json(): Convert instance to JSON string
    - from_json(cls, json_str): Create instance from JSON string
    """
    
    def __new__(
        mcs: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        """Create class with auto-generated serialization methods.
        
        Args:
            mcs: This metaclass
            name: Name of the class being created
            bases: Base classes
            namespace: Class namespace dictionary
            
        Returns:
            The newly created class with serialization methods
        """
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Get serialization configuration
        serialize_fields = namespace.get('__serialize_fields__')
        exclude_fields = namespace.get('__exclude_fields__', [])
        
        # Build to_dict if not already defined
        if 'to_dict' not in namespace:
            cls.to_dict = mcs._make_to_dict(cls, serialize_fields, exclude_fields)
        
        # Build from_dict if not already defined
        if 'from_dict' not in namespace:
            cls.from_dict = classmethod(mcs._make_from_dict(cls))
        
        return cls
    
    @staticmethod
    def _make_to_dict(
        cls: type,
        serialize_fields: list[str] | None,
        exclude_fields: list[str],
    ) -> Any:
        """Create to_dict method for the class.
        
        Args:
            cls: The class to create method for
            serialize_fields: Explicit list of fields to serialize
            exclude_fields: List of fields to exclude
            
        Returns:
            to_dict method
        """
        def to_dict(self: Any) -> dict[str, Any]:
            """Convert instance to dictionary."""
            result: dict[str, Any] = {}
            
            # Determine which fields to serialize
            if serialize_fields:
                fields = serialize_fields
            else:
                # Get from instance attributes (excluding private and callables)
                fields = [
                    attr for attr in dir(self)
                    if not attr.startswith('_')
                    and not callable(getattr(self, attr))
                    and attr not in exclude_fields
                ]
            
            for field in fields:
                if field in exclude_fields:
                    continue
                
                value = getattr(self, field, None)
                
                # Handle nested serializable objects
                if hasattr(value, 'to_dict'):
                    result[field] = value.to_dict()
                elif isinstance(value, list):
                    result[field] = [
                        item.to_dict() if hasattr(item, 'to_dict') else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    result[field] = {
                        k: v.to_dict() if hasattr(v, 'to_dict') else v
                        for k, v in value.items()
                    }
                else:
                    result[field] = value
            
            return result
        
        return to_dict
    
    @staticmethod
    def _make_from_dict(cls: type) -> Any:
        """Create from_dict classmethod for the class.
        
        Args:
            cls: The class to create method for
            
        Returns:
            from_dict classmethod
        """
        def from_dict(cls: type, data: dict[str, Any]) -> Any:
            """Create instance from dictionary."""
            # Get __init__ parameters
            import inspect
            sig = inspect.signature(cls.__init__)
            params = list(sig.parameters.items())[1:]  # Skip 'self'
            
            # Build kwargs from data
            kwargs: dict[str, Any] = {}
            for param_name, param in params:
                if param_name in data:
                    kwargs[param_name] = data[param_name]
                elif param.default is not inspect.Parameter.empty:
                    kwargs[param_name] = param.default
            
            return cls(**kwargs)
        
        return from_dict


class Serializable(metaclass=SerializableMeta):
    """Base class for serializable objects.
    
    Subclasses automatically get serialization methods.
    
    Optional class attributes:
    - __serialize_fields__: Explicit list of fields to serialize
    - __exclude_fields__: List of fields to exclude from serialization
    """
    
    __serialize_fields__: list[str] | None = None
    __exclude_fields__: list[str] = []
    
    def to_json(self, indent: int | None = None) -> str:
        """Convert instance to JSON string.
        
        Args:
            indent: Indentation for pretty printing
            
        Returns:
            JSON string
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> Serializable:
        """Create instance from JSON string.
        
        Args:
            json_str: JSON string
            
        Returns:
            New instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)


class Person(Serializable):
    """Person model with auto-serialization.
    
    Attributes:
        name: Person's name
        age: Person's age
        email: Person's email
    """
    
    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize person.
        
        Args:
            name: Person's name
            age: Person's age
            email: Person's email
        """
        self.name = name
        self.age = age
        self.email = email


class Address(Serializable):
    """Address model with auto-serialization.
    
    Attributes:
        street: Street address
        city: City name
        country: Country name
        postal_code: Postal/ZIP code
    """
    
    def __init__(
        self,
        street: str = "",
        city: str = "",
        country: str = "",
        postal_code: str = "",
    ) -> None:
        """Initialize address.
        
        Args:
            street: Street address
            city: City name
            country: Country name
            postal_code: Postal/ZIP code
        """
        self.street = street
        self.city = city
        self.country = country
        self.postal_code = postal_code


class Company(Serializable):
    """Company model with nested serialization.
    
    Attributes:
        name: Company name
        founded_year: Year founded
        address: Company address (Address object)
        employees: List of employees (Person objects)
    """
    
    __exclude_fields__ = ['_internal_id']
    
    def __init__(
        self,
        name: str = "",
        founded_year: int = 0,
        address: Address | None = None,
        employees: list[Person] | None = None,
    ) -> None:
        """Initialize company.
        
        Args:
            name: Company name
            founded_year: Year founded
            address: Company address
            employees: List of employees
        """
        self.name = name
        self.founded_year = founded_year
        self.address = address
        self.employees = employees or []
        self._internal_id = id(self)  # Excluded from serialization
    
    def add_employee(self, person: Person) -> None:
        """Add an employee to the company.
        
        Args:
            person: Person to add
        """
        self.employees.append(person)
    
    def employee_count(self) -> int:
        """Get number of employees.
        
        Returns:
            Employee count
        """
        return len(self.employees)
