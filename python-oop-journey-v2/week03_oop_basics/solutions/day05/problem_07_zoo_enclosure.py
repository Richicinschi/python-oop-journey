"""Solution for Problem 07: Zoo Enclosure.

Zoo with Enclosures and Animals - demonstrates composition
(enclosures are part of the zoo) and aggregation (animals).
"""

from __future__ import annotations
from typing import Optional


class Animal:
    """An animal in the zoo.
    
    Animals exist independently and can be moved between enclosures
    or even between zoos.
    """
    
    def __init__(self, name: str, species: str, age: int) -> None:
        """Initialize the animal.
        
        Args:
            name: Animal's name.
            species: Animal species.
            age: Animal age in years.
        """
        self.name = name
        self.species = species
        self.age = age
        self.enclosure_id: str | None = None
    
    def assign_to_enclosure(self, enclosure_id: str) -> None:
        """Assign animal to an enclosure.
        
        Args:
            enclosure_id: Enclosure identifier.
        """
        self.enclosure_id = enclosure_id
    
    def remove_from_enclosure(self) -> None:
        """Remove animal from its enclosure."""
        self.enclosure_id = None


class Enclosure:
    """An enclosure in the zoo (composed by Zoo).
    
    The enclosure is part of the zoo infrastructure and is
    created/managed by the zoo.
    """
    
    def __init__(self, enclosure_id: str, habitat_type: str, capacity: int) -> None:
        """Initialize the enclosure.
        
        Args:
            enclosure_id: Unique enclosure identifier.
            habitat_type: Type of habitat (e.g., 'savanna', 'aquatic').
            capacity: Maximum number of animals.
        """
        self.enclosure_id = enclosure_id
        self.habitat_type = habitat_type
        self.capacity = capacity
        self.animals: list[Animal] = []
    
    def add_animal(self, animal: Animal) -> bool:
        """Add an animal to the enclosure.
        
        Args:
            animal: Animal to add.
            
        Returns:
            True if added, False if at capacity.
        """
        if len(self.animals) >= self.capacity:
            return False
        
        self.animals.append(animal)
        animal.assign_to_enclosure(self.enclosure_id)
        return True
    
    def remove_animal(self, animal_name: str) -> bool:
        """Remove an animal from the enclosure.
        
        Args:
            animal_name: Name of animal to remove.
            
        Returns:
            True if removed, False if not found.
        """
        for i, animal in enumerate(self.animals):
            if animal.name == animal_name:
                animal.remove_from_enclosure()
                self.animals.pop(i)
                return True
        return False
    
    def get_animal_count(self) -> int:
        """Get number of animals in enclosure.
        
        Returns:
            Animal count.
        """
        return len(self.animals)
    
    def has_space(self) -> bool:
        """Check if enclosure has space.
        
        Returns:
            True if not at capacity, False otherwise.
        """
        return len(self.animals) < self.capacity
    
    def get_animals(self) -> list[Animal]:
        """Get all animals in enclosure.
        
        Returns:
            List of animals.
        """
        return self.animals.copy()


class Zoo:
    """A zoo composing enclosures.
    
    Enclosures are composed (owned by the zoo) while animals
    are aggregated within enclosures.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the zoo.
        
        Args:
            name: Zoo name.
        """
        self.name = name
        self.enclosures: dict[str, Enclosure] = {}  # id -> Enclosure
        self.all_animals: dict[str, Animal] = {}  # name -> Animal
    
    def add_enclosure(self, enclosure: Enclosure) -> None:
        """Add an enclosure to the zoo.
        
        Args:
            enclosure: Enclosure to add (composition).
        """
        self.enclosures[enclosure.enclosure_id] = enclosure
    
    def get_enclosure(self, enclosure_id: str) -> Optional[Enclosure]:
        """Get an enclosure by ID.
        
        Args:
            enclosure_id: Enclosure ID to find.
            
        Returns:
            Enclosure if found, None otherwise.
        """
        return self.enclosures.get(enclosure_id)
    
    def add_animal_to_enclosure(self, animal: Animal, enclosure_id: str) -> str:
        """Add an animal to an enclosure.
        
        Args:
            animal: Animal to add.
            enclosure_id: Target enclosure ID.
            
        Returns:
            Status message.
        """
        enclosure = self.enclosures.get(enclosure_id)
        if enclosure is None:
            return f"Enclosure {enclosure_id} not found"
        
        self.all_animals[animal.name] = animal
        
        if enclosure.add_animal(animal):
            return f"{animal.name} the {animal.species} added to {enclosure_id}"
        return f"Enclosure {enclosure_id} is full"
    
    def remove_animal(self, animal_name: str) -> str:
        """Remove an animal from the zoo.
        
        Args:
            animal_name: Name of animal to remove.
            
        Returns:
            Status message.
        """
        animal = self.all_animals.get(animal_name)
        if animal is None:
            return f"Animal {animal_name} not found"
        
        # Find which enclosure has this animal
        if animal.enclosure_id:
            enclosure = self.enclosures.get(animal.enclosure_id)
            if enclosure:
                enclosure.remove_animal(animal_name)
        
        del self.all_animals[animal_name]
        return f"{animal_name} removed from zoo"
    
    def get_animals_by_species(self, species: str) -> list[Animal]:
        """Get all animals of a species.
        
        Args:
            species: Species to filter by.
            
        Returns:
            List of matching animals.
        """
        return [
            animal for animal in self.all_animals.values()
            if animal.species == species
        ]
    
    def get_total_animal_count(self) -> int:
        """Get total number of animals in zoo.
        
        Returns:
            Total animal count.
        """
        return len(self.all_animals)
    
    def get_enclosure_count(self) -> int:
        """Get number of enclosures.
        
        Returns:
            Enclosure count.
        """
        return len(self.enclosures)
