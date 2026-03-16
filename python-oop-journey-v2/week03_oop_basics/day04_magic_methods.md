# Day 4: Magic Methods (Dunder Methods)

## Learning Objectives

By the end of this day, you will be able to:

- Implement `__repr__` and `__str__` for proper object representation
- Use `__eq__`, `__lt__`, and other comparison methods for custom ordering
- Overload arithmetic operators with `__add__`, `__sub__`, `__mul__`, etc.
- Create container-like objects with `__len__`, `__getitem__`, `__iter__`, and `__contains__`
- Understand when to use each magic method and their semantics
- Apply magic methods to create intuitive, Pythonic class interfaces

---

## Key Concepts

### What Are Magic Methods?

Magic methods (also called dunder methods for "double underscore") allow your classes to interact with Python's built-in operations and syntax. They are the foundation of Python's data model.

```python
class Point:
    """A 2D point with magic methods for intuitive behavior."""
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """Official string representation for debugging."""
        return f"Point({self.x!r}, {self.y!r})"
    
    def __str__(self) -> str:
        """Informal string representation for users."""
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other: object) -> bool:
        """Check if two points are equal."""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other: Point) -> Point:
        """Add two points: Point(1, 2) + Point(3, 4) = Point(4, 6)."""
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)
```

### Object Representation: `__repr__` vs `__str__`

| Method | Purpose | Called By |
|--------|---------|-----------|
| `__repr__` | Unambiguous, for developers | `repr()`, interactive shell |
| `__str__` | Readable, for users | `str()`, `print()` |

**Best Practice**: Always implement `__repr__`. If you only implement one, make it `__repr__`. `__str__` defaults to `__repr__` if not defined.

```python
class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price
    
    def __repr__(self) -> str:
        # Should ideally be valid Python that could recreate the object
        return f"Product(name={self.name!r}, price={self.price!r})"
    
    def __str__(self) -> str:
        # Human-readable
        return f"{self.name}: ${self.price:.2f}"

p = Product("Coffee", 4.50)
print(repr(p))  # Product(name='Coffee', price=4.5)
print(str(p))   # Coffee: $4.50
```

### Comparison Methods

Python provides six comparison methods that correspond to operators:

| Method | Operator | Description |
|--------|----------|-------------|
| `__eq__` | `==` | Equal to |
| `__ne__` | `!=` | Not equal to (usually inferred from `__eq__`) |
| `__lt__` | `<` | Less than |
| `__le__` | `<=` | Less than or equal |
| `__gt__` | `>` | Greater than |
| `__ge__` | `>=` | Greater than or equal |

```python
class Money:
    """Represents an amount of money in cents."""
    
    def __init__(self, dollars: int, cents: int) -> None:
        self.total_cents = dollars * 100 + cents
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.total_cents == other.total_cents
    
    def __lt__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.total_cents < other.total_cents
    
    # With functools.total_ordering, you only need __eq__ and one of __lt__, __le__, __gt__, __ge__

from functools import total_ordering

@total_ordering
class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius
    
    def __lt__(self, other: Temperature) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius
    
    # Now supports: ==, !=, <, <=, >, >= automatically
```

### Arithmetic Operators

Overload operators to work with your custom types:

| Method | Operator | Description |
|--------|----------|-------------|
| `__add__` | `+` | Addition |
| `__sub__` | `-` | Subtraction |
| `__mul__` | `*` | Multiplication |
| `__truediv__` | `/` | Division |
| `__floordiv__` | `//` | Floor division |
| `__mod__` | `%` | Modulo |
| `__pow__` | `**` | Power |

**In-place operators** (mutate the object):

| Method | Operator |
|--------|----------|
| `__iadd__` | `+=` |
| `__isub__` | `-=` |
| `__imul__` | `*=` |

```python
class Vector:
    """A 2D vector supporting arithmetic operations."""
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> Vector:
        # Scalar multiplication: Vector(2, 3) * 2 = Vector(4, 6)
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> Vector:
        # Reverse multiplication: 2 * Vector(2, 3) = Vector(4, 6)
        return self.__mul__(scalar)
    
    def __neg__(self) -> Vector:
        # Unary minus: -Vector(2, 3) = Vector(-2, -3)
        return Vector(-self.x, -self.y)
    
    def __iadd__(self, other: Vector) -> Vector:
        # In-place addition: vec += other_vec
        if not isinstance(other, Vector):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

# Usage
v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)        # Vector(4, 6)
print(v1 * 2)         # Vector(2, 4)
print(2 * v1)         # Vector(2, 4)  - uses __rmul__
print(-v1)            # Vector(-1, -2)
v1 += v2              # In-place addition
```

### Container Protocol

Make your objects behave like collections:

```python
class Playlist:
    """A music playlist supporting container operations."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._songs: list[str] = []
    
    def add_song(self, song: str) -> None:
        self._songs.append(song)
    
    def __len__(self) -> int:
        """Enable len(playlist)."""
        return len(self._songs)
    
    def __getitem__(self, index: int | slice) -> str | list[str]:
        """Enable playlist[0], playlist[1:3]."""
        return self._songs[index]
    
    def __iter__(self) -> Iterator[str]:
        """Enable for song in playlist."""
        return iter(self._songs)
    
    def __contains__(self, song: str) -> bool:
        """Enable 'song' in playlist."""
        return song in self._songs
    
    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, songs={self._songs!r})"

from typing import Iterator

playlist = Playlist("My Favorites")
playlist.add_song("Song A")
playlist.add_song("Song B")
playlist.add_song("Song C")

len(playlist)              # 3
playlist[0]                # 'Song A'
playlist[1:3]              # ['Song B', 'Song C']
"Song B" in playlist       # True
for song in playlist:      # Iterates through all songs
    print(song)
```

