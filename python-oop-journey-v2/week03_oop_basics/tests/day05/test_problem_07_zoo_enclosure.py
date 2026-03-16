"""Tests for Problem 07: Zoo Enclosure."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day05.problem_07_zoo_enclosure import (
    Animal,
    Enclosure,
    Zoo,
)


class TestAnimal:
    """Tests for Animal class."""
    
    def test_animal_init(self) -> None:
        """Test animal initialization."""
        animal = Animal("Leo", "Lion", 5)
        assert animal.name == "Leo"
        assert animal.species == "Lion"
        assert animal.age == 5
        assert animal.enclosure_id is None
    
    def test_assign_to_enclosure(self) -> None:
        """Test assigning animal to enclosure."""
        animal = Animal("Leo", "Lion", 5)
        animal.assign_to_enclosure("A1")
        assert animal.enclosure_id == "A1"
    
    def test_remove_from_enclosure(self) -> None:
        """Test removing animal from enclosure."""
        animal = Animal("Leo", "Lion", 5)
        animal.assign_to_enclosure("A1")
        animal.remove_from_enclosure()
        assert animal.enclosure_id is None


class TestEnclosure:
    """Tests for Enclosure class."""
    
    def test_enclosure_init(self) -> None:
        """Test enclosure initialization."""
        enclosure = Enclosure("A1", "Savanna", 5)
        assert enclosure.enclosure_id == "A1"
        assert enclosure.habitat_type == "Savanna"
        assert enclosure.capacity == 5
        assert enclosure.animals == []
    
    def test_add_animal(self) -> None:
        """Test adding animal to enclosure."""
        enclosure = Enclosure("A1", "Savanna", 5)
        animal = Animal("Leo", "Lion", 5)
        result = enclosure.add_animal(animal)
        assert result is True
        assert len(enclosure.animals) == 1
        assert animal.enclosure_id == "A1"
    
    def test_add_animal_over_capacity(self) -> None:
        """Test adding animal when at capacity."""
        enclosure = Enclosure("A1", "Savanna", 1)
        enclosure.add_animal(Animal("Leo", "Lion", 5))
        result = enclosure.add_animal(Animal("Simba", "Lion", 3))
        assert result is False
    
    def test_remove_animal(self) -> None:
        """Test removing animal from enclosure."""
        enclosure = Enclosure("A1", "Savanna", 5)
        animal = Animal("Leo", "Lion", 5)
        enclosure.add_animal(animal)
        result = enclosure.remove_animal("Leo")
        assert result is True
        assert len(enclosure.animals) == 0
        assert animal.enclosure_id is None
    
    def test_remove_animal_not_found(self) -> None:
        """Test removing non-existent animal."""
        enclosure = Enclosure("A1", "Savanna", 5)
        result = enclosure.remove_animal("Unknown")
        assert result is False
    
    def test_get_animal_count(self) -> None:
        """Test getting animal count."""
        enclosure = Enclosure("A1", "Savanna", 5)
        assert enclosure.get_animal_count() == 0
        enclosure.add_animal(Animal("Leo", "Lion", 5))
        assert enclosure.get_animal_count() == 1
    
    def test_has_space(self) -> None:
        """Test checking if enclosure has space."""
        enclosure = Enclosure("A1", "Savanna", 1)
        assert enclosure.has_space() is True
        enclosure.add_animal(Animal("Leo", "Lion", 5))
        assert enclosure.has_space() is False
    
    def test_get_animals(self) -> None:
        """Test getting animals list."""
        enclosure = Enclosure("A1", "Savanna", 5)
        animal = Animal("Leo", "Lion", 5)
        enclosure.add_animal(animal)
        animals = enclosure.get_animals()
        assert len(animals) == 1
        assert animals[0] is animal


class TestZoo:
    """Tests for Zoo class."""
    
    def test_zoo_init(self) -> None:
        """Test zoo initialization."""
        zoo = Zoo("City Zoo")
        assert zoo.name == "City Zoo"
        assert zoo.enclosures == {}
        assert zoo.all_animals == {}
    
    def test_add_enclosure(self) -> None:
        """Test adding enclosure."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        assert "A1" in zoo.enclosures
    
    def test_get_enclosure(self) -> None:
        """Test getting enclosure."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        found = zoo.get_enclosure("A1")
        assert found is enclosure
    
    def test_get_enclosure_not_found(self) -> None:
        """Test getting non-existent enclosure."""
        zoo = Zoo("City Zoo")
        found = zoo.get_enclosure("UNKNOWN")
        assert found is None
    
    def test_add_animal_to_enclosure(self) -> None:
        """Test adding animal to enclosure."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        animal = Animal("Leo", "Lion", 5)
        result = zoo.add_animal_to_enclosure(animal, "A1")
        assert "added" in result.lower()
        assert "Leo" in zoo.all_animals
    
    def test_add_animal_enclosure_not_found(self) -> None:
        """Test adding animal to non-existent enclosure."""
        zoo = Zoo("City Zoo")
        animal = Animal("Leo", "Lion", 5)
        result = zoo.add_animal_to_enclosure(animal, "UNKNOWN")
        assert "not found" in result.lower()
    
    def test_add_animal_enclosure_full(self) -> None:
        """Test adding animal to full enclosure."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 0)
        zoo.add_enclosure(enclosure)
        animal = Animal("Leo", "Lion", 5)
        result = zoo.add_animal_to_enclosure(animal, "A1")
        assert "full" in result.lower()
    
    def test_remove_animal(self) -> None:
        """Test removing animal."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        animal = Animal("Leo", "Lion", 5)
        zoo.add_animal_to_enclosure(animal, "A1")
        result = zoo.remove_animal("Leo")
        assert "removed" in result.lower()
        assert "Leo" not in zoo.all_animals
    
    def test_remove_animal_not_found(self) -> None:
        """Test removing non-existent animal."""
        zoo = Zoo("City Zoo")
        result = zoo.remove_animal("Unknown")
        assert "not found" in result.lower()
    
    def test_get_animals_by_species(self) -> None:
        """Test getting animals by species."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        zoo.add_animal_to_enclosure(Animal("Leo", "Lion", 5), "A1")
        zoo.add_animal_to_enclosure(Animal("Simba", "Lion", 3), "A1")
        zoo.add_animal_to_enclosure(Animal("Dumbo", "Elephant", 8), "A1")
        
        lions = zoo.get_animals_by_species("Lion")
        assert len(lions) == 2
        assert all(a.species == "Lion" for a in lions)
    
    def test_get_total_animal_count(self) -> None:
        """Test getting total animal count."""
        zoo = Zoo("City Zoo")
        enclosure = Enclosure("A1", "Savanna", 5)
        zoo.add_enclosure(enclosure)
        zoo.add_animal_to_enclosure(Animal("Leo", "Lion", 5), "A1")
        zoo.add_animal_to_enclosure(Animal("Dumbo", "Elephant", 8), "A1")
        assert zoo.get_total_animal_count() == 2
    
    def test_get_enclosure_count(self) -> None:
        """Test getting enclosure count."""
        zoo = Zoo("City Zoo")
        assert zoo.get_enclosure_count() == 0
        zoo.add_enclosure(Enclosure("A1", "Savanna", 5))
        assert zoo.get_enclosure_count() == 1
