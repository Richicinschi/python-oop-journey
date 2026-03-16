"""Problem 02: Flying and Swimming Animals.

Implement mixins and classes for animals with different capabilities.

Classes to implement:
- Flyable: Mixin providing flying capability
- Swimmable: Mixin providing swimming capability
- Walkable: Mixin providing walking capability
- Duck: Can fly, swim, and walk
- Penguin: Can swim and walk, but not fly

Example:
    >>> duck = Duck("Donald", 3)
    >>> duck.fly()
    'Donald is flying through the air!'
    >>> duck.swim()
    'Donald is swimming gracefully!'
    >>> penguin = Penguin("Skipper", 5)
    >>> penguin.swim()
    'Skipper is swimming gracefully!'
"""

from __future__ import annotations

from typing import Any


class Flyable:
    """Mixin that provides flying capability.
    
    Classes using this mixin must have 'name' attribute.
    """
    
    def fly(self) -> str:
        """Return a flying message.
        
        Returns:
            A message describing the flying action.
        """
        # TODO: Return f"{self.name} is flying through the air!"
        raise NotImplementedError("Return flying message")
    
    def take_off(self) -> str:
        """Return a take-off message.
        
        Returns:
            A message describing the take-off action.
        """
        # TODO: Return f"{self.name} takes off into the sky!"
        raise NotImplementedError("Return take-off message")


class Swimmable:
    """Mixin that provides swimming capability.
    
    Classes using this mixin must have 'name' attribute.
    """
    
    def swim(self) -> str:
        """Return a swimming message.
        
        Returns:
            A message describing the swimming action.
        """
        # TODO: Return f"{self.name} is swimming gracefully!"
        raise NotImplementedError("Return swimming message")
    
    def dive(self) -> str:
        """Return a diving message.
        
        Returns:
            A message describing the diving action.
        """
        # TODO: Return f"{self.name} dives underwater!"
        raise NotImplementedError("Return diving message")


class Walkable:
    """Mixin that provides walking capability.
    
    Classes using this mixin must have 'name' attribute.
    """
    
    def walk(self) -> str:
        """Return a walking message.
        
        Returns:
            A message describing the walking action.
        """
        # TODO: Return f"{self.name} is walking around."
        raise NotImplementedError("Return walking message")


class Animal:
    """Base class for all animals.
    
    Attributes:
        name: The animal's name.
        age: The animal's age in years.
        species: The animal species (class attribute to be set by subclasses).
    
    Args:
        name: The animal's name.
        age: The animal's age in years.
    """
    
    species: str = "unknown"
    
    def __init__(self, name: str, age: int) -> None:
        # TODO: Set name and age attributes
        raise NotImplementedError("Set name and age")
    
    def describe(self) -> str:
        """Return a description of the animal.
        
        Returns:
            A description string.
        """
        # TODO: Return f"{self.name} is a {self.age}-year-old {self.species}"
        raise NotImplementedError("Return description")
    
    def speak(self) -> str:
        """Return the animal's sound.
        
        Returns:
            The sound the animal makes.
        """
        # TODO: Return f"{self.name} makes a sound."
        raise NotImplementedError("Return sound")


class Duck(Animal, Flyable, Swimmable, Walkable):
    """A duck that can fly, swim, and walk.
    
    Attributes:
        name: The duck's name.
        age: The duck's age in years.
    
    Args:
        name: The duck's name.
        age: The duck's age in years.
    """
    
    species = "duck"
    
    def __init__(self, name: str, age: int) -> None:
        # TODO: Call super().__init__ with name and age
        raise NotImplementedError("Initialize duck")
    
    def speak(self) -> str:
        """Return the duck's sound.
        
        Returns:
            'Quack!'
        """
        # TODO: Return "Quack!"
        raise NotImplementedError("Return quack")
    
    def perform_trick(self) -> str:
        """Perform a trick combining multiple capabilities.
        
        Returns:
            A message describing the trick.
        """
        # TODO: Return f"{self.name} flies and dives in a loop!"
        raise NotImplementedError("Return trick message")


class Penguin(Animal, Swimmable, Walkable):
    """A penguin that can swim and walk, but not fly.
    
    Attributes:
        name: The penguin's name.
        age: The penguin's age in years.
    
    Args:
        name: The penguin's name.
        age: The penguin's age in years.
    """
    
    species = "penguin"
    
    def __init__(self, name: str, age: int) -> None:
        # TODO: Call super().__init__ with name and age
        raise NotImplementedError("Initialize penguin")
    
    def speak(self) -> str:
        """Return the penguin's sound.
        
        Returns:
            'Squawk!'
        """
        # TODO: Return "Squawk!"
        raise NotImplementedError("Return squawk")
    
    def walk(self) -> str:
        """Penguins waddle instead of walk.
        
        Returns:
            A waddling message.
        """
        # TODO: Return f"{self.name} is waddling around."
        raise NotImplementedError("Return waddle message")
    
    def slide(self) -> str:
        """Slide on belly (penguin-specific behavior).
        
        Returns:
            A sliding message.
        """
        # TODO: Return f"{self.name} slides on its belly! Wheee!"
        raise NotImplementedError("Return slide message")
