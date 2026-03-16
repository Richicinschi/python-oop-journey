"""Comprehensive tests for Animal Shelter Management System.

Tests cover:
- Inheritance (Animal hierarchy)
- Polymorphism (Staff roles)
- Composition (Enclosure, MedicalRecord)
- Integration (Shelter operations)
- Adoption workflow
"""

from __future__ import annotations

import pytest
from week04_oop_intermediate.project.reference_solution.animal import (
    Animal,
    Bird,
    Cat,
    Dog,
    MedicalRecord,
    Rabbit,
)
from week04_oop_intermediate.project.reference_solution.staff import (
    AdoptionCoordinator,
    Caretaker,
    StaffMember,
    Veterinarian,
)
from week04_oop_intermediate.project.reference_solution.enclosure import Enclosure
from week04_oop_intermediate.project.reference_solution.adoption import (
    AdoptionApplication,
    AdoptionManager,
    AdoptionRecord,
    AdoptionStatus,
)
from week04_oop_intermediate.project.reference_solution.shelter import Shelter


# =============================================================================
# MedicalRecord Tests
# =============================================================================

class TestMedicalRecord:
    """Tests for MedicalRecord composition class."""

    def test_creation(self) -> None:
        record = MedicalRecord()
        assert record.get_history() == []

    def test_add_entry(self) -> None:
        record = MedicalRecord()
        record.add_entry("checkup", "Annual examination", "Dr. Smith")
        history = record.get_history()
        assert len(history) == 1
        assert history[0]["type"] == "checkup"
        assert history[0]["vet"] == "Dr. Smith"

    def test_get_latest_entry(self) -> None:
        record = MedicalRecord()
        assert record.get_latest_entry() is None
        record.add_entry("checkup", "First", "Dr. A")
        record.add_entry("vaccination", "Second", "Dr. B")
        latest = record.get_latest_entry()
        assert latest["type"] == "vaccination"

    def test_multiple_entries(self) -> None:
        record = MedicalRecord()
        for i in range(5):
            record.add_entry("visit", f"Visit {i}", "Dr. Smith")
        assert len(record.get_history()) == 5


# =============================================================================
# Animal Inheritance Tests
# =============================================================================

