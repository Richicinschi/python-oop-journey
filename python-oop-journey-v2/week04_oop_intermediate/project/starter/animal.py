"""Animal module - starter code.

This module defines the animal hierarchy using inheritance.
TODO: Implement all methods marked with NotImplementedError.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime


class MedicalRecord:
    """Medical record for an animal using composition."""

    def __init__(self) -> None:
        """TODO: Initialize medical record with empty history."""
        raise NotImplementedError("Initialize empty medical history")

    def add_entry(self, entry_type: str, description: str, vet_name: str) -> None:
        """TODO: Add a medical entry with timestamp."""
        raise NotImplementedError("Add entry with current timestamp")

    def get_history(self) -> list[dict[str, Any]]:
        """TODO: Return complete medical history."""
        raise NotImplementedError("Return medical history")

    def get_latest_entry(self) -> dict[str, Any] | None:
        """TODO: Return most recent entry or None if empty."""
        raise NotImplementedError("Return latest entry")


class Animal(ABC):
    """Abstract base class for all animals.
    
    This is the root of our inheritance hierarchy.
    All animals share these fundamental characteristics.
    """

    _id_counter = 0

    def __init__(
        self,
        name: str,
        age: int,
        species: str,
        health_status: str = "healthy",
    ) -> None:
        """TODO: Initialize animal with auto-generated ID."""
        raise NotImplementedError("Initialize with unique ID")

    @property
    def animal_id(self) -> str:
        """TODO: Return unique animal ID."""
        raise NotImplementedError("Return animal_id")

    @abstractmethod
    def make_sound(self) -> str:
        """TODO: Return the sound this animal makes."""
        raise NotImplementedError("Implement sound")

    @abstractmethod
    def get_care_instructions(self) -> str:
        """TODO: Return care instructions specific to this animal type."""
        raise NotImplementedError("Implement care instructions")

    @abstractmethod
    def get_species_traits(self) -> dict[str, Any]:
        """TODO: Return dictionary of species-specific traits."""
        raise NotImplementedError("Implement traits")

    def update_health_status(self, status: str) -> None:
        """TODO: Update health status."""
        raise NotImplementedError("Update health status")

    def add_medical_note(self, note_type: str, description: str, vet_name: str) -> None:
        """TODO: Add note to medical record (uses composition)."""
        raise NotImplementedError("Add to medical record")

    def get_medical_history(self) -> list[dict[str, Any]]:
        """TODO: Return medical history."""
        raise NotImplementedError("Return medical history")

    def to_dict(self) -> dict[str, Any]:
        """TODO: Return animal data as dictionary."""
        raise NotImplementedError("Convert to dict")


class Dog(Animal):
    """Dog class inheriting from Animal.
    
    TODO: Implement dog-specific attributes and behaviors.
    """

    def __init__(
        self,
        name: str,
        age: int,
        breed: str,
        size: str = "medium",
        training_level: int = 5,
        good_with_kids: bool = True,
        **kwargs: Any,
    ) -> None:
        """TODO: Initialize dog with breed-specific attributes."""
        raise NotImplementedError("Initialize dog")

    def make_sound(self) -> str:
        """TODO: Return 'Woof!'."""
        raise NotImplementedError("Implement dog sound")

    def get_care_instructions(self) -> str:
        """TODO: Return dog care instructions."""
        raise NotImplementedError("Implement care instructions")

    def get_species_traits(self) -> dict[str, Any]:
        """TODO: Return dog traits."""
        raise NotImplementedError("Implement traits")


class Cat(Animal):
    """Cat class inheriting from Animal.
    
    TODO: Implement cat-specific attributes and behaviors.
    """

    def __init__(
        self,
        name: str,
        age: int,
        indoor_only: bool = True,
        litter_trained: bool = True,
        declawed: bool = False,
        **kwargs: Any,
    ) -> None:
        """TODO: Initialize cat with cat-specific attributes."""
        raise NotImplementedError("Initialize cat")

    def make_sound(self) -> str:
        """TODO: Return 'Meow!'."""
        raise NotImplementedError("Implement cat sound")

    def get_care_instructions(self) -> str:
        """TODO: Return cat care instructions."""
        raise NotImplementedError("Implement care instructions")

    def get_species_traits(self) -> dict[str, Any]:
        """TODO: Return cat traits."""
        raise NotImplementedError("Implement traits")


class Bird(Animal):
    """Bird class inheriting from Animal.
    
    TODO: Implement bird-specific attributes and behaviors.
    """

    def __init__(
        self,
        name: str,
        age: int,
        species: str,
        wingspan_cm: float,
        can_fly: bool = True,
        talkative: bool = False,
        **kwargs: Any,
    ) -> None:
        """TODO: Initialize bird with bird-specific attributes."""
        raise NotImplementedError("Initialize bird")

    def make_sound(self) -> str:
        """TODO: Return 'Tweet!' or squawk depending on species."""
        raise NotImplementedError("Implement bird sound")

    def get_care_instructions(self) -> str:
        """TODO: Return bird care instructions."""
        raise NotImplementedError("Implement care instructions")

    def get_species_traits(self) -> dict[str, Any]:
        """TODO: Return bird traits."""
        raise NotImplementedError("Implement traits")


class Rabbit(Animal):
    """Rabbit class inheriting from Animal.
    
    TODO: Implement rabbit-specific attributes and behaviors.
    """

    def __init__(
        self,
        name: str,
        age: int,
        ear_type: str = "upright",
        hop_score: int = 5,
        litter_trained: bool = False,
        **kwargs: Any,
    ) -> None:
        """TODO: Initialize rabbit with rabbit-specific attributes."""
        raise NotImplementedError("Initialize rabbit")

    def make_sound(self) -> str:
        """TODO: Return 'Squeak!'."""
        raise NotImplementedError("Implement rabbit sound")

    def get_care_instructions(self) -> str:
        """TODO: Return rabbit care instructions."""
        raise NotImplementedError("Implement care instructions")

    def get_species_traits(self) -> dict[str, Any]:
        """TODO: Return rabbit traits."""
        raise NotImplementedError("Implement traits")
