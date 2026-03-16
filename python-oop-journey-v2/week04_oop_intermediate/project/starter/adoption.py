"""Adoption module - starter code.

This module handles adoption workflows and records.
TODO: Implement all methods marked with NotImplementedError.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import Any


class AdoptionStatus(Enum):
    """TODO: Define adoption status states:
    - PENDING
    - UNDER_REVIEW
    - APPROVED
    - REJECTED
    - COMPLETED
    - CANCELLED
    """
    raise NotImplementedError("Define status enum")


class AdoptionApplication:
    """Represents an adoption application.
    
    TODO: Implement application lifecycle management.
    """

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
        """TODO: Initialize application with PENDING status."""
        raise NotImplementedError("Initialize application")

    @property
    def application_id(self) -> str:
        """TODO: Return unique application ID."""
        raise NotImplementedError("Return application_id")

    @property
    def status(self) -> AdoptionStatus:
        """TODO: Return current status."""
        raise NotImplementedError("Return status")

    def submit(self) -> str:
        """TODO: Submit application, return confirmation message."""
        raise NotImplementedError("Submit application")

    def review(self, reviewer_id: str) -> str:
        """TODO: Move to UNDER_REVIEW status."""
        raise NotImplementedError("Review application")

    def approve(self, approver_id: str, notes: str = "") -> str:
        """TODO: Approve application."""
        raise NotImplementedError("Approve application")

    def reject(self, reason: str) -> str:
        """TODO: Reject application with reason."""
        raise NotImplementedError("Reject application")

    def complete(self) -> str:
        """TODO: Complete the adoption."""
        raise NotImplementedError("Complete adoption")

    def cancel(self, reason: str = "") -> str:
        """TODO: Cancel application."""
        raise NotImplementedError("Cancel application")

    def get_timeline(self) -> list[dict[str, Any]]:
        """TODO: Return application timeline."""
        raise NotImplementedError("Return timeline")

    def to_dict(self) -> dict[str, Any]:
        """TODO: Return application data as dictionary."""
        raise NotImplementedError("Convert to dict")


class AdoptionRecord:
    """Record of a completed adoption.
    
    TODO: Implement adoption record.
    """

    def __init__(
        self,
        application: AdoptionApplication,
        final_fee: float,
        follow_up_date: datetime | None = None,
    ) -> None:
        """TODO: Initialize adoption record."""
        raise NotImplementedError("Initialize record")

    @property
    def record_id(self) -> str:
        """TODO: Return record ID."""
        raise NotImplementedError("Return record_id")

    def add_follow_up_note(self, note: str) -> None:
        """TODO: Add follow-up note."""
        raise NotImplementedError("Add follow-up note")

    def get_follow_up_notes(self) -> list[dict[str, Any]]:
        """TODO: Return follow-up notes."""
        raise NotImplementedError("Return follow-up notes")

    def to_dict(self) -> dict[str, Any]:
        """TODO: Return record as dictionary."""
        raise NotImplementedError("Convert to dict")


class AdoptionManager:
    """Manages adoption applications and records.
    
    TODO: Implement adoption management.
    """

    def __init__(self) -> None:
        """TODO: Initialize with empty collections."""
        raise NotImplementedError("Initialize manager")

    def submit_application(
        self,
        applicant_name: str,
        applicant_contact: str,
        animal_id: str,
        **kwargs: Any,
    ) -> AdoptionApplication:
        """TODO: Create and submit new application."""
        raise NotImplementedError("Submit application")

    def get_application(self, application_id: str) -> AdoptionApplication | None:
        """TODO: Get application by ID."""
        raise NotImplementedError("Get application")

    def get_applications_by_status(self, status: AdoptionStatus) -> list[AdoptionApplication]:
        """TODO: Filter applications by status."""
        raise NotImplementedError("Filter by status")

    def get_applications_for_animal(self, animal_id: str) -> list[AdoptionApplication]:
        """TODO: Get all applications for specific animal."""
        raise NotImplementedError("Get applications for animal")

    def create_record(
        self,
        application: AdoptionApplication,
        final_fee: float,
    ) -> AdoptionRecord:
        """TODO: Create adoption record from approved application."""
        raise NotImplementedError("Create record")

    def get_record(self, record_id: str) -> AdoptionRecord | None:
        """TODO: Get adoption record by ID."""
        raise NotImplementedError("Get record")

    def get_statistics(self) -> dict[str, Any]:
        """TODO: Return adoption statistics."""
        raise NotImplementedError("Return statistics")
