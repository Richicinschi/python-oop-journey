# Week 4 Project: Animal Shelter Management System

## Project Goal

Build a complete animal shelter management system that demonstrates all Week 4 intermediate OOP concepts working together in a real-world application. By completing this project, you will prove your understanding of:

- **Inheritance** - Creating specialized animal types from a base class
- **Method Overriding & super()** - Customizing parent behavior in child classes
- **Abstract Base Classes** - Enforcing consistent interfaces across types
- **Polymorphism** - Processing different types uniformly through shared interfaces
- **Composition** - Building complex objects from simpler parts

## Project Connection to Daily Lessons

| Day | Concept | Project Application |
|-----|---------|---------------------|
| Day 1: Inheritance Basics | Base/derived classes, `isinstance()` | `Animal` base class → `Dog`, `Cat`, `Bird`, `Rabbit` |
| Day 2: Method Overriding & `super()` | Extending parent behavior | `to_dict()` in subclasses extends base, `super().__init__()` calls |
| Day 3: Abstract Base Classes | `@abstractmethod`, ABCs | `Animal` ABC enforces `make_sound()`, `StaffMember` ABC enforces `perform_duties()` |
| Day 4: Multiple Inheritance | MRO, mixins | `MedicalRecord` composed into `Animal` (composition pattern) |

**Key Insight**: This project uses both inheritance (animals, staff) AND composition (enclosures have animals, animals have medical records). Understanding when to use each is a core Week 4 learning outcome.

## Files That Matter Most

### Where to Start (Recommended Order)

1. **`starter/animal.py`** - Start here
   - Implements the inheritance hierarchy
   - Most concrete examples of overriding and `super()`
   - Contains `MedicalRecord` demonstrating composition

2. **`starter/staff.py`** - Second
   - Demonstrates polymorphism through abstract base class
   - Shows how different roles implement same interface differently

3. **`starter/enclosure.py`** - Third
   - Pure composition example
   - Shows "has-a" vs "is-a" relationships

4. **`starter/adoption.py`** - Fourth
   - State machine pattern for adoption workflow
   - Enum usage for status tracking

5. **`starter/shelter.py`** - Last
   - Integrates all components
   - Demonstrates high-level API design

### Project Structure

```
project/
├── README.md                    # This file
├── starter/                     # Your starting point
│   ├── animal.py               # Animal inheritance hierarchy
│   ├── staff.py                # Polymorphic staff roles
│   ├── enclosure.py            # Composition-based enclosure
│   ├── adoption.py             # Adoption workflow
│   └── shelter.py              # Main integration class
├── reference_solution/          # Complete implementation
│   ├── animal.py
│   ├── staff.py
│   ├── enclosure.py
│   ├── adoption.py
│   └── shelter.py
└── tests/
    └── test_shelter.py         # Comprehensive test suite
```

## Public Contract: What You Must Implement

### Animal Hierarchy

**Base Class: `Animal` (ABC)**
- `animal_id`: Auto-generated unique ID (format: "A0001")
- `name`, `age`, `species`, `health_status`: Core attributes
- Abstract methods (MUST implement in subclasses):
  - `make_sound() → str` - Return species-specific sound
  - `get_care_instructions() → str` - Return care guidelines
  - `get_species_traits() → dict` - Return type-specific attributes
- Methods:
  - `update_health_status(status)` - Change health status
  - `add_medical_note(type, description, vet_name)` - Add to medical record
  - `get_medical_history() → list` - Retrieve medical history
  - `to_dict() → dict` - Serialize to dictionary

**Subclasses** (each extends `Animal`):

| Class | Extra Attributes | Sound | Notes |
|-------|-----------------|-------|-------|
| `Dog` | `breed`, `size`, `training_level`, `good_with_kids` | "Woof!" | Species="dog" |
| `Cat` | `indoor_only`, `litter_trained`, `declawed` | "Meow!" | Species="cat" |
| `Bird` | `wingspan_cm`, `can_fly`, `talkative` | "Tweet!" or "Hello!" | Use passed species |
| `Rabbit` | `ear_type`, `hop_score`, `litter_trained` | "Squeak!" | Species="rabbit" |