class TestAnimalBase:
    """Tests for Animal abstract base class."""

    def test_cannot_instantiate_base(self) -> None:
        with pytest.raises(TypeError):
            Animal("Test", 5, "unknown")

    def test_auto_id_generation(self) -> None:
        dog1 = Dog("Dog1", 3, "Labrador")
        dog2 = Dog("Dog2", 2, "Beagle")
        assert dog1.animal_id != dog2.animal_id
        assert dog1.animal_id.startswith("A")

    def test_health_status_update(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        assert dog.health_status == "healthy"
        dog.update_health_status("sick")
        assert dog.health_status == "sick"

    def test_is_adoptable_default(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        assert dog.is_adoptable is True

    def test_medical_record_composition(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        dog.add_medical_note("checkup", "Healthy", "Dr. Smith")
        history = dog.get_medical_history()
        assert len(history) == 1

    def test_to_dict(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        data = dog.to_dict()
        assert data["name"] == "Buddy"
        assert data["species"] == "dog"
        assert "animal_id" in data


class TestDog:
    """Tests for Dog class."""

    def test_creation(self) -> None:
        dog = Dog("Buddy", 3, "Golden Retriever", size="large", training_level=8)
        assert dog.name == "Buddy"
        assert dog.age == 3
        assert dog.breed == "Golden Retriever"
        assert dog.size == "large"
        assert dog.training_level == 8

    def test_species(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        assert dog.species == "dog"

    def test_make_sound(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        assert dog.make_sound() == "Woof!"

    def test_get_care_instructions(self) -> None:
        dog = Dog("Buddy", 3, "Golden", training_level=8)
        instructions = dog.get_care_instructions()
        assert "Walk daily" in instructions
        assert "Buddy" in instructions

    def test_get_species_traits(self) -> None:
        dog = Dog("Buddy", 3, "Golden", good_with_kids=True)
        traits = dog.get_species_traits()
        assert traits["breed"] == "Golden"
        assert traits["good_with_kids"] is True

    def test_is_animal(self) -> None:
        dog = Dog("Buddy", 3, "Golden")
        assert isinstance(dog, Animal)


class TestCat:
    """Tests for Cat class."""

    def test_creation(self) -> None:
        cat = Cat("Whiskers", 2, indoor_only=True, declawed=False)
        assert cat.name == "Whiskers"
        assert cat.indoor_only is True
        assert cat.declawed is False

    def test_species(self) -> None:
        cat = Cat("Whiskers", 2)
        assert cat.species == "cat"

    def test_make_sound(self) -> None:
        cat = Cat("Whiskers", 2)
        assert cat.make_sound() == "Meow!"

    def test_get_care_instructions_indoor(self) -> None:
        cat = Cat("Whiskers", 2, indoor_only=True)
        instructions = cat.get_care_instructions()
        assert "indoor" in instructions

    def test_get_care_instructions_outdoor(self) -> None:
        cat = Cat("Whiskers", 2, indoor_only=False)
        instructions = cat.get_care_instructions()
        assert "indoor/outdoor" in instructions

    def test_is_animal(self) -> None:
        cat = Cat("Whiskers", 2)
        assert isinstance(cat, Animal)


class TestBird:
    """Tests for Bird class."""

    def test_creation(self) -> None:
        bird = Bird("Tweety", 1, "Canary", 15.0, can_fly=True, talkative=False)
        assert bird.name == "Tweety"
        assert bird.species == "Canary"
        assert bird.wingspan_cm == 15.0

    def test_make_sound_quiet(self) -> None:
        bird = Bird("Tweety", 1, "Canary", 15.0, talkative=False)
        assert bird.make_sound() == "Tweet!"

    def test_make_sound_talkative(self) -> None:
        bird = Bird("Polly", 5, "Parrot", 25.0, talkative=True)
        assert "Hello" in bird.make_sound()

    def test_get_species_traits(self) -> None:
        bird = Bird("Tweety", 1, "Canary", 15.0, can_fly=True)
        traits = bird.get_species_traits()
        assert traits["wingspan_cm"] == 15.0
        assert traits["can_fly"] is True

    def test_is_animal(self) -> None:
        bird = Bird("Tweety", 1, "Canary", 15.0)
        assert isinstance(bird, Animal)


class TestRabbit:
    """Tests for Rabbit class."""

    def test_creation(self) -> None:
        rabbit = Rabbit("Hoppy", 2, ear_type="lop", hop_score=9)
        assert rabbit.name == "Hoppy"
        assert rabbit.ear_type == "lop"
        assert rabbit.hop_score == 9

    def test_species(self) -> None:
        rabbit = Rabbit("Hoppy", 2)
        assert rabbit.species == "rabbit"

    def test_make_sound(self) -> None:
        rabbit = Rabbit("Hoppy", 2)
        assert rabbit.make_sound() == "Squeak!"

    def test_get_species_traits(self) -> None:
        rabbit = Rabbit("Hoppy", 2, litter_trained=True)
        traits = rabbit.get_species_traits()
        assert traits["litter_trained"] is True

    def test_is_animal(self) -> None:
        rabbit = Rabbit("Hoppy", 2)
        assert isinstance(rabbit, Animal)


class TestAnimalPolymorphism:
    """Tests demonstrating polymorphic behavior across animal types."""

    def test_polymorphic_sounds(self) -> None:
        animals = [
            Dog("Buddy", 3, "Golden"),
            Cat("Whiskers", 2),
            Bird("Tweety", 1, "Canary", 15.0),
            Rabbit("Hoppy", 2),
        ]
        sounds = [a.make_sound() for a in animals]
        assert sounds == ["Woof!", "Meow!", "Tweet!", "Squeak!"]

    def test_polymorphic_care_instructions(self) -> None:
        animals = [Dog("Buddy", 3, "Golden"), Cat("Whiskers", 2)]
        instructions = [a.get_care_instructions() for a in animals]
        assert all(len(inst) > 0 for inst in instructions)

    def test_all_animals_have_medical_records(self) -> None:
        animals = [Dog("Buddy", 3, "Golden"), Cat("Whiskers", 2)]
        for animal in animals:
            animal.add_medical_note("checkup", "Healthy", "Dr. Smith")
            assert len(animal.get_medical_history()) == 1


# =============================================================================
# Staff Polymorphism Tests
# =============================================================================

class TestStaffBase:
    """Tests for StaffMember abstract base class."""

    def test_cannot_instantiate_base(self) -> None:
        with pytest.raises(TypeError):
            StaffMember("Test", "555-0000")

    def test_auto_id_generation(self) -> None:
        vet1 = Veterinarian("Dr. A", "555-1", "Small", "V001")
        vet2 = Veterinarian("Dr. B", "555-2", "Large", "V002")
        assert vet1.staff_id != vet2.staff_id


class TestVeterinarian:
    """Tests for Veterinarian class."""

    def test_creation(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small Animals", "VET123")
        assert vet.name == "Dr. Smith"
        assert vet.specialization == "Small Animals"
        assert vet.license_number == "VET123"

    def test_role(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        assert vet.role == "veterinarian"

    def test_perform_duties(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        result = vet.perform_duties()
        assert "examining" in result or "veterinary duties" in result

    def test_perform_duties_with_context(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        result = vet.perform_duties({"animal_name": "Buddy"})
        assert "Buddy" in result

    def test_can_handle_medical_tasks(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        assert vet.can_handle_task("medical") is True
        assert vet.can_handle_task("surgery") is True
        assert vet.can_handle_task("cleaning") is False

    def test_examine_animal(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        result = vet.examine_animal("Buddy")
        assert "examines" in result
        assert "Buddy" in result

    def test_prescribe_treatment(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        result = vet.prescribe_treatment("Buddy", "antibiotics")
        assert "prescribes" in result
        assert "antibiotics" in result

    def test_is_staff(self) -> None:
        vet = Veterinarian("Dr. Smith", "555-0100", "Small", "VET123")
        assert isinstance(vet, StaffMember)


class TestCaretaker:
    """Tests for Caretaker class."""

    def test_creation(self) -> None:
        caretaker = Caretaker("John", "555-0200", shift="morning")
        assert caretaker.name == "John"
        assert caretaker.shift == "morning"

    def test_role(self) -> None:
        caretaker = Caretaker("John", "555-0200")
        assert caretaker.role == "caretaker"

    def test_perform_duties(self) -> None:
        caretaker = Caretaker("John", "555-0200", shift="day")
        result = caretaker.perform_duties()
        assert "caring" in result
        assert "day" in result

    def test_can_handle_care_tasks(self) -> None:
        caretaker = Caretaker("John", "555-0200")
        assert caretaker.can_handle_task("feeding") is True
        assert caretaker.can_handle_task("cleaning") is True
        assert caretaker.can_handle_task("medical") is False

    def test_assign_to_animal(self) -> None:
        caretaker = Caretaker("John", "555-0200")
        caretaker.assign_to_animal("A0001")
        assert "A0001" in caretaker.get_assigned_animals()

    def test_get_assigned_animals(self) -> None:
        caretaker = Caretaker("John", "555-0200")
        caretaker.assign_to_animal("A0001")
        caretaker.assign_to_animal("A0002")
        animals = caretaker.get_assigned_animals()
        assert len(animals) == 2


class TestAdoptionCoordinator:
    """Tests for AdoptionCoordinator class."""

    def test_creation(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        assert coord.name == "Jane"

    def test_role(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        assert coord.role == "adoption_coordinator"

    def test_perform_duties(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        result = coord.perform_duties()
        assert "coordinating" in result

    def test_can_handle_adoption_tasks(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        assert coord.can_handle_task("adoption") is True
        assert coord.can_handle_task("screening") is True
        assert coord.can_handle_task("medical") is False

    def test_process_application(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        result = coord.process_application("John Smith")
        assert "processed" in result
        assert coord.get_applications_processed() == 1

    def test_multiple_applications(self) -> None:
        coord = AdoptionCoordinator("Jane", "555-0300")
        for i in range(5):
            coord.process_application(f"Applicant {i}")
        assert coord.get_applications_processed() == 5


class TestStaffPolymorphism:
    """Tests demonstrating polymorphic staff behavior."""

    def test_polymorphic_perform_duties(self) -> None:
        staff = [
            Veterinarian("Dr. Smith", "555-1", "Small", "V001"),
            Caretaker("John", "555-2"),
            AdoptionCoordinator("Jane", "555-3"),
        ]
        results = [s.perform_duties() for s in staff]
        assert all(len(r) > 0 for r in results)

    def test_polymorphic_role_property(self) -> None:
        staff = [
            Veterinarian("Dr. Smith", "555-1", "Small", "V001"),
            Caretaker("John", "555-2"),
            AdoptionCoordinator("Jane", "555-3"),
        ]
        roles = [s.role for s in staff]
        assert "veterinarian" in roles
        assert "caretaker" in roles
        assert "adoption_coordinator" in roles


# =============================================================================
# Enclosure Composition Tests
# =============================================================================

class TestEnclosure:
    """Tests for Enclosure composition class."""

    def test_creation(self) -> None:
        enc = Enclosure("Kennel A", 10, "dog", outdoor_access=True)
        assert enc.name == "Kennel A"
        assert enc.capacity == 10
        assert enc.enclosure_type == "dog"

    def test_auto_id_generation(self) -> None:
        enc1 = Enclosure("A", 5)
        enc2 = Enclosure("B", 5)
        assert enc1.enclosure_id != enc2.enclosure_id

    def test_add_animal(self) -> None:
        enc = Enclosure("Kennel A", 10, "dog")
        dog = Dog("Buddy", 3, "Golden")
        result = enc.add_animal(dog)
        assert result["success"] is True
        assert enc.get_occupancy() == 1

    def test_add_animal_at_capacity(self) -> None:
        enc = Enclosure("Small", 1, "general")
        enc.add_animal(Dog("Dog1", 3, "Golden"))
        result = enc.add_animal(Dog("Dog2", 2, "Beagle"))
        assert result["success"] is False

    def test_add_incompatible_animal(self) -> None:
        enc = Enclosure("Aviary", 5, "aviary")
        dog = Dog("Buddy", 3, "Golden")
        result = enc.add_animal(dog)
        assert result["success"] is False

    def test_remove_animal(self) -> None:
        enc = Enclosure("Kennel A", 10)
        dog = Dog("Buddy", 3, "Golden")
        enc.add_animal(dog)
        result = enc.remove_animal(dog.animal_id)
        assert result["success"] is True
        assert enc.get_occupancy() == 0

    def test_remove_nonexistent_animal(self) -> None:
        enc = Enclosure("Kennel A", 10)
        result = enc.remove_animal("NONEXISTENT")
        assert result["success"] is False

    def test_has_animal(self) -> None:
        enc = Enclosure("Kennel A", 10)
        dog = Dog("Buddy", 3, "Golden")
        enc.add_animal(dog)
        assert enc.has_animal(dog.animal_id) is True
        assert enc.has_animal("OTHER") is False

    def test_has_space(self) -> None:
        enc = Enclosure("Small", 2)
        assert enc.has_space() is True
        enc.add_animal(Dog("Dog1", 3, "Golden"))
        assert enc.has_space() is True
        enc.add_animal(Dog("Dog2", 2, "Beagle"))
        assert enc.has_space() is False

    def test_clean(self) -> None:
        enc = Enclosure("Kennel A", 10)
        result = enc.clean()
        assert "cleaned" in result
        assert enc.get_cleanliness() == "clean"

    def test_needs_cleaning_after_adding(self) -> None:
        enc = Enclosure("Kennel A", 10)
        assert enc.get_cleanliness() == "clean"
        enc.add_animal(Dog("Buddy", 3, "Golden"))
        assert enc.needs_cleaning() is True

    def test_get_animals_by_species(self) -> None:
        enc = Enclosure("Mixed", 10, "general")
        enc.add_animal(Dog("Buddy", 3, "Golden"))
        enc.add_animal(Cat("Whiskers", 2))
        enc.add_animal(Dog("Rex", 5, "Shepherd"))
        dogs = enc.get_animals_by_species("dog")
        assert len(dogs) == 2

    def test_get_status(self) -> None:
        enc = Enclosure("Kennel A", 10, "dog")
        enc.add_animal(Dog("Buddy", 3, "Golden"))
        status = enc.get_status()
        assert status["name"] == "Kennel A"
        assert status["occupancy"] == 1
        assert status["capacity"] == 10


# =============================================================================
# Adoption Workflow Tests
# =============================================================================

class TestAdoptionStatus:
    """Tests for AdoptionStatus enum."""

    def test_status_values(self) -> None:
        assert AdoptionStatus.PENDING.name == "PENDING"
        assert AdoptionStatus.APPROVED.name == "APPROVED"
        assert AdoptionStatus.COMPLETED.name == "COMPLETED"


class TestAdoptionApplication:
    """Tests for AdoptionApplication class."""

    def test_creation(self) -> None:
        app = AdoptionApplication("John", "john@email.com", "A0001")
        assert app.applicant_name == "John"
        assert app.status == AdoptionStatus.PENDING

    def test_auto_id_generation(self) -> None:
        app1 = AdoptionApplication("John", "j@e.com", "A0001")
        app2 = AdoptionApplication("Jane", "ja@e.com", "A0002")
        assert app1.application_id != app2.application_id

    def test_submit(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        result = app.submit()
        assert "submitted" in result

    def test_review(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        app.submit()
        result = app.review("S0001")
        assert app.status == AdoptionStatus.UNDER_REVIEW
        assert "review" in result

    def test_approve(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        result = app.approve("S0001", "Good home")
        assert app.status == AdoptionStatus.APPROVED
        assert "approved" in result

    def test_reject(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        result = app.reject("Insufficient space")
        assert app.status == AdoptionStatus.REJECTED
        assert "rejected" in result

    def test_complete(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        app.approve("S0001")
        result = app.complete()
        assert app.status == AdoptionStatus.COMPLETED
        assert "completed" in result

    def test_cannot_complete_without_approval(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        result = app.complete()
        assert app.status != AdoptionStatus.COMPLETED

    def test_cancel(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        result = app.cancel("Changed mind")
        assert app.status == AdoptionStatus.CANCELLED

    def test_get_timeline(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        app.submit()
        app.review("S0001")
        timeline = app.get_timeline()
        assert len(timeline) >= 3  # created, submitted, reviewed


class TestAdoptionRecord:
    """Tests for AdoptionRecord class."""

    def test_creation(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        app.approve("S0001")
        app.complete()
        record = AdoptionRecord(app, 150.0)
        assert record.final_fee == 150.0

    def test_follow_up_notes(self) -> None:
        app = AdoptionApplication("John", "j@e.com", "A0001")
        app.approve("S0001")
        app.complete()
        record = AdoptionRecord(app, 150.0)
        record.add_follow_up_note("Animal doing well")
        assert len(record.get_follow_up_notes()) == 1


class TestAdoptionManager:
    """Tests for AdoptionManager class."""

    def test_creation(self) -> None:
        manager = AdoptionManager()
        assert manager.get_statistics()["total_applications"] == 0

    def test_submit_application(self) -> None:
        manager = AdoptionManager()
        app = manager.submit_application("John", "j@e.com", "A0001")
        assert app is not None
        assert app.applicant_name == "John"

    def test_get_application(self) -> None:
        manager = AdoptionManager()
        app = manager.submit_application("John", "j@e.com", "A0001")
        retrieved = manager.get_application(app.application_id)
        assert retrieved == app

    def test_get_applications_by_status(self) -> None:
        manager = AdoptionManager()
        manager.submit_application("John", "j@e.com", "A0001")
        pending = manager.get_applications_by_status(AdoptionStatus.PENDING)
        assert len(pending) >= 1

    def test_get_applications_for_animal(self) -> None:
        manager = AdoptionManager()
        manager.submit_application("John", "j@e.com", "A0001")
        manager.submit_application("Jane", "ja@e.com", "A0001")
        apps = manager.get_applications_for_animal("A0001")
        assert len(apps) == 2

    def test_create_record(self) -> None:
        manager = AdoptionManager()
        app = manager.submit_application("John", "j@e.com", "A0001")
        app.approve("S0001")
        app.complete()
        record = manager.create_record(app, 150.0)
        assert record.final_fee == 150.0

    def test_get_statistics(self) -> None:
        manager = AdoptionManager()
        manager.submit_application("John", "j@e.com", "A0001")
        stats = manager.get_statistics()
        assert stats["total_applications"] >= 1
        assert "by_status" in stats


# =============================================================================
# Shelter Integration Tests
# =============================================================================

class TestShelter:
    """Integration tests for Shelter class."""

    def test_creation(self) -> None:
        shelter = Shelter("Happy Tails", "123 Main St")
        assert shelter.name == "Happy Tails"

    def test_add_enclosure(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        result = shelter.add_enclosure(enc)
        assert "Added enclosure" in result

    def test_hire_staff(self) -> None:
        shelter = Shelter("Test")
        vet = Veterinarian("Dr. Smith", "555-1", "Small", "V001")
        result = shelter.hire_staff(vet)
        assert "Hired" in result

    def test_intake_animal(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        result = shelter.intake_animal(dog, enc.enclosure_id)
        assert result["success"] is True

    def test_intake_animal_auto_assign(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("General", 10, "general")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        result = shelter.intake_animal(dog)
        assert result["success"] is True
        assert "enclosure_id" in result

    def test_get_animal(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        retrieved = shelter.get_animal(dog.animal_id)
        assert retrieved == dog

    def test_get_all_animals(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("General", 10, "general")
        shelter.add_enclosure(enc)
        shelter.intake_animal(Dog("Buddy", 3, "Golden"))
        shelter.intake_animal(Cat("Whiskers", 2))
        assert len(shelter.get_all_animals()) == 2

    def test_get_animals_by_species(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("General", 10, "general")
        shelter.add_enclosure(enc)
        shelter.intake_animal(Dog("Buddy", 3, "Golden"))
        shelter.intake_animal(Dog("Rex", 5, "Shepherd"))
        shelter.intake_animal(Cat("Whiskers", 2))
        dogs = shelter.get_animals_by_species("dog")
        assert len(dogs) == 2

    def test_get_available_animals(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("General", 10, "general")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog)
        available = shelter.get_available_animals()
        assert len(available) == 1

    def test_update_animal_health(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        vet = Veterinarian("Dr. Smith", "555-1", "Small", "V001")
        shelter.hire_staff(vet)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        
        result = shelter.update_animal_health(
            dog.animal_id, "sick", vet.staff_id, "Has cold"
        )
        assert result["success"] is True
        assert dog.health_status == "sick"

    def test_assign_staff_to_animal(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        caretaker = Caretaker("John", "555-2")
        shelter.hire_staff(caretaker)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        
        result = shelter.assign_staff_to_animal(caretaker.staff_id, dog.animal_id)
        assert result["success"] is True

    def test_get_staff_for_animal(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        caretaker = Caretaker("John", "555-2")
        shelter.hire_staff(caretaker)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        shelter.assign_staff_to_animal(caretaker.staff_id, dog.animal_id)
        
        staff = shelter.get_staff_for_animal(dog.animal_id)
        assert len(staff) == 1

    def test_clean_enclosure(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        caretaker = Caretaker("John", "555-2")
        shelter.hire_staff(caretaker)
        
        result = shelter.clean_enclosure(enc.enclosure_id, caretaker.staff_id)
        assert result["success"] is True

    def test_submit_adoption_application(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        
        app = shelter.submit_adoption_application("John", dog.animal_id, "j@e.com")
        assert app.applicant_name == "John"

    def test_process_adoption_application_approve(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        coord = AdoptionCoordinator("Jane", "555-3")
        shelter.hire_staff(coord)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        app = shelter.submit_adoption_application("John", dog.animal_id, "j@e.com")
        
        result = shelter.process_adoption_application(
            app.application_id, coord.staff_id, "approve", "Good home"
        )
        assert result["success"] is True
        assert app.status == AdoptionStatus.APPROVED

    def test_complete_adoption(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        coord = AdoptionCoordinator("Jane", "555-3")
        shelter.hire_staff(coord)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        app = shelter.submit_adoption_application("John", dog.animal_id, "j@e.com")
        shelter.process_adoption_application(
            app.application_id, coord.staff_id, "approve"
        )
        
        record = shelter.complete_adoption(app.application_id, 150.0)
        assert record.final_fee == 150.0
        assert dog.is_adoptable is False

    def test_get_shelter_statistics(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("General", 10, "general")
        shelter.add_enclosure(enc)
        shelter.intake_animal(Dog("Buddy", 3, "Golden"))
        shelter.hire_staff(Veterinarian("Dr. Smith", "555-1", "Small", "V001"))
        
        stats = shelter.get_shelter_statistics()
        assert stats["shelter_name"] == "Test"
        assert stats["total_animals"] == 1
        assert stats["total_staff"] == 1

    def test_generate_daily_report(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        
        report = shelter.generate_daily_report()
        assert report["shelter"] == "Test"
        assert "enclosures" in report

    def test_perform_staff_duties(self) -> None:
        shelter = Shelter("Test")
        vet = Veterinarian("Dr. Smith", "555-1", "Small", "V001")
        shelter.hire_staff(vet)
        
        result = shelter.perform_staff_duties(vet.staff_id)
        assert "examining" in result or "veterinary duties" in result

    def test_make_animal_sound(self) -> None:
        shelter = Shelter("Test")
        enc = Enclosure("Kennel A", 10, "dog")
        shelter.add_enclosure(enc)
        dog = Dog("Buddy", 3, "Golden")
        shelter.intake_animal(dog, enc.enclosure_id)
        
        sound = shelter.make_animal_sound(dog.animal_id)
        assert sound == "Woof!"


class TestShelterEndToEnd:
    """End-to-end workflow tests."""

    def test_full_adoption_workflow(self) -> None:
        # Setup shelter
        shelter = Shelter("Happy Tails")
        
        # Add enclosure
        kennel = Enclosure("Main Kennel", 20, "general")
        shelter.add_enclosure(kennel)
        
        # Hire staff
        vet = Veterinarian("Dr. Smith", "555-VET", "General", "V001")
        caretaker = Caretaker("John", "555-CARE", "day")
        coordinator = AdoptionCoordinator("Jane", "555-ADOPT")
        shelter.hire_staff(vet)
        shelter.hire_staff(caretaker)
        shelter.hire_staff(coordinator)
        
        # Intake animal
        dog = Dog("Buddy", 3, "Golden Retriever", training_level=8)
        shelter.intake_animal(dog)
        
        # Assign caretaker
        shelter.assign_staff_to_animal(caretaker.staff_id, dog.animal_id)
        
        # Vet check
        shelter.update_animal_health(
            dog.animal_id, "healthy", vet.staff_id, "Clear bill of health"
        )
        
        # Submit adoption
        app = shelter.submit_adoption_application(
            "John Smith", dog.animal_id, "john@email.com"
        )
        
        # Process application
        shelter.process_adoption_application(
            app.application_id, coordinator.staff_id, "approve", "Great match!"
        )
        
        # Complete adoption
        record = shelter.complete_adoption(app.application_id, 150.0)
        
        # Verify
        assert app.status == AdoptionStatus.COMPLETED
        assert record.final_fee == 150.0
        assert dog.is_adoptable is False
        
        # Check stats
        stats = shelter.get_shelter_statistics()
        assert stats["adoption_stats"]["total_completed"] >= 1

    def test_polymorphic_operations(self) -> None:
        shelter = Shelter("Test")
        
        # Add various animals
        enc = Enclosure("General", 20, "general")
        shelter.add_enclosure(enc)
        
        animals = [
            Dog("Buddy", 3, "Golden"),
            Cat("Whiskers", 2),
            Bird("Tweety", 1, "Canary", 15.0),
            Rabbit("Hoppy", 2),
        ]
        
        for animal in animals:
            shelter.intake_animal(animal)
        
        # Get all sounds polymorphically
        sounds = []
        for animal in shelter.get_all_animals():
            sounds.append(shelter.make_animal_sound(animal.animal_id))
        
        assert "Woof!" in sounds
        assert "Meow!" in sounds
        assert "Tweet!" in sounds
        assert "Squeak!" in sounds


# =============================================================================
# Count Tests
# =============================================================================

def test_total_test_count() -> None:
    """Verify we have at least 80 tests defined."""
    import inspect
    test_count = 0
    for name, obj in globals().items():
        if inspect.isclass(obj) and name.startswith("Test"):
            for method_name in dir(obj):
                if method_name.startswith("test_"):
                    test_count += 1
    assert test_count >= 80, f"Expected at least 80 tests, found {test_count}"
