"""Animal module - reference solution.

Demonstrates inheritance with an abstract Animal base class
and concrete implementations for different species.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime


class MedicalRecord:
    """Medical record for an animal using composition."""

    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    def add_entry(self, entry_type: str, description: str, vet_name: str) -> None:
        """Add a medical entry with timestamp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": entry_type,
            "description": description,
            "vet": vet_name,
        }
        self._history.append(entry)

    def get_history(self) -> list[dict[str, Any]]:
        """Return complete medical history."""
        return self._history.copy()

    def get_latest_entry(self) -> dict[str, Any] | None:
        """Return most recent entry or None if empty."""
        if not self._history:
            return None
        return self._history[-1].copy()


class Animal(ABC):
    """Abstract base class for all animals."""

    _id_counter = 0

    def __init__(
        self,
        name: str,
        age: int,
        species: str,
        health_status: str = "healthy",
    ) -> None:
        Animal._id_counter += 1
        self._animal_id = f"A{Animal._id_counter:04d}"
        self.name = name
        self.age = age
        self.species = species
        self.health_status = health_status
        self.is_adoptable = True
        self._medical_record = MedicalRecord()

    @property
    def animal_id(self) -> str:
        return self._animal_id

    @abstractmethod
    def make_sound(self) -> str:
        """Return the sound this animal makes."""
        pass

    @abstractmethod
    def get_care_instructions(self) -> str:
        """Return care instructions specific to this animal type."""
        pass

    @abstractmethod
    def get_species_traits(self) -> dict[str, Any]:
        """Return dictionary of species-specific traits."""
        pass

    def update_health_status(self, status: str) -> None:
        self.health_status = status

    def add_medical_note(self, note_type: str, description: str, vet_name: str) -> None:
        """Add note to medical record (uses composition)."""
        self._medical_record.add_entry(note_type, description, vet_name)

    def get_medical_history(self) -> list[dict[str, Any]]:
        """Return medical history."""
        return self._medical_record.get_history()

    def to_dict(self) -> dict[str, Any]:
        return {
            "animal_id": self.animal_id,
            "name": self.name,
            "age": self.age,
            "species": self.species,
            "health_status": self.health_status,
            "is_adoptable": self.is_adoptable,
        }


class Dog(Animal):
    """Dog class inheriting from Animal."""

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
        super().__init__(name, age, "dog")
        self.breed = breed
        self.size = size
        self.training_level = training_level
        self.good_with_kids = good_with_kids

    def make_sound(self) -> str:
        return "Woof!"

    def get_care_instructions(self) -> str:
        return f"Walk daily, train regularly. {self.name} is a {self.breed} with training level {self.training_level}."

    def get_species_traits(self) -> dict[str, Any]:
        return {
            "breed": self.breed,
            "size": self.size,
            "training_level": self.training_level,
            "good_with_kids": self.good_with_kids,
        }

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(self.get_species_traits())
        return data


class Cat(Animal):
    """Cat class inheriting from Animal."""

    def __init__(
        self,
        name: str,
        age: int,
        indoor_only: bool = True,
        litter_trained: bool = True,
        declawed: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, age, "cat")
        self.indoor_only = indoor_only
        self.litter_trained = litter_trained
        self.declawed = declawed

    def make_sound(self) -> str:
        return "Meow!"

    def get_care_instructions(self) -> str:
        indoor_status = "indoor" if self.indoor_only else "indoor/outdoor"
        return f"Provide {indoor_status} environment, clean litter box daily."

    def get_species_traits(self) -> dict[str, Any]:
        return {
            "indoor_only": self.indoor_only,
            "litter_trained": self.litter_trained,
            "declawed": self.declawed,
        }

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(self.get_species_traits())
        return data


class Bird(Animal):
    """Bird class inheriting from Animal."""

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
        super().__init__(name, age, species)
        self.wingspan_cm = wingspan_cm
        self.can_fly = can_fly
        self.talkative = talkative

    def make_sound(self) -> str:
        if self.talkative:
            return "Hello! Pretty bird!"
        return "Tweet!"

    def get_care_instructions(self) -> str:
        flying_status = "can fly" if self.can_fly else "flightless"
        return f"Provide spacious cage, fresh seeds daily. {self.name} is {flying_status}."

    def get_species_traits(self) -> dict[str, Any]:
        return {
            "wingspan_cm": self.wingspan_cm,
            "can_fly": self.can_fly,
            "talkative": self.talkative,
        }

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(self.get_species_traits())
        return data


class Rabbit(Animal):
    """Rabbit class inheriting from Animal."""

    def __init__(
        self,
        name: str,
        age: int,
        ear_type: str = "upright",
        hop_score: int = 5,
        litter_trained: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, age, "rabbit")
        self.ear_type = ear_type
        self.hop_score = hop_score
        self.litter_trained = litter_trained

    def make_sound(self) -> str:
        return "Squeak!"

    def get_care_instructions(self) -> str:
        litter_status = "litter trained" if self.litter_trained else "not litter trained"
        return f"Provide hay, fresh vegetables. {self.name} has {self.ear_type} ears and is {litter_status}."

    def get_species_traits(self) -> dict[str, Any]:
        return {
            "ear_type": self.ear_type,
            "hop_score": self.hop_score,
            "litter_trained": self.litter_trained,
        }

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(self.get_species_traits())
        return data