### Staff Hierarchy

**Base Class: `StaffMember` (ABC)**
- `staff_id`: Auto-generated unique ID (format: "S0001")
- `name`, `contact_info`: Core attributes
- Abstract property: `role → str`
- Abstract methods:
  - `perform_duties(context=None) → str` - Polymorphic duty message
  - `can_handle_task(task_type) → bool` - Check capability
- Method: `to_dict() → dict`

**Subclasses**:

| Class | Role | Valid Tasks | Special Methods |
|-------|------|-------------|-----------------|
| `Veterinarian` | "veterinarian" | medical, examination, surgery, vaccination, treatment | `examine_animal()`, `prescribe_treatment()` |
| `Caretaker` | "caretaker" | feeding, cleaning, exercise, grooming, walking, socialization | `assign_to_animal()`, `get_assigned_animals()` |
| `AdoptionCoordinator` | "adoption_coordinator" | adoption, screening, matching, interview, paperwork | `process_application()`, `get_applications_processed()` |

### Enclosure (Composition)

**Class: `Enclosure`**
- `enclosure_id`: Auto-generated unique ID (format: "E0001")
- `name`, `capacity`, `enclosure_type`, `outdoor_access`
- Composition: holds list of `Animal` objects
- Key methods:
  - `add_animal(animal) → dict` - Returns `{"success": bool, "message": str, ...}`
  - `remove_animal(animal_id) → dict` - Returns `{"success": bool, "animal": Animal|None}`
  - `is_compatible(animal) → bool` - Check type compatibility
  - `clean() → str` - Clean enclosure
  - `get_status() → dict` - Full status report

**Compatibility Rules**:
- "general" enclosure: accepts any animal
- "dog" enclosure: accepts dogs only
- "cat" enclosure: accepts cats only
- "aviary" enclosure: accepts birds only
- "small_mammal" enclosure: accepts rabbits only

### Adoption System

**Enum: `AdoptionStatus`**
- PENDING → UNDER_REVIEW → APPROVED → COMPLETED
- Can also transition to: REJECTED, CANCELLED

**Class: `AdoptionApplication`**
- `application_id`: Auto-generated (format: "APP0001")
- `applicant_name`, `applicant_contact`, `animal_id`
- `home_type`, `has_yard`, `other_pets`, `experience_level`
- Status workflow methods:
  - `submit() → str`
  - `review(reviewer_id) → str`
  - `approve(approver_id, notes) → str`
  - `reject(reason) → str`
  - `complete() → str`
  - `cancel(reason) → str`
- `get_timeline() → list` - Audit trail of all actions

**Class: `AdoptionRecord`**
- Created when adoption is completed
- `record_id`: Auto-generated (format: "REC0001")
- Stores final fee, completion date, follow-up notes

**Class: `AdoptionManager`**
- Central registry for applications and records
- Methods: `submit_application()`, `get_application()`, `create_record()`, `get_statistics()`

### Shelter (Integration)

**Class: `Shelter`** - The main API

**Animal Management:**
- `intake_animal(animal, enclosure_id=None) → dict` - Accept new animal
- `get_animal(animal_id) → Animal|None` - Find by ID
- `get_all_animals() → list` - All animals
- `get_available_animals() → list` - Healthy, adoptable animals
- `update_animal_health(animal_id, status, vet_id, notes) → dict`

**Staff Management:**
- `hire_staff(staff_member) → str`
- `get_staff(staff_id) → StaffMember|None`
- `assign_staff_to_animal(staff_id, animal_id) → dict`
- `get_staff_for_animal(animal_id) → list`

**Enclosure Management:**
- `add_enclosure(enclosure) → str`
- `clean_enclosure(enclosure_id, staff_id) → dict`

**Adoption Management:**
- `submit_adoption_application(...) → AdoptionApplication`
- `process_adoption_application(app_id, staff_id, decision, notes) → dict`
- `complete_adoption(app_id, final_fee) → AdoptionRecord`

