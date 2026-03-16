"""Adoption module - reference solution.

Handles adoption workflows and records.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import Any


class AdoptionStatus(Enum):
    """Adoption status states."""
    PENDING = auto()
    UNDER_REVIEW = auto()
    APPROVED = auto()
    REJECTED = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class AdoptionApplication:
    """Represents an adoption application."""

    _id_counter = 0

    def __init__(
        self,
        applicant_name: str,
        applicant_contact: str,
        animal_id: str,
        home_type: str = "house",
        has_yard: bool = False,
        other_pets: list[str] | None = None,
        experience_level: str = "beginner",
    ) -> None:
        AdoptionApplication._id_counter += 1
        self._application_id = f"APP{AdoptionApplication._id_counter:04d}"
        self.applicant_name = applicant_name
        self.applicant_contact = applicant_contact
        self.animal_id = animal_id
        self.home_type = home_type
        self.has_yard = has_yard
        self.other_pets = other_pets or []
        self.experience_level = experience_level
        self._status = AdoptionStatus.PENDING
        self._timeline: list[dict[str, Any]] = []
        self._reviewer_id: str | None = None
        self._rejection_reason: str = ""
        self._created_at = datetime.now().isoformat()
        
        # Initial timeline entry
        self._add_timeline_entry("created", "Application submitted")

    @property
    def application_id(self) -> str:
        return self._application_id

    @property
    def status(self) -> AdoptionStatus:
        return self._status

    def _add_timeline_entry(self, action: str, notes: str = "") -> None:
        self._timeline.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "notes": notes,
        })

    def submit(self) -> str:
        """Submit application."""
        self._add_timeline_entry("submitted")
        return f"Application {self._application_id} submitted for {self.animal_id}"

    def review(self, reviewer_id: str) -> str:
        """Move to UNDER_REVIEW status."""
        if self._status != AdoptionStatus.PENDING:
            return f"Cannot review application in {self._status.name} status"
        self._status = AdoptionStatus.UNDER_REVIEW
        self._reviewer_id = reviewer_id
        self._add_timeline_entry("review_started", f"Reviewer: {reviewer_id}")
        return f"Application {self._application_id} under review by {reviewer_id}"

    def approve(self, approver_id: str, notes: str = "") -> str:
        """Approve application."""
        if self._status not in (AdoptionStatus.PENDING, AdoptionStatus.UNDER_REVIEW):
            return f"Cannot approve application in {self._status.name} status"
        self._status = AdoptionStatus.APPROVED
        self._add_timeline_entry("approved", f"Approved by {approver_id}: {notes}")
        return f"Application {self._application_id} approved by {approver_id}"

    def reject(self, reason: str) -> str:
        """Reject application with reason."""
        if self._status == AdoptionStatus.COMPLETED:
            return "Cannot reject completed application"
        self._status = AdoptionStatus.REJECTED
        self._rejection_reason = reason
        self._add_timeline_entry("rejected", reason)
        return f"Application {self._application_id} rejected: {reason}"

    def complete(self) -> str:
        """Complete the adoption."""
        if self._status != AdoptionStatus.APPROVED:
            return f"Cannot complete application in {self._status.name} status"
        self._status = AdoptionStatus.COMPLETED
        self._add_timeline_entry("completed", "Adoption finalized")
        return f"Application {self._application_id} completed"

    def cancel(self, reason: str = "") -> str:
        """Cancel application."""
        if self._status == AdoptionStatus.COMPLETED:
            return "Cannot cancel completed application"
        self._status = AdoptionStatus.CANCELLED
        self._add_timeline_entry("cancelled", reason)
        return f"Application {self._application_id} cancelled: {reason}"

    def get_timeline(self) -> list[dict[str, Any]]:
        """Return application timeline."""
        return self._timeline.copy()

    def to_dict(self) -> dict[str, Any]:
        return {
            "application_id": self._application_id,
            "applicant_name": self.applicant_name,
            "applicant_contact": self.applicant_contact,
            "animal_id": self.animal_id,
            "status": self._status.name,
            "home_type": self.home_type,
            "has_yard": self.has_yard,
            "other_pets": self.other_pets,
            "experience_level": self.experience_level,
            "created_at": self._created_at,
        }


class AdoptionRecord:
    """Record of a completed adoption."""

    _id_counter = 0

    def __init__(
        self,
        application: AdoptionApplication,
        final_fee: float,
        follow_up_date: datetime | None = None,
    ) -> None:
        AdoptionRecord._id_counter += 1
        self._record_id = f"REC{AdoptionRecord._id_counter:04d}"
        self.application = application
        self.final_fee = final_fee
        self.completion_date = datetime.now()
        self.follow_up_date = follow_up_date
        self._follow_up_notes: list[dict[str, Any]] = []

    @property
    def record_id(self) -> str:
        return self._record_id

    def add_follow_up_note(self, note: str) -> None:
        """Add follow-up note."""
        self._follow_up_notes.append({
            "timestamp": datetime.now().isoformat(),
            "note": note,
        })

    def get_follow_up_notes(self) -> list[dict[str, Any]]:
        """Return follow-up notes."""
        return self._follow_up_notes.copy()

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self._record_id,
            "application_id": self.application.application_id,
            "animal_id": self.application.animal_id,
            "adopter_name": self.application.applicant_name,
            "final_fee": self.final_fee,
            "completion_date": self.completion_date.isoformat(),
        }


class AdoptionManager:
    """Manages adoption applications and records."""

    def __init__(self) -> None:
        self._applications: dict[str, AdoptionApplication] = {}
        self._records: dict[str, AdoptionRecord] = {}

    def submit_application(
        self,
        applicant_name: str,
        applicant_contact: str,
        animal_id: str,
        **kwargs: Any,
    ) -> AdoptionApplication:
        """Create and submit new application."""
        app = AdoptionApplication(
            applicant_name=applicant_name,
            applicant_contact=applicant_contact,
            animal_id=animal_id,
            **kwargs,
        )
        app.submit()
        self._applications[app.application_id] = app
        return app

    def get_application(self, application_id: str) -> AdoptionApplication | None:
        """Get application by ID."""
        return self._applications.get(application_id)

    def get_applications_by_status(self, status: AdoptionStatus) -> list[AdoptionApplication]:
        """Filter applications by status."""
        return [app for app in self._applications.values() if app.status == status]

    def get_applications_for_animal(self, animal_id: str) -> list[AdoptionApplication]:
        """Get all applications for specific animal."""
        return [
            app for app in self._applications.values()
            if app.animal_id == animal_id
        ]

    def create_record(
        self,
        application: AdoptionApplication,
        final_fee: float,
    ) -> AdoptionRecord:
        """Create adoption record from approved application."""
        record = AdoptionRecord(application, final_fee)
        self._records[record.record_id] = record
        return record

    def get_record(self, record_id: str) -> AdoptionRecord | None:
        """Get adoption record by ID."""
        return self._records.get(record_id)

    def get_statistics(self) -> dict[str, Any]:
        """Return adoption statistics."""
        total = len(self._applications)
        by_status = {}
        for status in AdoptionStatus:
            count = len(self.get_applications_by_status(status))
            by_status[status.name.lower()] = count
        
        return {
            "total_applications": total,
            "total_completed": len(self._records),
            "by_status": by_status,
        }
