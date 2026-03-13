/**
 * Sample Projects Data
 * 
 * These projects correspond to the weekly curriculum and provide
 * hands-on practice for each week's concepts.
 */

import { WeeklyProject } from '@/types/project';

export const sampleProjects: WeeklyProject[] = [
  // Week 1: Simple CLI Tool
  {
    slug: 'week-01-cli-calculator',
    title: 'CLI Calculator',
    description: 'Build a command-line calculator that performs basic arithmetic operations. Practice using variables, functions, and user input while creating a useful utility.',
    difficulty: 'Beginner',
    estimatedTime: '2 hours',
    weekSlug: 'week00_getting_started',
    weekNumber: 1,
    starterFiles: [
      {
        id: 'main-py',
        name: 'main.py',
        path: '/main.py',
        content: `"""CLI Calculator

A simple command-line calculator that performs basic arithmetic operations.

Usage:
    python main.py
"""

from __future__ import annotations


def add(a: float, b: float) -> float:
    """Add two numbers."""
    # TODO: Implement this function
    pass


def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    # TODO: Implement this function
    pass


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    # TODO: Implement this function
    pass


def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    # TODO: Implement this function
    # Remember to handle division by zero!
    pass


def main() -> None:
    """Main calculator loop."""
    print("Welcome to CLI Calculator!")
    print("Type 'quit' to exit")
    
    # TODO: Implement the calculator loop
    # Hint: Use input() to get user input


if __name__ == "__main__":
    main()`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'readme-md',
        name: 'README.md',
        path: '/README.md',
        content: `# CLI Calculator Project

## Description
Build a command-line calculator that performs basic arithmetic operations.

## Learning Objectives
- Practice using variables and functions
- Handle user input with input()
- Implement basic error handling
- Create a reusable utility

## Requirements

### Core Features
1. Implement add(), subtract(), multiply(), divide() functions
2. Create a main loop that accepts user input
3. Handle invalid input gracefully
4. Support decimal numbers

### Bonus Features
- Add a help command that shows available operations
- Implement calculation history
- Add more advanced operations (power, square root)

## Example Usage
\`\`\`
$ python main.py
Welcome to CLI Calculator!
Type 'quit' to exit

Enter operation (add/subtract/multiply/divide): add
Enter first number: 5
Enter second number: 3
Result: 8.0

Enter operation: quit
Goodbye!
\`\`\`

## Testing
Run the calculator and verify:
- All four operations work correctly
- Division by zero is handled
- Invalid input shows helpful messages
- The quit command works`,
        language: 'markdown',
        isModified: false,
        lastModified: Date.now(),
      },
    ],
    requirements: [
      'Implement add, subtract, multiply, divide functions',
      'Create interactive calculator loop',
      'Handle invalid input gracefully',
      'Handle division by zero',
    ],
    hints: [
      'Use float() to convert string input to numbers',
      'Use a while loop for the main calculator loop',
      'Try/except blocks help handle invalid input',
    ],
  },

  // Week 4: Data Structures (Library System)
  {
    slug: 'week-04-library-system',
    title: 'Library Management System',
    description: 'Build a library management system using classes and inheritance. Create a system to manage books, patrons, and checkouts.',
    difficulty: 'Intermediate',
    estimatedTime: '3 hours',
    weekSlug: 'week-04-inheritance',
    weekNumber: 4,
    starterFiles: [
      {
        id: 'book-py',
        name: 'book.py',
        path: '/book.py',
        content: `"""Book module for Library Management System."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional


class Book:
    """Base class for library books."""
    
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
        self.due_date: Optional[datetime] = None
    
    def check_out(self, days: int = 14) -> bool:
        """Check out the book."""
        # TODO: Implement check out logic
        pass
    
    def return_book(self) -> None:
        """Return the book."""
        # TODO: Implement return logic
        pass
    
    def is_overdue(self) -> bool:
        """Check if the book is overdue."""
        # TODO: Implement overdue check
        pass
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author}"


class FictionBook(Book):
    """Fiction book with genre."""
    
    def __init__(self, title: str, author: str, isbn: str, genre: str) -> None:
        # TODO: Call parent constructor and add genre
        pass


class NonFictionBook(Book):
    """Non-fiction book with subject."""
    
    def __init__(self, title: str, author: str, isbn: str, subject: str) -> None:
        # TODO: Call parent constructor and add subject
        pass`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'patron-py',
        name: 'patron.py',
        path: '/patron.py',
        content: `"""Patron module for Library Management System."""

from __future__ import annotations
from typing import List
from book import Book


class Patron:
    """Library patron who can check out books."""
    
    def __init__(self, name: str, patron_id: str) -> None:
        self.name = name
        self.patron_id = patron_id
        self.checked_out_books: List[Book] = []
        self.max_books = 5
    
    def check_out_book(self, book: Book) -> bool:
        """Check out a book if under the limit."""
        # TODO: Implement check out logic
        # Check if patron has reached max books
        # Add book to checked_out_books list
        pass
    
    def return_book(self, book: Book) -> bool:
        """Return a book."""
        # TODO: Implement return logic
        pass
    
    def get_overdue_books(self) -> List[Book]:
        """Get list of overdue books."""
        # TODO: Return books where is_overdue() is True
        pass
    
    def __str__(self) -> str:
        return f"{self.name} ({self.patron_id})"`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'library-py',
        name: 'library.py',
        path: '/library.py',
        content: `"""Main Library class that manages books and patrons."""

from __future__ import annotations
from typing import List, Optional, Dict
from book import Book
from patron import Patron


class Library:
    """Manages the collection of books and patrons."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.books: Dict[str, Book] = {}  # ISBN -> Book
        self.patrons: Dict[str, Patron] = {}  # ID -> Patron
    
    def add_book(self, book: Book) -> None:
        """Add a book to the library."""
        # TODO: Add book to books dictionary
        pass
    
    def add_patron(self, patron: Patron) -> None:
        """Add a patron to the library."""
        # TODO: Add patron to patrons dictionary
        pass
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by ISBN."""
        # TODO: Return book or None
        pass
    
    def find_patron(self, patron_id: str) -> Optional[Patron]:
        """Find a patron by ID."""
        # TODO: Return patron or None
        pass
    
    def get_available_books(self) -> List[Book]:
        """Get all books that are not checked out."""
        # TODO: Return list of books where is_checked_out is False
        pass
    
    def get_overdue_books(self) -> List[Book]:
        """Get all overdue books."""
        # TODO: Return list of overdue books
        pass`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'main-py',
        name: 'main.py',
        path: '/main.py',
        content: `"""Main entry point for Library Management System."""

from library import Library
from book import FictionBook, NonFictionBook
from patron import Patron


def main():
    """Run the library system demo."""
    library = Library("City Library")
    
    # TODO: Create some books
    # TODO: Create some patrons
    # TODO: Demonstrate checkouts and returns
    # TODO: Show overdue tracking
    
    print(f"Welcome to {library.name}!")


if __name__ == "__main__":
    main()`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'readme-md',
        name: 'README.md',
        path: '/README.md',
        content: `# Library Management System

## Description
Build a complete library management system using OOP principles including inheritance, encapsulation, and composition.

## Learning Objectives
- Design class hierarchies using inheritance
- Practice encapsulation with private attributes
- Use composition to build complex systems
- Implement real-world business logic

## Architecture

### Book Class Hierarchy
\`\`\`
Book (base class)
├── FictionBook (adds genre)
└── NonFictionBook (adds subject)
\`\`\`

### Key Classes
- **Book**: Base class for all books
- **FictionBook**: Fiction books with genre
- **NonFictionBook**: Non-fiction books with subject  
- **Patron**: Library members who check out books
- **Library**: Manages the collection and operations

## Requirements

### Core Features
1. Create Book base class with common attributes
2. Implement FictionBook and NonFictionBook subclasses
3. Create Patron class with checkout limits
4. Build Library class to manage everything
5. Track due dates and overdue books

### Advanced Features
- Save/load library data to JSON
- Search books by title or author
- Generate overdue reports
- Handle book reservations

## Testing Checklist
- [ ] Can create books and patrons
- [ ] Books can be checked out and returned
- [ ] Checkout limits are enforced
- [ ] Due dates are calculated correctly
- [ ] Overdue detection works
- [ ] Inheritance is used appropriately`,
        language: 'markdown',
        isModified: false,
        lastModified: Date.now(),
      },
    ],
    requirements: [
      'Create Book base class with title, author, ISBN',
      'Implement FictionBook and NonFictionBook subclasses',
      'Create Patron class with checkout limit',
      'Build Library class using composition',
      'Track due dates and overdue status',
    ],
    hints: [
      'Use super().__init__() to call parent constructor',
      'datetime module helps with date calculations',
      'Composition: Library has Books and Patrons (not inherits)',
    ],
  },

  // Week 8: Full OOP System (E-Commerce)
  {
    slug: 'week-08-ecommerce-system',
    title: 'E-Commerce Backend System',
    description: 'Build a complete e-commerce backend with products, shopping cart, orders, and inventory management. Apply all OOP principles in a capstone project.',
    difficulty: 'Expert',
    estimatedTime: '6 hours',
    weekSlug: 'week-08-capstone',
    weekNumber: 8,
    starterFiles: [
      {
        id: 'product-py',
        name: 'product.py',
        path: '/product.py',
        content: `"""Product classes for E-Commerce System."""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from decimal import Decimal


class Product(ABC):
    """Abstract base class for all products."""
    
    def __init__(
        self,
        product_id: str,
        name: str,
        price: Decimal,
        description: str,
        stock_quantity: int
    ) -> None:
        self._product_id = product_id
        self._name = name
        self._price = price
        self._description = description
        self._stock_quantity = stock_quantity
        self._created_at = datetime.now()
    
    @property
    def product_id(self) -> str:
        return self._product_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> Decimal:
        return self._price
    
    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity
    
    @abstractmethod
    def get_category(self) -> str:
        """Return product category."""
        pass
    
    def is_in_stock(self, quantity: int = 1) -> bool:
        """Check if requested quantity is available."""
        return self._stock_quantity >= quantity
    
    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock by quantity."""
        if self.is_in_stock(quantity):
            self._stock_quantity -= quantity
            return True
        return False
    
    def __str__(self) -> str:
        return f"{self._name} (\${self._price})"


class PhysicalProduct(Product):
    """Physical product with weight and dimensions."""
    
    def __init__(
        self,
        product_id: str,
        name: str,
        price: Decimal,
        description: str,
        stock_quantity: int,
        weight_kg: float,
        dimensions: str
    ) -> None:
        super().__init__(product_id, name, price, description, stock_quantity)
        self.weight_kg = weight_kg
        self.dimensions = dimensions
    
    def get_category(self) -> str:
        return "Physical"
    
    def calculate_shipping_cost(self) -> Decimal:
        """Calculate shipping based on weight."""
        # TODO: Implement shipping calculation
        pass


class DigitalProduct(Product):
    """Digital product with download link."""
    
    def __init__(
        self,
        product_id: str,
        name: str,
        price: Decimal,
        description: str,
        stock_quantity: int,
        file_size_mb: float,
        download_url: str
    ) -> None:
        super().__init__(product_id, name, price, description, stock_quantity)
        self.file_size_mb = file_size_mb
        self.download_url = download_url
    
    def get_category(self) -> str:
        return "Digital"
    
    def generate_download_link(self) -> str:
        """Generate temporary download link."""
        # TODO: Implement secure download link generation
        pass`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'cart-py',
        name: 'cart.py',
        path: '/cart.py',
        content: `"""Shopping cart implementation."""

from __future__ import annotations
from typing import Dict, List
from decimal import Decimal
from product import Product


class CartItem:
    """Item in shopping cart."""
    
    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this item."""
        return self.product.price * self.quantity
    
    def __repr__(self) -> str:
        return f"CartItem({self.product.name} x{self.quantity})"


class ShoppingCart:
    """Shopping cart that holds items."""
    
    def __init__(self) -> None:
        self._items: Dict[str, CartItem] = {}
        self._coupon_code: Optional[str] = None
        self._discount_percent: Decimal = Decimal('0')
    
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        """Add product to cart."""
        # TODO: Check stock availability
        # TODO: Add to items dict or update quantity
        pass
    
    def remove_item(self, product_id: str) -> None:
        """Remove item from cart."""
        # TODO: Remove item from cart
        pass
    
    def update_quantity(self, product_id: str, quantity: int) -> bool:
        """Update quantity of item in cart."""
        # TODO: Update quantity if valid
        pass
    
    def get_items(self) -> List[CartItem]:
        """Get all items in cart."""
        return list(self._items.values())
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal before discounts."""
        # TODO: Sum all item subtotals
        pass
    
    def get_total(self) -> Decimal:
        """Calculate total after discounts."""
        # TODO: Apply discount to subtotal
        pass
    
    def apply_coupon(self, code: str, discount_percent: Decimal) -> bool:
        """Apply discount coupon."""
        # TODO: Validate and apply coupon
        pass
    
    def clear(self) -> None:
        """Empty the cart."""
        self._items.clear()
        self._coupon_code = None
        self._discount_percent = Decimal('0')
    
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self._items) == 0`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'order-py',
        name: 'order.py',
        path: '/order.py',
        content: `"""Order processing system."""

from __future__ import annotations
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional
from decimal import Decimal
from product import Product


class OrderStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class OrderItem:
    """Item in an order (snapshot of product at purchase time)."""
    
    def __init__(
        self,
        product_id: str,
        product_name: str,
        unit_price: Decimal,
        quantity: int
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity
    
    def get_subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


class Order:
    """Customer order."""
    
    def __init__(self, order_id: str, customer_email: str) -> None:
        self.order_id = order_id
        self.customer_email = customer_email
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.shipped_at: Optional[datetime] = None
        self._total: Decimal = Decimal('0')
    
    def add_item(self, product: Product, quantity: int) -> bool:
        """Add item to order."""
        # TODO: Check stock and add item
        # TODO: Update order total
        pass
    
    def confirm(self) -> bool:
        """Confirm the order."""
        # TODO: Validate order and change status
        pass
    
    def ship(self) -> None:
        """Mark order as shipped."""
        # TODO: Update status and shipped_at
        pass
    
    def cancel(self) -> bool:
        """Cancel the order if possible."""
        # TODO: Cancel if not already shipped
        pass
    
    @property
    def total(self) -> Decimal:
        """Get order total."""
        return self._total
    
    def __str__(self) -> str:
        return f"Order {self.order_id} ({self.status.name})"`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'inventory-py',
        name: 'inventory.py',
        path: '/inventory.py',
        content: `"""Inventory management system."""

from __future__ import annotations
from typing import Dict, List, Optional
from product import Product


class Inventory:
    """Manages product inventory."""
    
    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}
        self._low_stock_threshold = 10
    
    def add_product(self, product: Product) -> None:
        """Add product to inventory."""
        self._products[product.product_id] = product
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        return self._products.get(product_id)
    
    def remove_product(self, product_id: str) -> bool:
        """Remove product from inventory."""
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False
    
    def get_all_products(self) -> List[Product]:
        """Get all products."""
        return list(self._products.values())
    
    def get_products_in_stock(self) -> List[Product]:
        """Get products with stock > 0."""
        # TODO: Filter products with stock
        pass
    
    def get_low_stock_products(self) -> List[Product]:
        """Get products below threshold."""
        # TODO: Filter products with low stock
        pass
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name."""
        # TODO: Search by name (case-insensitive)
        pass
    
    def restock(self, product_id: str, quantity: int) -> bool:
        """Add stock to a product."""
        # TODO: Increase product stock
        pass`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'main-py',
        name: 'main.py',
        path: '/main.py',
        content: `"""Main E-Commerce System."""

from decimal import Decimal
from inventory import Inventory
from cart import ShoppingCart
from order import Order
from product import PhysicalProduct, DigitalProduct


def main():
    """Run the e-commerce system demo."""
    # TODO: Create inventory
    # TODO: Add products
    # TODO: Create shopping cart
    # TODO: Add items to cart
    # TODO: Create and confirm order
    
    print("E-Commerce System Demo")
    print("=" * 50)


if __name__ == "__main__":
    main()`,
        language: 'python',
        isModified: false,
        lastModified: Date.now(),
      },
      {
        id: 'readme-md',
        name: 'README.md',
        path: '/README.md',
        content: `# E-Commerce Backend System

## Description
Build a complete e-commerce backend system applying all OOP principles: abstraction, encapsulation, inheritance, and polymorphism.

## Architecture

### Class Hierarchy
\`\`\`
Product (abstract)
├── PhysicalProduct (adds weight, dimensions)
└── DigitalProduct (adds download URL)

Supporting Classes:
- ShoppingCart (manages items)
- CartItem (product + quantity)
- Order (purchase record)
- OrderItem (snapshot of purchase)
- Inventory (product management)
\`\`\`

## Key Features

### 1. Product Management
- Abstract Product base class
- Physical and Digital product types
- Stock tracking
- Category-specific behavior

### 2. Shopping Cart
- Add/remove items
- Update quantities
- Apply discount coupons
- Calculate totals

### 3. Order Processing
- Create orders from cart
- Status tracking
- Order confirmation
- Shipping workflow

### 4. Inventory System
- Product catalog
- Stock management
- Low stock alerts
- Search functionality

## Requirements

### Core Functionality
1. Create Product hierarchy with abstract base class
2. Implement ShoppingCart with add/remove/update
3. Build Order system with status tracking
4. Create Inventory management
5. Handle stock validation throughout

### Design Patterns to Apply
- Abstract Factory (for products)
- Observer (for inventory alerts)
- Strategy (for pricing/discounts)

## Testing Scenarios
1. Add products to inventory
2. Add items to cart (respect stock limits)
3. Create and confirm order
4. Verify stock reduced after order
5. Try to order out-of-stock item
6. Apply coupon and verify discount

## Extension Ideas
- Add user authentication
- Implement payment processing
- Add order history
- Create admin dashboard
- Add product reviews`,
        language: 'markdown',
        isModified: false,
        lastModified: Date.now(),
      },
    ],
    requirements: [
      'Create abstract Product base class',
      'Implement PhysicalProduct and DigitalProduct subclasses',
      'Build ShoppingCart with coupon support',
      'Create Order system with status workflow',
      'Implement Inventory management',
      'Apply all four OOP principles throughout',
    ],
    hints: [
      'Use ABC and @abstractmethod for abstract classes',
      'Decimal is better than float for money calculations',
      'Enum helps with status management',
      'Composition connects the system components',
    ],
  },
];

export function getProjectBySlug(slug: string): WeeklyProject | undefined {
  return sampleProjects.find(p => p.slug === slug);
}

export function getProjectsByWeek(weekNumber: number): WeeklyProject[] {
  return sampleProjects.filter(p => p.weekNumber === weekNumber);
}

export function getAllProjects(): WeeklyProject[] {
  return sampleProjects;
}
