"""Reference solution for Problem 03: Animal Kingdom."""

from __future__ import annotations


class Animal:
    """Base class for all animals."""
    
    def __init__(self, name: str, species: str, age: int) -> None:
        self.name = name
        self.species = species
        self.age = age
    
    def speak(self) -> str:
        return "Some generic animal sound"
    
    def move(self) -> str:
        return "moving"
    
    def describe(self) -> str:
        return f"{self.name} ({self.species}), {self.age} years old"
    
    def get_animal_type(self) -> str:
        return "Unknown"


class Mammal(Animal):
    """A mammal is an animal with fur/hair."""
    
    def __init__(self, name: str, species: str, age: int, fur_color: str, is_domesticated: bool) -> None:
        super().__init__(name, species, age)
        self.fur_color = fur_color
        self.is_domesticated = is_domesticated
    
    def speak(self) -> str:
        return "Grunt!"
    
    def move(self) -> str:
        return "walking on four legs"
    
    def get_animal_type(self) -> str:
        return "Mammal"
    
    def nurse(self) -> str:
        return "Nursing young with milk"


class Bird(Animal):
    """A bird is an animal with feathers and wings."""
    
    def __init__(self, name: str, species: str, age: int, wingspan: float, 
                 can_fly: bool, feather_color: str) -> None:
        super().__init__(name, species, age)
        self.wingspan = wingspan
        self.can_fly = can_fly
        self.feather_color = feather_color
    
    def speak(self) -> str:
        return "Chirp!"
    
    def move(self) -> str:
        if self.can_fly:
            return "flying through the air"
        return "walking on two legs"
    
    def get_animal_type(self) -> str:
        return "Bird"
    
    def lay_egg(self) -> str:
        return "Laying an egg"


class Fish(Animal):
    """A fish is an aquatic animal with fins."""
    
    def __init__(self, name: str, species: str, age: int, water_type: str,
                 fin_count: int, max_depth: float) -> None:
        super().__init__(name, species, age)
        self.water_type = water_type
        self.fin_count = fin_count
        self.max_depth = max_depth
    
    def speak(self) -> str:
        return "Blub blub!"
    
    def move(self) -> str:
        return f"swimming with {self.fin_count} fins"
    
    def get_animal_type(self) -> str:
        return "Fish"
    
    def dive(self, depth: float) -> str:
        if depth <= self.max_depth:
            return f"Dived to {depth} meters"
        return f"Cannot dive to {depth}m. Max depth: {self.max_depth}m"
