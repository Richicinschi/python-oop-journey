"""Enclosure module - reference solution.

Demonstrates composition - Enclosure HAS animals.
"""

from __future__ import annotations

from typing import Any

from .animal import Animal


class Enclosure:
    """Enclosure class using composition to contain animals."""

    _id_counter = 0

    def __init__(
        self,
        name: str,
        capacity: int,
        enclosure_type: str = "general",
        outdoor_access: bool = False,
    ) -> None:
        Enclosure._id_counter += 1
        self._enclosure_id = f"E{Enclosure._id_counter:04d}"
        self.name = name
        self.capacity = capacity
        self.enclosure_type = enclosure_type
        self.outdoor_access = outdoor_access
        self._animals: list[Animal] = []
        self._cleanliness = "clean"
        self._cleaning_count = 0

    @property
    def enclosure_id(self) -> str:
        return self._enclosure_id

    def add_animal(self, animal: Animal) -> dict[str, Any]:
        """Add animal to enclosure."""
        if len(self._animals) >= self.capacity:
            return {
                "success": False,
                "message": f"Enclosure {self.name} is at capacity",
            }
        
        if not self.is_compatible(animal):
            return {
                "success": False,
                "message": f"{animal.species} not compatible with {self.enclosure_type} enclosure",
            }
        
        self._animals.append(animal)
        self._cleanliness = "needs_cleaning"
        return {
            "success": True,
            "message": f"{animal.name} added to {self.name}",
            "animal_id": animal.animal_id,
        }

    def remove_animal(self, animal_id: str) -> dict[str, Any]:
        """Remove animal from enclosure."""
        for i, animal in enumerate(self._animals):
            if animal.animal_id == animal_id:
                removed = self._animals.pop(i)
                return {
                    "success": True,
                    "message": f"{removed.name} removed from {self.name}",
                    "animal": removed,
                }
        return {
            "success": False,
            "message": f"Animal {animal_id} not found in {self.name}",
            "animal": None,
        }

    def get_animals(self) -> list[Animal]:
        """Return list of all animals in enclosure."""
        return self._animals.copy()

    def get_animal_ids(self) -> list[str]:
        """Return list of animal IDs."""
        return [a.animal_id for a in self._animals]

    def has_animal(self, animal_id: str) -> bool:
        """Return True if animal is in enclosure."""
        return any(a.animal_id == animal_id for a in self._animals)

    def get_occupancy(self) -> int:
        """Return current number of animals."""
        return len(self._animals)

    def has_space(self) -> bool:
        """Return True if enclosure has space."""
        return len(self._animals) < self.capacity

    def get_available_space(self) -> int:
        """Return number of available spots."""
        return self.capacity - len(self._animals)

    def clean(self) -> str:
        """Clean enclosure and return status message."""
        if not self._animals:
            self._cleanliness = "clean"
            self._cleaning_count += 1
            return f"{self.name} cleaned (was empty)"
        
        old_status = self._cleanliness
        self._cleanliness = "clean"
        self._cleaning_count += 1
        return f"{self.name} cleaned (was {old_status})"

    def get_cleanliness(self) -> str:
        """Return cleanliness level."""
        return self._cleanliness

    def needs_cleaning(self) -> bool:
        """Return True if enclosure needs cleaning."""
        return self._cleanliness != "clean"

    def get_status(self) -> dict[str, Any]:
        """Return complete enclosure status."""
        return {
            "enclosure_id": self.enclosure_id,
            "name": self.name,
            "type": self.enclosure_type,
            "capacity": self.capacity,
            "occupancy": self.get_occupancy(),
            "available_space": self.get_available_space(),
            "cleanliness": self._cleanliness,
            "cleaning_count": self._cleaning_count,
            "outdoor_access": self.outdoor_access,
            "animals": [a.animal_id for a in self._animals],
        }

    def get_animals_by_species(self, species: str) -> list[Animal]:
        """Filter animals by species."""
        return [a for a in self._animals if a.species == species]

    def is_compatible(self, animal: Animal) -> bool:
        """Check if animal type is compatible with enclosure."""
        compatibility_map = {
            "dog": ["dog", "general"],
            "cat": ["cat", "general"],
            "bird": ["aviary", "general"],
            "rabbit": ["small_mammal", "general"],
        }
        
        if self.enclosure_type == "general":
            return True
        
        allowed = compatibility_map.get(animal.species, ["general"])
        return self.enclosure_type in allowed
