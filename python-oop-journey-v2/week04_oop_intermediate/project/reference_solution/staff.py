"""Staff module - reference solution.

Demonstrates polymorphism with different staff roles
implementing the same interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class StaffMember(ABC):
    """Abstract base class for all staff members."""

    _id_counter = 0

    def __init__(self, name: str, contact_info: str) -> None:
        StaffMember._id_counter += 1
        self._staff_id = f"S{StaffMember._id_counter:04d}"
        self.name = name
        self.contact_info = contact_info

    @property
    def staff_id(self) -> str:
        return self._staff_id

    @property
    @abstractmethod
    def role(self) -> str:
        """Return role identifier."""
        pass

    @abstractmethod
    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        """Perform role-specific duties (polymorphic method)."""
        pass

    @abstractmethod
    def can_handle_task(self, task_type: str) -> bool:
        """Return True if this role can handle the task type."""
        pass

    def contact(self) -> str:
        return f"Contact {self.name} at {self.contact_info}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "role": self.role,
            "contact_info": self.contact_info,
        }


class Veterinarian(StaffMember):
    """Veterinarian role."""

    VALID_TASKS = {"medical", "examination", "surgery", "vaccination", "treatment"}

    def __init__(
        self,
        name: str,
        contact_info: str,
        specialization: str,
        license_number: str,
    ) -> None:
        super().__init__(name, contact_info)
        self.specialization = specialization
        self.license_number = license_number

    @property
    def role(self) -> str:
        return "veterinarian"

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        if context and "animal_name" in context:
            return f"Dr. {self.name} is examining {context['animal_name']}"
        return f"Dr. {self.name} is performing veterinary duties"

    def can_handle_task(self, task_type: str) -> bool:
        return task_type.lower() in self.VALID_TASKS

    def examine_animal(self, animal_name: str) -> str:
        return f"Dr. {self.name} examines {animal_name}: Health check complete."

    def prescribe_treatment(self, animal_name: str, treatment: str) -> str:
        return f"Dr. {self.name} prescribes {treatment} for {animal_name}."

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update({
            "specialization": self.specialization,
            "license_number": self.license_number,
        })
        return data


class Caretaker(StaffMember):
    """Caretaker role."""

    VALID_TASKS = {"feeding", "cleaning", "exercise", "grooming", "walking", "socialization"}

    def __init__(
        self,
        name: str,
        contact_info: str,
        shift: str = "day",
    ) -> None:
        super().__init__(name, contact_info)
        self.shift = shift
        self._assigned_animals: list[str] = []

    @property
    def role(self) -> str:
        return "caretaker"

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        duty_msg = f"{self.name} is caring for animals on {self.shift} shift"
        if self._assigned_animals:
            duty_msg += f" (assigned: {len(self._assigned_animals)} animals)"
        return duty_msg

    def can_handle_task(self, task_type: str) -> bool:
        return task_type.lower() in self.VALID_TASKS

    def assign_to_animal(self, animal_id: str) -> None:
        if animal_id not in self._assigned_animals:
            self._assigned_animals.append(animal_id)

    def get_assigned_animals(self) -> list[str]:
        return self._assigned_animals.copy()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["shift"] = self.shift
        data["assigned_animals"] = len(self._assigned_animals)
        return data


class AdoptionCoordinator(StaffMember):
    """Adoption coordinator role."""

    VALID_TASKS = {"adoption", "screening", "matching", "interview", "paperwork"}

    def __init__(self, name: str, contact_info: str) -> None:
        super().__init__(name, contact_info)
        self._applications_processed = 0

    @property
    def role(self) -> str:
        return "adoption_coordinator"

    def perform_duties(self, context: dict[str, Any] | None = None) -> str:
        return f"{self.name} is coordinating adoptions (processed: {self._applications_processed})"

    def can_handle_task(self, task_type: str) -> bool:
        return task_type.lower() in self.VALID_TASKS

    def process_application(self, applicant_name: str) -> str:
        self._applications_processed += 1
        return f"{self.name} processed application from {applicant_name}"

    def get_applications_processed(self) -> int:
        return self._applications_processed

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["applications_processed"] = self._applications_processed
        return data
