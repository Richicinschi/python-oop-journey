"""Enclosure module - starter code.

This module demonstrates composition - Enclosure HAS animals.
TODO: Implement all methods marked with NotImplementedError.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .animal import Animal


class Enclosure:
    """Enclosure class using composition to contain animals.
    
    This class demonstrates composition over inheritance:
    - An Enclosure HAS animals (composition)
    - An Enclosure IS NOT an animal (no inheritance)
    
    TODO: Implement all enclosure management methods.
    """

    _id_counter = 0

    def __init__(
        self,
        name: str,
        capacity: int,
        enclosure_type: str = "general",
        outdoor_access: bool = False,
    ) -> None:
        """TODO: Initialize enclosure with empty animal collection."""
        raise NotImplementedError("Initialize enclosure")

    @property
    def enclosure_id(self) -> str:
        """TODO: Return unique enclosure ID."""
        raise NotImplementedError("Return enclosure_id")

    def add_animal(self, animal: Animal) -> dict[str, Any]:
        """TODO: Add animal to enclosure.
        
        Returns dict with success status and message.
        Should check capacity and type compatibility.
        """
        raise NotImplementedError("Add animal to enclosure")

    def remove_animal(self, animal_id: str) -> dict[str, Any]:
        """TODO: Remove animal from enclosure.
        
        Returns dict with success status and removed animal (if found).
        """
        raise NotImplementedError("Remove animal from enclosure")

    def get_animals(self) -> list[Animal]:
        """TODO: Return list of all animals in enclosure."""
        raise NotImplementedError("Return animals")

    def get_animal_ids(self) -> list[str]:
        """TODO: Return list of animal IDs."""
        raise NotImplementedError("Return animal IDs")

    def has_animal(self, animal_id: str) -> bool:
        """TODO: Return True if animal is in enclosure."""
        raise NotImplementedError("Check for animal")

    def get_occupancy(self) -> int:
        """TODO: Return current number of animals."""
        raise NotImplementedError("Return occupancy")

    def has_space(self) -> bool:
        """TODO: Return True if enclosure has space."""
        raise NotImplementedError("Check space")

    def get_available_space(self) -> int:
        """TODO: Return number of available spots."""
        raise NotImplementedError("Return available space")

    def clean(self) -> str:
        """TODO: Clean enclosure and return status message."""
        raise NotImplementedError("Clean enclosure")

    def get_cleanliness(self) -> str:
        """TODO: Return cleanliness level (clean, needs_cleaning, dirty)."""
        raise NotImplementedError("Return cleanliness")

    def needs_cleaning(self) -> bool:
        """TODO: Return True if enclosure needs cleaning."""
        raise NotImplementedError("Check if needs cleaning")

    def get_status(self) -> dict[str, Any]:
        """TODO: Return complete enclosure status."""
        raise NotImplementedError("Return status")

    def get_animals_by_species(self, species: str) -> list[Animal]:
        """TODO: Filter animals by species."""
        raise NotImplementedError("Filter by species")

    def is_compatible(self, animal: Animal) -> bool:
        """TODO: Check if animal type is compatible with enclosure.
        
        Example: Birds need aviary, rabbits need ground enclosure.
        """
        raise NotImplementedError("Check compatibility")
