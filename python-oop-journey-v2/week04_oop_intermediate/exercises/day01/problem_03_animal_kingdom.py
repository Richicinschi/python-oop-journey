"""Problem 03: Animal Kingdom

Topic: Multiple Subclasses with Specific Behaviors
Difficulty: Medium

Create an Animal base class and three animal type subclasses (Mammal, Bird, Fish)
with unique behaviors for each type.
"""

from __future__ import annotations


class Animal:
    """Base class for all animals.
    
    Attributes:
        name: The animal's name
        species: The species name
        age: Age in years
    """
    
    def __init__(self, name: str, species: str, age: int) -> None:
        """Initialize an Animal.
        
        Args:
            name: Animal's name
            species: Species name
            age: Age in years
        """
        raise NotImplementedError("Implement Animal.__init__")
    
    def speak(self) -> str:
        """Return the sound the animal makes.
        
        Returns:
            Generic sound: "Some generic animal sound"
        """
        raise NotImplementedError("Implement Animal.speak")
    
    def move(self) -> str:
        """Return how the animal moves.
        
        Returns:
            Generic movement: "moving"
        """
        raise NotImplementedError("Implement Animal.move")
    
    def describe(self) -> str:
        """Return a description of the animal.
        
        Returns:
            String: "Name (Species), X years old"
        """
        raise NotImplementedError("Implement Animal.describe")
    
    def get_animal_type(self) -> str:
        """Return the type of animal.
        
        Returns:
            "Unknown"
        """
        raise NotImplementedError("Implement Animal.get_animal_type")


class Mammal(Animal):
    """A mammal is an animal with fur/hair and gives live birth.
    
    Additional Attributes:
        fur_color: Color of the mammal's fur/hair
        is_domesticated: Whether the mammal is domesticated
    """
    
    def __init__(self, name: str, species: str, age: int, fur_color: str, is_domesticated: bool) -> None:
        """Initialize a Mammal.
        
        Args:
            name: Mammal's name
            species: Species name
            age: Age in years
            fur_color: Fur/hair color
            is_domesticated: Whether domesticated
        """
        raise NotImplementedError("Implement Mammal.__init__")
    
    def speak(self) -> str:
        """Override: Mammal-specific sound.
        
        Returns:
            "Grunt!"
        """
        raise NotImplementedError("Implement Mammal.speak")
    
    def move(self) -> str:
        """Override: Mammals typically walk or run.
        
        Returns:
            "walking on four legs"
        """
        raise NotImplementedError("Implement Mammal.move")
    
    def get_animal_type(self) -> str:
        """Override: Return animal type.
        
        Returns:
            "Mammal"
        """
        raise NotImplementedError("Implement Mammal.get_animal_type")
    
    def nurse(self) -> str:
        """Mammal-specific behavior.
        
        Returns:
            "Nursing young with milk"
        """
        raise NotImplementedError("Implement Mammal.nurse")


class Bird(Animal):
    """A bird is an animal with feathers and wings.
    
    Additional Attributes:
        wingspan: Wingspan in centimeters
        can_fly: Whether the bird can fly
        feather_color: Primary feather color
    """
    
    def __init__(self, name: str, species: str, age: int, wingspan: float, 
                 can_fly: bool, feather_color: str) -> None:
        """Initialize a Bird.
        
        Args:
            name: Bird's name
            species: Species name
            age: Age in years
            wingspan: Wingspan in cm
            can_fly: Whether bird can fly
            feather_color: Primary feather color
        """
        raise NotImplementedError("Implement Bird.__init__")
    
    def speak(self) -> str:
        """Override: Bird-specific sound.
        
        Returns:
            "Chirp!"
        """
        raise NotImplementedError("Implement Bird.speak")
    
    def move(self) -> str:
        """Override: Birds fly if they can, otherwise walk.
        
        Returns:
            "flying through the air" if can_fly
            "walking on two legs" if not can_fly
        """
        raise NotImplementedError("Implement Bird.move")
    
    def get_animal_type(self) -> str:
        """Override: Return animal type.
        
        Returns:
            "Bird"
        """
        raise NotImplementedError("Implement Bird.get_animal_type")
    
    def lay_egg(self) -> str:
        """Bird-specific behavior.
        
        Returns:
            "Laying an egg"
        """
        raise NotImplementedError("Implement Bird.lay_egg")


class Fish(Animal):
    """A fish is an aquatic animal with fins and gills.
    
    Additional Attributes:
        water_type: "freshwater" or "saltwater"
        fin_count: Number of fins
        max_depth: Maximum diving depth in meters
    """
    
    def __init__(self, name: str, species: str, age: int, water_type: str,
                 fin_count: int, max_depth: float) -> None:
        """Initialize a Fish.
        
        Args:
            name: Fish's name
            species: Species name
            age: Age in years
            water_type: "freshwater" or "saltwater"
            fin_count: Number of fins
            max_depth: Maximum depth in meters
        """
        raise NotImplementedError("Implement Fish.__init__")
    
    def speak(self) -> str:
        """Override: Fish don't really speak.
        
        Returns:
            "Blub blub!"
        """
        raise NotImplementedError("Implement Fish.speak")
    
    def move(self) -> str:
        """Override: Fish swim.
        
        Returns:
            "swimming with X fins"
        """
        raise NotImplementedError("Implement Fish.move")
    
    def get_animal_type(self) -> str:
        """Override: Return animal type.
        
        Returns:
            "Fish"
        """
        raise NotImplementedError("Implement Fish.get_animal_type")
    
    def dive(self, depth: float) -> str:
        """Fish-specific behavior.
        
        Args:
            depth: Depth to dive to
            
        Returns:
            Success message if depth <= max_depth
            Failure message if depth > max_depth
        """
        raise NotImplementedError("Implement Fish.dive")
