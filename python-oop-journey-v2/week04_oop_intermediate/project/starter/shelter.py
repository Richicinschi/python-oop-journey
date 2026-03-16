"""Shelter module - starter code.

Main shelter management class that composes all components.
TODO: Implement all methods marked with NotImplementedError.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .animal import Animal
    from .staff import StaffMember
    from .enclosure import Enclosure
    from .adoption import AdoptionApplication, AdoptionRecord, AdoptionManager


class Shelter:
    """Main shelter management class.
    
    This class demonstrates composition by bringing together:
    - Animals (via Enclosure composition)
    - Staff (polymorphic collection)
    - Adoption management
    
    TODO: Implement all shelter operations.
    """

    def __init__(self, name: str, address: str = "") -> None:
        """TODO: Initialize shelter with empty collections."""
        raise NotImplementedError("Initialize shelter")

    # Animal Management

    def intake_animal(
        self,
        animal: Animal,
        enclosure_id: str | None = None,
    ) -> dict[str, Any]:
        """TODO: Accept new animal into shelter.
        
        If enclosure_id provided, try to place there.
        Otherwise, find suitable enclosure.
        """
        raise NotImplementedError("Intake animal")

    def get_animal(self, animal_id: str) -> Animal | None:
        """TODO: Get animal by ID from any enclosure."""
        raise NotImplementedError("Get animal")

    def get_all_animals(self) -> list[Animal]:
        """TODO: Return all animals in shelter."""
        raise NotImplementedError("Get all animals")

    def get_animals_by_species(self, species: str) -> list[Animal]:
        """TODO: Filter animals by species."""
        raise NotImplementedError("Filter by species")

    def get_available_animals(self) -> list[Animal]:
        """TODO: Return animals available for adoption."""
        raise NotImplementedError("Get available animals")

    def update_animal_health(
        self,
        animal_id: str,
        health_status: str,
        vet_id: str,
        notes: str,
    ) -> dict[str, Any]:
        """TODO: Update animal health with vet notes."""
        raise NotImplementedError("Update health")

    # Staff Management

    def hire_staff(self, staff_member: StaffMember) -> str:
        """TODO: Add staff member to shelter."""
        raise NotImplementedError("Hire staff")

    def get_staff(self, staff_id: str) -> StaffMember | None:
        """TODO: Get staff member by ID."""
        raise NotImplementedError("Get staff")

    def get_all_staff(self) -> list[StaffMember]:
        """TODO: Return all staff members."""
        raise NotImplementedError("Get all staff")

    def get_staff_by_role(self, role: str) -> list[StaffMember]:
        """TODO: Filter staff by role."""
        raise NotImplementedError("Filter by role")

    def assign_staff_to_animal(
        self,
        staff_id: str,
        animal_id: str,
    ) -> dict[str, Any]:
        """TODO: Assign caretaker to animal."""
        raise NotImplementedError("Assign staff")

    def get_staff_for_animal(self, animal_id: str) -> list[StaffMember]:
        """TODO: Get staff assigned to animal."""
        raise NotImplementedError("Get staff for animal")

    # Enclosure Management

    def add_enclosure(self, enclosure: Enclosure) -> str:
        """TODO: Add enclosure to shelter."""
        raise NotImplementedError("Add enclosure")

    def get_enclosure(self, enclosure_id: str) -> Enclosure | None:
        """TODO: Get enclosure by ID."""
        raise NotImplementedError("Get enclosure")

    def get_all_enclosures(self) -> list[Enclosure]:
        """TODO: Return all enclosures."""
        raise NotImplementedError("Get all enclosures")

    def clean_enclosure(self, enclosure_id: str, staff_id: str) -> dict[str, Any]:
        """TODO: Clean enclosure (requires caretaker)."""
        raise NotImplementedError("Clean enclosure")

    # Adoption Management

    def submit_adoption_application(
        self,
        applicant_name: str,
        animal_id: str,
        applicant_contact: str = "",
        **kwargs: Any,
    ) -> AdoptionApplication:
        """TODO: Submit adoption application."""
        raise NotImplementedError("Submit application")

    def get_adoption_application(self, application_id: str) -> AdoptionApplication | None:
        """TODO: Get application by ID."""
        raise NotImplementedError("Get application")

    def process_adoption_application(
        self,
        application_id: str,
        staff_id: str,
        decision: str,
        notes: str = "",
    ) -> dict[str, Any]:
        """TODO: Approve or reject application (requires coordinator)."""
        raise NotImplementedError("Process application")

    def complete_adoption(
        self,
        application_id: str,
        final_fee: float,
    ) -> AdoptionRecord:
        """TODO: Complete adoption and create record."""
        raise NotImplementedError("Complete adoption")

    def get_adoption_record(self, record_id: str) -> AdoptionRecord | None:
        """TODO: Get adoption record."""
        raise NotImplementedError("Get record")

    # Reporting

    def get_shelter_statistics(self) -> dict[str, Any]:
        """TODO: Return comprehensive shelter statistics."""
        raise NotImplementedError("Get statistics")

    def generate_daily_report(self) -> dict[str, Any]:
        """TODO: Generate daily operations report."""
        raise NotImplementedError("Generate report")

    # Polymorphic Operations

    def perform_staff_duties(self, staff_id: str, context: dict[str, Any] | None = None) -> str:
        """TODO: Trigger staff duties polymorphically."""
        raise NotImplementedError("Perform duties")

    def make_animal_sound(self, animal_id: str) -> str:
        """TODO: Get animal sound polymorphically."""
        raise NotImplementedError("Make sound")