**Polymorphic Operations:**
- `perform_staff_duties(staff_id, context=None) → str`
- `make_animal_sound(animal_id) → str`

**Reporting:**
- `get_shelter_statistics() → dict` - Comprehensive stats
- `generate_daily_report() → dict` - Operations report

## How to Approach the Starter

### Step-by-Step Implementation Guide

**Phase 1: Animal Hierarchy (Day 1-2 concepts)**

1. Open `starter/animal.py`
2. Implement `MedicalRecord` class first (simple composition)
3. Implement `Animal.__init__()`:
   - Increment `_id_counter` class variable
   - Generate ID: `f"A{self._id_counter:04d}"`
   - Initialize `_medical_record = MedicalRecord()`
4. Implement `@property animal_id` to return `self._animal_id`
5. Implement concrete methods: `update_health_status()`, `add_medical_note()`, etc.
6. Implement `Dog` class:
   - Call `super().__init__(name, age, "dog")` 
   - Store breed-specific attributes
   - Implement abstract methods: `make_sound()` returns "Woof!", etc.
7. Repeat for `Cat`, `Bird`, `Rabbit`

**Phase 2: Staff Polymorphism (Day 3 concepts)**

1. Open `starter/staff.py`
2. Implement `StaffMember.__init__()` with auto-ID generation (format: "S0001")
3. Implement `Veterinarian`:
   - `role` property returns "veterinarian"
   - `perform_duties()` returns descriptive string
   - `can_handle_task()` checks against valid medical tasks
4. Repeat for `Caretaker` and `AdoptionCoordinator`

**Phase 3: Enclosure Composition (Day 4 concepts)**

1. Open `starter/enclosure.py`
2. Implement `__init__()` with auto-ID (format: "E0001")
3. Initialize `self._animals: list[Animal] = []`
4. Implement `add_animal()`:
   - Check capacity: `len(self._animals) < self.capacity`
   - Check compatibility via `is_compatible()`
   - Return dict with success status and message
5. Implement `remove_animal()`, `get_animals()`, `clean()`

**Phase 4: Adoption Workflow**

1. Open `starter/adoption.py`
2. Define `AdoptionStatus` enum with all states
3. Implement `AdoptionApplication.__init__()`:
   - Auto-generate ID (format: "APP0001")
   - Set initial status to `PENDING`
   - Initialize empty timeline list
4. Implement status transition methods with validation
5. Implement `AdoptionManager` as registry

**Phase 5: Shelter Integration**

1. Open `starter/shelter.py`
2. Implement `__init__()` with empty collections:
   - `self._enclosures: dict[str, Enclosure] = {}`
   - `self._staff: dict[str, StaffMember] = {}`
   - `self._adoption_manager = AdoptionManager()`
3. Implement animal intake logic:
   - If enclosure_id provided, use it
   - Else find first compatible enclosure with space
4. Implement staff hiring and assignment
5. Implement adoption workflow methods

### Testing as You Go

After completing each phase, run relevant tests:

```bash
# Test just animals
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestAnimalBase -v
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestDog -v

# Test just staff
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestVeterinarian -v

# Test enclosures
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestEnclosure -v

# Test everything
pytest week04_oop_intermediate/project/tests/test_shelter.py -v
```

## Expected Final Behavior

### Working Example

