"""Staff module - starter code.

This module defines staff roles using polymorphism.
TODO: Implement all methods marked with NotImplementedError.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class StaffMember(ABC):
    """Abstract base class for all staff members.
    
    Demonstrates polymorphism - different roles perform duties differently
    through the same interface.
    """

    _id_counter = 0

    def __init__(self, name: str, contact_info: str) -> None:
        """TODO: Initialize staff with auto-generated ID."""
        raise NotImplementedError("Initialize with unique ID")

    @property
    def staff_id(self) -> str:
        """TODO: Return unique staff ID."""
        raise NotImplementedError("Return staff_id")

    @property
    @abstractmethod
    def role(self) -> str:
        """TODO: Return role identifier."""
        raise NotImplementedError("Implement role")

    @abstractmethod
    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        """TODO: Perform role-specific duties (polymorphic method)."""
        raise NotImplementedError("Implement duties")

    @abstractmethod
    def can_handle_task(self, task_type: str) -> bool:
        """TODO: Return True if this role can handle the task type."""
        raise NotImplementedError("Implement task check")

    def contact(self) -> str:
        """TODO: Return contact message."""
        raise NotImplementedError("Implement contact")

    def to_dict(self) -> dict[str, Any]:
        """TODO: Return staff data as dictionary."""
        raise NotImplementedError("Convert to dict")


class Veterinarian(StaffMember):
    """Veterinarian role.
    
    TODO: Implement vet-specific duties and capabilities.
    """

    def __init__(
        self,
        name: str,
        contact_info: str,
        specialization: str,
        license_number: str,
    ) -> None:
        """TODO: Initialize veterinarian."""
        raise NotImplementedError("Initialize vet")

    @property
    def role(self) -> str:
        """TODO: Return 'veterinarian'."""
        raise NotImplementedError("Implement role")

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        """TODO: Return vet duty message, optionally examine animal from context."""
        raise NotImplementedError("Implement vet duties")

    def can_handle_task(self, task_type: str) -> bool:
        """TODO: Vets can handle: medical, examination, surgery."""
        raise NotImplementedError("Implement task check")

    def examine_animal(self, animal_name: str) -> str:
        """TODO: Return examination message."""
        raise NotImplementedError("Implement examination")

    def prescribe_treatment(self, animal_name: str, treatment: str) -> str:
        """TODO: Return prescription message."""
        raise NotImplementedError("Implement prescription")


class Caretaker(StaffMember):
    """Caretaker role.
    
    TODO: Implement caretaker-specific duties and capabilities.
    """

    def __init__(
        self,
        name: str,
        contact_info: str,
        shift: str = "day",
    ) -> None:
        """TODO: Initialize caretaker."""
        raise NotImplementedError("Initialize caretaker")

    @property
    def role(self) -> str:
        """TODO: Return 'caretaker'."""
        raise NotImplementedError("Implement role")

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        """TODO: Return caretaker duty message."""
        raise NotImplementedError("Implement caretaker duties")

    def can_handle_task(self, task_type: str) -> bool:
        """TODO: Caretakers can handle: feeding, cleaning, exercise, grooming."""
        raise NotImplementedError("Implement task check")

    def assign_to_animal(self, animal_id: str) -> None:
        """TODO: Add animal to assigned list."""
        raise NotImplementedError("Implement assignment")

    def get_assigned_animals(self) -> list[str]:
        """TODO: Return list of assigned animal IDs."""
        raise NotImplementedError("Return assigned animals")


class AdoptionCoordinator(StaffMember):
    """Adoption coordinator role.
    
    TODO: Implement coordinator-specific duties and capabilities.
    """

    def __init__(self, name: str, contact_info: str) -> None:
        """TODO: Initialize coordinator."""
        raise NotImplementedError("Initialize coordinator")

    @property
    def role(self) -> str:
        """TODO: Return 'adoption_coordinator'."""
        raise NotImplementedError("Implement role")

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        """TODO: Return coordinator duty message."""
        raise NotImplementedError("Implement coordinator duties")

    def can_handle_task(self, task_type: str) -> bool:
        """TODO: Coordinators can handle: adoption, screening, matching."""
        raise NotImplementedError("Implement task check")

    def process_application(self, applicant_name: str) -> str:
        """TODO: Return processing message."""
        raise NotImplementedError("Implement application processing")

    def get_applications_processed(self) -> int:
        """TODO: Return count of processed applications."""
        raise NotImplementedError("Return processed count")