### Hashable Objects and `__hash__`

For objects to be used in sets or as dictionary keys, they must be hashable:

```python
class Product:
    """A hashable product for use in sets and as dict keys."""
    
    def __init__(self, sku: str, name: str) -> None:
        self.sku = sku
        self.name = name
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.sku == other.sku
    
    def __hash__(self) -> int:
        """Hash based on immutable identifier."""
        return hash(self.sku)
    
    def __repr__(self) -> str:
        return f"Product(sku={self.sku!r}, name={self.name!r})"

# Now Products can be used in sets
inventory = {Product("ABC123", "Widget"), Product("DEF456", "Gadget")}
product_map = {Product("ABC123", "Widget"): 10}  # As dict key
```

**Critical Rule**: If you define `__eq__`, objects become unhashable by default. You must also define `__hash__`, and equal objects must have equal hashes.

### Truthiness with `__bool__`

Control how your objects evaluate in boolean contexts:

```python
class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[str] = []
    
    def add_item(self, item: str) -> None:
        self._items.append(item)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __bool__(self) -> bool:
        """Enable if cart: ... (True if has items)."""
        return len(self._items) > 0

cart = ShoppingCart()
bool(cart)          # False (empty)
cart.add_item("book")
bool(cart)          # True (has items)
if cart:            # Uses __bool__
    print("Cart has items!")
```

---

## Common Mistakes

### 1. Forgetting to Return `NotImplemented`

```python
# WRONG
class Point:
    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Can only add Point to Point")
        return Point(self.x + other.x, self.y + other.y)

# CORRECT: Return NotImplemented to let Python try the reverse operation
class Point:
    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)
```

### 2. Inconsistent `__eq__` and `__hash__`

```python
# WRONG: Equal objects have different hashes
class Item:
    def __init__(self, name: str):
        self.name = name
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name
    
    def __hash__(self):
        return id(self)  # Different hash for equal objects!

# CORRECT: Equal objects have equal hashes
class Item:
    def __init__(self, name: str):
        self.name = name
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)  # Same hash for equal names
```

### 3. Using Mutable Values in `__hash__`

```python
# WRONG: Hash changes when object mutates (breaks dict/set invariants)
class BadProduct:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    
    def __hash__(self):
        return hash((self.name, self.price))  # price can change!

# CORRECT: Hash only on immutable identifier
class GoodProduct:
    def __init__(self, sku: str, name: str, price: float):
        self._sku = sku  # Immutable identifier
        self.name = name
        self.price = price
    
    @property
    def sku(self) -> str:
        return self._sku
    
    def __hash__(self):
        return hash(self._sku)
    
    def __eq__(self, other):
        return isinstance(other, GoodProduct) and self._sku == other._sku
```

### 4. Not Checking Type in Comparison Methods

```python
# WRONG: Will crash or give wrong results
class Money:
    def __eq__(self, other):
        return self.amount == other.amount  # Crashes if other is None/int

# CORRECT: Check type first
class Money:
    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount
```

### 5. Confusing `__str__` and `__repr__`

```python
# WRONG: __repr__ is for debugging, not users
class Person:
    def __repr__(self):
        return f"Hi, I'm {self.name}!"  # Too informal

# CORRECT: __repr__ should be unambiguous and ideally valid Python
class Person:
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"
    
    def __str__(self):
        return f"Hi, I'm {self.name}!"  # This is for users
```

---

## Connection to Exercises

| Exercise | Magic Methods Practiced |
|----------|------------------------|
| 01. Vector 2D | `__add__`, `__sub__`, `__mul__`, `__repr__` |
| 02. Money | `__add__`, `__sub__`, `__eq__`, `__lt__`, currency handling |
| 03. Product Catalog Item | `__eq__`, `__hash__`, `__repr__` |
| 04. Playlist | `__len__`, `__getitem__`, `__iter__`, `__contains__` |
| 05. Fraction Number | `__add__`, `__mul__`, `__eq__`, `__lt__`, simplify |
| 06. Range Box | `__contains__`, `__iter__`, bounds checking |
| 07. Basket | `__add__`, `__iadd__`, `__len__`, `__iter__`, total |
| 08. Point Comparison | `__eq__`, `__lt__`, `__hash__`, distance |

---

## Weekly Project Connection

The Week 3 project (Basic E-commerce System) uses magic methods extensively:

- **Product equality**: `__eq__` and `__hash__` for cart operations
- **Cart operations**: `__len__`, `__iter__`, `__contains__` for the shopping cart
- **Money handling**: `__add__`, `__sub__` for price calculations
- **Order totals**: `__repr__` for debugging order state
- **Inventory lookup**: `__eq__` and `__hash__` for product identification

Mastering magic methods will make your e-commerce classes intuitive and Pythonic.

---

## Summary

- **Magic methods** enable Python's built-in operators to work with your classes
- **`__repr__`** provides the official string representation (aim for valid Python)
- **`__str__`** provides the user-friendly representation
- **Comparison methods** (`__eq__`, `__lt__`, etc.) define ordering and equality
- **Arithmetic methods** (`__add__`, `__mul__`, etc.) overload math operators
- **Container methods** (`__len__`, `__iter__`, etc.) make objects collection-like
- **`__hash__`** must be consistent with `__eq__` for set/dict usage
- **Return `NotImplemented`** (not raise exceptions) for unsupported operand types