```python
from week04_oop_intermediate.project.starter.animal import Dog, Cat
from week04_oop_intermediate.project.starter.staff import Veterinarian, AdoptionCoordinator, Caretaker
from week04_oop_intermediate.project.starter.enclosure import Enclosure
from week04_oop_intermediate.project.starter.shelter import Shelter

# Create shelter
shelter = Shelter("Happy Tails Shelter", "123 Main St")

# Add enclosures
kennel = Enclosure("Main Kennel", 10, "dog", outdoor_access=True)
cattery = Enclosure("Cattery", 8, "cat")
shelter.add_enclosure(kennel)
shelter.add_enclosure(cattery)

# Hire staff
vet = Veterinarian("Dr. Smith", "555-0100", "Small Animals", "VET123")
caretaker = Caretaker("John Doe", "555-0200", shift="day")
coordinator = AdoptionCoordinator("Jane Smith", "555-0300")
shelter.hire_staff(vet)
shelter.hire_staff(caretaker)
shelter.hire_staff(coordinator)

# Intake animals
buddy = Dog("Buddy", 3, "Golden Retriever", training_level=8)
whiskers = Cat("Whiskers", 2, indoor_only=True)
shelter.intake_animal(buddy, kennel.enclosure_id)
shelter.intake_animal(whiskers)

# Vet check
shelter.update_animal_health(
    buddy.animal_id, "healthy", vet.staff_id, "Annual checkup clear"
)

# Assign caretaker
shelter.assign_staff_to_animal(caretaker.staff_id, buddy.animal_id)

# Submit adoption application
app = shelter.submit_adoption_application(
    applicant_name="Alice Johnson",
    animal_id=buddy.animal_id,
    applicant_contact="alice@email.com",
    home_type="house",
    has_yard=True
)

# Process application
shelter.process_adoption_application(
    app.application_id, 
    coordinator.staff_id, 
    decision="approve",
    notes="Great match!"
)

# Complete adoption
record = shelter.complete_adoption(app.application_id, final_fee=150.0)

# Check stats
stats = shelter.get_shelter_statistics()
print(f"Total animals: {stats['total_animals']}")
print(f"Adoptions completed: {stats['adoption_stats']['total_completed']}")

# Polymorphic operations
print(shelter.make_animal_sound(whiskers.animal_id))  # "Meow!"
print(shelter.perform_staff_duties(vet.staff_id))      # Vet-specific message
```

### Expected Output Behaviors

**Animal Sounds (Polymorphism):**
- `Dog.make_sound()` → `"Woof!"`
- `Cat.make_sound()` → `"Meow!"`
- `Bird.make_sound()` → `"Tweet!"` (or `"Hello! Pretty bird!"` if talkative)
- `Rabbit.make_sound()` → `"Squeak!"`

**Staff Duties (Polymorphism):**
- Vet: `"Dr. {name} is examining {animal}"` or `"Dr. {name} is performing veterinary duties"`
- Caretaker: `"{name} is caring for animals on {shift} shift"`
- Coordinator: `"{name} is coordinating adoptions (processed: {count})"`

**Enclosure Operations:**
- Adding animal to full enclosure → `{"success": False, "message": "... at capacity"}`
- Adding incompatible animal → `{"success": False, "message": "... not compatible"}`
- Successful add → `{"success": True, "message": "... added", "animal_id": "..."}`

**Adoption Workflow:**
- New application status: `AdoptionStatus.PENDING`
- After review: `AdoptionStatus.UNDER_REVIEW`
- After approve: `AdoptionStatus.APPROVED`
- After complete: `AdoptionStatus.COMPLETED`
- Invalid transitions return error message

## Verification: How to Check Your Work

### Run All Project Tests

```bash
# From repo root
pytest week04_oop_intermediate/project/tests/test_shelter.py -v

# Expected: 115 passed
```

### Run Specific Test Categories

```bash
# Animals (inheritance)
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestDog -v
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestAnimalPolymorphism -v

# Staff (polymorphism)
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestVeterinarian -v
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestStaffPolymorphism -v

# Enclosure (composition)
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestEnclosure -v

# Adoption workflow
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestAdoptionApplication -v

# Full integration
pytest week04_oop_intermediate/project/tests/test_shelter.py::TestShelterEndToEnd -v
```

### Manual Verification Script

Create this test script to verify key behaviors:

