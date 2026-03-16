"""Problem 07: Zoo Enclosure.

Implement a Zoo with Enclosures and Animals.
This demonstrates composition (enclosures are part of the zoo) and aggregation (animals in enclosures).

Classes to implement:
- Animal: with attributes name, species, age, enclosure_id (optional)
- Enclosure: with attributes id, habitat_type, capacity, animals (aggregation)
- Zoo: composes Enclosures

Methods required:
- Animal.assign_to_enclosure(enclosure_id: str) -> None
- Enclosure.add_animal(animal: Animal) -> bool
- Enclosure.remove_animal(animal_name: str) -> bool
- Enclosure.get_animal_count() -> int
- Zoo.add_enclosure(enclosure: Enclosure) - composition
- Zoo.add_animal_to_enclosure(animal: Animal, enclosure_id: str) -> str
- Zoo.get_animals_by_species(species: str) -> list[Animal]

Hints:
    - Hint 1: Zoo stores enclosures in dict: self._enclosures = {id: Enclosure}
    - Hint 2: Enclosure stores animals in a list (aggregation), manages their enclosure_id
    - Hint 3: Cross-reference: when adding animal to enclosure, update both enclosure's list AND animal's enclosure_id
"""

from __future__ import annotations
from typing import Optional


class Animal:
    """An animal in the zoo."""
    
    def __init__(self, name: str, species: str, age: int) -> None:
        # TODO: Initialize name, species, age, enclosure_id (None)
        pass
    
    def assign_to_enclosure(self, enclosure_id: str) -> None:
        # TODO: Set enclosure_id
        pass
    
    def remove_from_enclosure(self) -> None:
        # TODO: Clear enclosure_id
        pass


class Enclosure:
    """An enclosure in the zoo (composed by Zoo)."""
    
    def __init__(self, enclosure_id: str, habitat_type: str, capacity: int) -> None:
        # TODO: Initialize id, habitat_type, capacity, animals (empty list)
        pass
    
    def add_animal(self, animal: Animal) -> bool:
        # TODO: Add animal if under capacity and update animal's enclosure_id
        pass
    
    def remove_animal(self, animal_name: str) -> bool:
        # TODO: Remove animal by name, clear its enclosure_id, return True if found
        pass
    
    def get_animal_count(self) -> int:
        # TODO: Return number of animals in enclosure
        pass
    
    def has_space(self) -> bool:
        # TODO: Return True if not at capacity
        pass
    
    def get_animals(self) -> list[Animal]:
        # TODO: Return list of animals in enclosure
        pass


class Zoo:
    """A zoo composing enclosures."""
    
    def __init__(self, name: str) -> None:
        # TODO: Initialize name, enclosures dict (id -> Enclosure), all_animals dict (name -> Animal)
        pass
    
    def add_enclosure(self, enclosure: Enclosure) -> None:
        # TODO: Add enclosure to zoo
        pass
    
    def get_enclosure(self, enclosure_id: str) -> Optional[Enclosure]:
        # TODO: Return enclosure by ID or None
        pass
    
    def add_animal_to_enclosure(self, animal: Animal, enclosure_id: str) -> str:
        # TODO: Find enclosure, add animal, track animal, return status
        pass
    
    def remove_animal(self, animal_name: str) -> str:
        # TODO: Find animal, remove from its enclosure, return status
        pass
    
    def get_animals_by_species(self, species: str) -> list[Animal]:
        # TODO: Return all animals matching species
        pass
    
    def get_total_animal_count(self) -> int:
        # TODO: Return total count across all enclosures
        pass
