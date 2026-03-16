"""Shelter module - reference solution.

Main shelter management class that composes all components.
"""

from __future__ import annotations

from typing import Any

from .animal import Animal
from .staff import StaffMember, Caretaker, AdoptionCoordinator, Veterinarian
from .enclosure import Enclosure
from .adoption import (
    AdoptionApplication,
    AdoptionRecord,
    AdoptionManager,
    AdoptionStatus,
)


class Shelter:
    """Main shelter management class."""

    def __init__(self, name: str, address: str = "") -> None:
        self.name = name
        self.address = address
        self._enclosures: dict[str, Enclosure] = {}
        self._staff: dict[str, StaffMember] = {}
        self._adoption_manager = AdoptionManager()
        self._animal_to_enclosure: dict[str, str] = {}
        self._animal_assignments: dict[str, list[str]] = {}  # animal_id -> staff_ids

    # Animal Management

    def intake_animal(
        self,
        animal: Animal,
        enclosure_id: str | None = None,
    ) -> dict[str, Any]:
        """Accept new animal into shelter."""
        if enclosure_id:
            enclosure = self._enclosures.get(enclosure_id)
            if not enclosure:
                return {"success": False, "message": f"Enclosure {enclosure_id} not found"}
            result = enclosure.add_animal(animal)
            if result["success"]:
                self._animal_to_enclosure[animal.animal_id] = enclosure_id
            return result
        
        # Find suitable enclosure
        for enc_id, enclosure in self._enclosures.items():
            if enclosure.has_space() and enclosure.is_compatible(animal):
                result = enclosure.add_animal(animal)
                if result["success"]:
                    self._animal_to_enclosure[animal.animal_id] = enc_id
                return {**result, "enclosure_id": enc_id}
        
        return {"success": False, "message": "No suitable enclosure available"}

    def get_animal(self, animal_id: str) -> Animal | None:
        """Get animal by ID from any enclosure."""
        for enclosure in self._enclosures.values():
            for animal in enclosure.get_animals():
                if animal.animal_id == animal_id:
                    return animal
        return None

    def get_all_animals(self) -> list[Animal]:
        """Return all animals in shelter."""
        all_animals = []
        for enclosure in self._enclosures.values():
            all_animals.extend(enclosure.get_animals())
        return all_animals

    def get_animals_by_species(self, species: str) -> list[Animal]:
        """Filter animals by species."""
        return [a for a in self.get_all_animals() if a.species == species]

    def get_available_animals(self) -> list[Animal]:
        """Return animals available for adoption."""
        return [
            a for a in self.get_all_animals()
            if a.is_adoptable and a.health_status == "healthy"
        ]

    def update_animal_health(
        self,
        animal_id: str,
        health_status: str,
        vet_id: str,
        notes: str,
    ) -> dict[str, Any]:
        """Update animal health with vet notes."""
        animal = self.get_animal(animal_id)
        if not animal:
            return {"success": False, "message": "Animal not found"}
        
        vet = self._staff.get(vet_id)
        if not vet or not isinstance(vet, Veterinarian):
            return {"success": False, "message": "Valid veterinarian required"}
        
        animal.update_health_status(health_status)
        animal.add_medical_note("health_update", notes, vet.name)
        
        return {
            "success": True,
            "message": f"Health updated for {animal.name}",
            "new_status": health_status,
        }

    # Staff Management

    def hire_staff(self, staff_member: StaffMember) -> str:
        """Add staff member to shelter."""
        self._staff[staff_member.staff_id] = staff_member
        return f"Hired {staff_member.name} as {staff_member.role}"

    def get_staff(self, staff_id: str) -> StaffMember | None:
        """Get staff member by ID."""
        return self._staff.get(staff_id)

    def get_all_staff(self) -> list[StaffMember]:
        """Return all staff members."""
        return list(self._staff.values())

    def get_staff_by_role(self, role: str) -> list[StaffMember]:
        """Filter staff by role."""
        return [s for s in self._staff.values() if s.role == role]

    def assign_staff_to_animal(
        self,
        staff_id: str,
        animal_id: str,
    ) -> dict[str, Any]:
        """Assign caretaker to animal."""
        staff = self._staff.get(staff_id)
        if not staff:
            return {"success": False, "message": "Staff not found"}
        
        animal = self.get_animal(animal_id)
        if not animal:
            return {"success": False, "message": "Animal not found"}
        
        if not isinstance(staff, Caretaker):
            return {"success": False, "message": "Only caretakers can be assigned to animals"}
        
        staff.assign_to_animal(animal_id)
        
        if animal_id not in self._animal_assignments:
            self._animal_assignments[animal_id] = []
        if staff_id not in self._animal_assignments[animal_id]:
            self._animal_assignments[animal_id].append(staff_id)
        
        return {
            "success": True,
            "message": f"{staff.name} assigned to {animal.name}",
        }

    def get_staff_for_animal(self, animal_id: str) -> list[StaffMember]:
        """Get staff assigned to animal."""
        staff_ids = self._animal_assignments.get(animal_id, [])
        return [self._staff[sid] for sid in staff_ids if sid in self._staff]

    # Enclosure Management

    def add_enclosure(self, enclosure: Enclosure) -> str:
        """Add enclosure to shelter."""
        self._enclosures[enclosure.enclosure_id] = enclosure
        return f"Added enclosure {enclosure.name}"

    def get_enclosure(self, enclosure_id: str) -> Enclosure | None:
        """Get enclosure by ID."""
        return self._enclosures.get(enclosure_id)

    def get_all_enclosures(self) -> list[Enclosure]:
        """Return all enclosures."""
        return list(self._enclosures.values())

    def clean_enclosure(self, enclosure_id: str, staff_id: str) -> dict[str, Any]:
        """Clean enclosure (requires caretaker)."""
        enclosure = self._enclosures.get(enclosure_id)
        if not enclosure:
            return {"success": False, "message": "Enclosure not found"}
        
        staff = self._staff.get(staff_id)
        if not staff or not isinstance(staff, Caretaker):
            return {"success": False, "message": "Caretaker required for cleaning"}
        
        result = enclosure.clean()
        return {"success": True, "message": result}

    # Adoption Management

    def submit_adoption_application(
        self,
        applicant_name: str,
        animal_id: str,
        applicant_contact: str = "",
        **kwargs: Any,
    ) -> AdoptionApplication:
        """Submit adoption application."""
        return self._adoption_manager.submit_application(
            applicant_name=applicant_name,
            applicant_contact=applicant_contact,
            animal_id=animal_id,
            **kwargs,
        )

    def get_adoption_application(self, application_id: str) -> AdoptionApplication | None:
        """Get application by ID."""
        return self._adoption_manager.get_application(application_id)

    def process_adoption_application(
        self,
        application_id: str,
        staff_id: str,
        decision: str,
        notes: str = "",
    ) -> dict[str, Any]:
        """Approve or reject application (requires coordinator)."""
        application = self._adoption_manager.get_application(application_id)
        if not application:
            return {"success": False, "message": "Application not found"}
        
        staff = self._staff.get(staff_id)
        if not staff or not isinstance(staff, AdoptionCoordinator):
            return {"success": False, "message": "Adoption coordinator required"}
        
        if decision.lower() == "approve":
            result = application.approve(staff_id, notes)
            staff.process_application(application.applicant_name)
            return {"success": True, "message": result}
        elif decision.lower() == "reject":
            result = application.reject(notes)
            return {"success": True, "message": result}
        else:
            return {"success": False, "message": "Invalid decision"}

    def complete_adoption(
        self,
        application_id: str,
        final_fee: float,
    ) -> AdoptionRecord:
        """Complete adoption and create record."""
        application = self._adoption_manager.get_application(application_id)
        if not application:
            raise ValueError("Application not found")
        
        result = application.complete()
        
        # Mark animal as adopted (remove from available)
        animal = self.get_animal(application.animal_id)
        if animal:
            animal.is_adoptable = False
        
        return self._adoption_manager.create_record(application, final_fee)

    def get_adoption_record(self, record_id: str) -> AdoptionRecord | None:
        """Get adoption record."""
        return self._adoption_manager.get_record(record_id)

    # Reporting

    def get_shelter_statistics(self) -> dict[str, Any]:
        """Return comprehensive shelter statistics."""
        all_animals = self.get_all_animals()
        species_counts: dict[str, int] = {}
        for animal in all_animals:
            species_counts[animal.species] = species_counts.get(animal.species, 0) + 1
        
        return {
            "shelter_name": self.name,
            "total_animals": len(all_animals),
            "available_for_adoption": len(self.get_available_animals()),
            "total_enclosures": len(self._enclosures),
            "total_staff": len(self._staff),
            "species_breakdown": species_counts,
            "adoption_stats": self._adoption_manager.get_statistics(),
        }

    def generate_daily_report(self) -> dict[str, Any]:
        """Generate daily operations report."""
        enclosure_statuses = [
            enc.get_status() for enc in self._enclosures.values()
        ]
        
        pending_apps = self._adoption_manager.get_applications_by_status(
            AdoptionStatus.PENDING
        )
        
        return {
            "report_date": "today",
            "shelter": self.name,
            "enclosures": enclosure_statuses,
            "pending_applications": len(pending_apps),
            "total_animals": len(self.get_all_animals()),
        }

    # Polymorphic Operations

    def perform_staff_duties(self, staff_id: str, context: dict[str, Any] | None = None) -> str:
        """Trigger staff duties polymorphically."""
        staff = self._staff.get(staff_id)
        if not staff:
            return "Staff not found"
        return staff.perform_duties(context)

    def make_animal_sound(self, animal_id: str) -> str:
        """Get animal sound polymorphically."""
        animal = self.get_animal(animal_id)
        if not animal:
            return "Animal not found"
        return animal.make_sound()