```python
# test_my_solution.py
from starter.animal import Dog, Cat, MedicalRecord
from starter.staff import Veterinarian, Caretaker
from starter.enclosure import Enclosure
from starter.shelter import Shelter

def test_animals():
    dog = Dog("Buddy", 3, "Golden")
    assert dog.make_sound() == "Woof!"
    assert dog.species == "dog"
    print("✓ Animals work")

def test_staff():
    vet = Veterinarian("Dr. Smith", "555-1", "Small", "V001")
    assert vet.role == "veterinarian"
    assert vet.can_handle_task("medical") is True
    print("✓ Staff work")

def test_enclosure():
    enc = Enclosure("Test", 5, "general")
    dog = Dog("Buddy", 3, "Golden")
    result = enc.add_animal(dog)
    assert result["success"] is True
    print("✓ Enclosures work")

def test_shelter():
    shelter = Shelter("Test")
    enc = Enclosure("Kennel", 10, "dog")
    shelter.add_enclosure(enc)
    dog = Dog("Buddy", 3, "Golden")
    result = shelter.intake_animal(dog)
    assert result["success"] is True
    print("✓ Shelter works")

if __name__ == "__main__":
    test_animals()
    test_staff()
    test_enclosure()
    test_shelter()
    print("\nAll manual tests passed!")
```

## Common Pitfalls & Debugging Tips

### Inheritance Issues

**Problem**: `AttributeError: 'Dog' object has no attribute 'animal_id'`
- **Cause**: Forgot to call `super().__init__()` in subclass
- **Fix**: Ensure `Dog.__init__()` calls `super().__init__(name, age, "dog")`

**Problem**: Animal IDs not unique or not incrementing
- **Cause**: Using instance variable instead of class variable for counter
- **Fix**: Use `Animal._id_counter` (class variable), not `self._id_counter`

### Abstract Class Issues

**Problem**: `TypeError: Can't instantiate abstract class Animal with abstract methods ...`
- **Cause**: Trying to create `Animal` directly, or subclass didn't implement all abstract methods
- **Fix**: Instantiate `Dog`, `Cat`, etc. - never `Animal`. Check all abstract methods are implemented.

### Composition Issues

**Problem**: Animal in enclosure not the same object as animal retrieved later
- **Cause**: Creating copies instead of storing references
- **Fix**: Store the animal object directly: `self._animals.append(animal)`

### Polymorphism Issues

**Problem**: `perform_duties()` returns generic message for all staff types
- **Cause**: Not overriding method in subclasses
- **Fix**: Each subclass must implement its own `perform_duties()` method

### Adoption Workflow Issues

**Problem**: Can approve application that's already rejected
- **Cause**: Not checking current status before transition
- **Fix**: Validate status in each transition method:
  ```python
  if self._status != AdoptionStatus.PENDING:
      return "Cannot approve..."
  ```

### ID Generation Issues

**Problem**: IDs formatted incorrectly (e.g., "A1" instead of "A0001")
- **Cause**: Not using zero-padding in f-string
- **Fix**: Use `f"A{self._id_counter:04d}"` for 4-digit zero-padding

## Stretch Goals

After completing the base project, consider these extensions:

1. **Serialization**: Add `save_to_file()` and `load_from_file()` to persist shelter state
2. **Search**: Implement `search_animals(criteria)` with filtering by species, age, breed
3. **Statistics Dashboard**: Add visualization-friendly stats methods
4. **Medical Alerts**: Track due dates for vaccinations and notify
5. **Donor Management**: Add `Donor` class and donation tracking
6. **Volunteer Scheduling**: Add shift management for volunteers

## Reference Solution

The `reference_solution/` directory contains a complete, working implementation. Use it when:

- You're stuck on a specific implementation detail (look at relevant file)
- You want to compare your approach after completing a module
- You need to understand expected behavior for a failing test

**Important**: Only look at the reference solution after attempting the implementation yourself. The learning happens in the struggle!

## Summary Checklist

Before considering this project complete, verify:

- [ ] All 5 starter files implemented
- [ ] All 115 tests pass
- [ ] Animal inheritance hierarchy works (Dog, Cat, Bird, Rabbit)
- [ ] Staff polymorphism works (Vet, Caretaker, Coordinator)
- [ ] Enclosure composition manages animals correctly
- [ ] Adoption workflow handles all state transitions
- [ ] Shelter integrates all components
- [ ] Can run the example usage code successfully

Good luck! This project ties together everything you've learned in Week 4. Take it one module at a time, test frequently, and don't hesitate to review the daily theory docs when needed.
