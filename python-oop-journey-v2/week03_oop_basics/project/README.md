# Week 3 Project: Basic E-commerce System

## Project Overview

This project is a comprehensive e-commerce system that brings together all the Object-Oriented Programming concepts learned in Week 3:

- **Classes and Objects**: Building the foundational data models
- **Instance/Class/Static Methods**: Different types of methods for different purposes
- **Encapsulation and Properties**: Protecting internal state with validation
- **Magic Methods**: Making objects Pythonic with `__repr__`, `__eq__`, `__len__`, etc.
- **Composition and Aggregation**: Building complex systems from simple parts

## Learning Goals

After completing this project, you will be able to:

1. Design a multi-class system with clear responsibilities
2. Implement proper encapsulation with getters, setters, and validation
3. Use composition to build complex objects from simpler ones
4. Implement magic methods for natural object behavior
5. Create class methods and static methods where appropriate
6. Write testable, decoupled code
7. Apply the Single Responsibility Principle

## Required Features

### Product Management
- Products with name, price, category, and SKU
- Price validation (non-negative)
- SKU-based equality and hashing
- Discount calculation
- Dictionary serialization/deserialization

### User Management
- User accounts with ID, name, and email
- Email format validation
- Shopping cart association (composition)
- Order history tracking
- Total spending calculation

### Shopping Cart
- Add/remove/update items
- Quantity management
- Total calculation
- Discount code support
- Iteration support

### Order Processing
- Order lifecycle (PENDING → CONFIRMED → SHIPPED → DELIVERED)
- Order cancellation (when allowed)
- Immutable order items
- Status transition validation
- Automatic order ID generation

### Inventory Management
- Stock tracking by SKU
- Stock reservation and release
- Low stock alerts
- Stock threshold configuration

## Optional Stretch Features

1. **Product Categories**: Create a Category class with hierarchical categories
2. **Payment Processing**: Add a Payment class with different payment methods
3. **Shipping Calculation**: Add shipping costs based on weight/destination
4. **Wishlist**: Allow users to save items for later
5. **Product Reviews**: Let users rate and review products
6. **Inventory Alerts**: Notify when stock is low
7. **Bulk Operations**: Support bulk stock updates

## File Structure

```
week03_oop_basics/project/
├── README.md              # This file
├── starter/               # Starter code with TODOs
│   ├── __init__.py
│   ├── product.py         # Product class
│   ├── user.py            # User/Customer class
│   ├── cart.py            # ShoppingCart and CartItem classes
│   ├── order.py           # Order, OrderItem, OrderStatus classes
│   └── inventory.py       # Inventory class
├── reference_solution/    # Complete working implementation
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   ├── cart.py
│   ├── order.py
│   └── inventory.py
└── tests/
    ├── __init__.py
    └── test_ecommerce.py  # Comprehensive test suite
```

## Connection to Daily Lessons

This project reinforces all Week 3 concepts:

| Day | Concept | Where You'll Apply It |
|-----|---------|----------------------|
| **Day 1** | Classes and Objects | All five modules - defining classes, `__init__`, instance attributes |
| **Day 2** | Method Types | `Product.from_dict()` (classmethod), `User.validate_email()` (staticmethod), `Inventory.set_low_stock_threshold()` (classmethod) |
| **Day 3** | Encapsulation & Properties | Every class uses private attributes (`_name`, `_price`) with `@property` decorators and validation in setters |
| **Day 4** | Magic Methods | `__repr__` in all classes, `__eq__` and `__hash__` in Product, `__len__` and `__iter__` in ShoppingCart |
| **Day 5** | Composition & Aggregation | User-has-Cart (composition), Cart-has-Items (composition), Order-captures-CartItems (snapshot) |
| **Day 6** | Class Design | Single Responsibility Principle - each class has one clear job |

---

## How to Work Through This Project

### Recommended Order

Follow this order - it builds complexity gradually and matches the week's learning progression:

### Step 1: Start with Product (Days 1-3)
The `Product` class is the simplest and has no dependencies.

**Open:** `starter/product.py`

**You'll practice:**
- **Day 1**: Class definition, `__init__`, instance attributes
- **Day 3**: Private attributes with property decorators, validation in setters
- **Day 4**: `__repr__`, `__eq__`, `__hash__` for value-based equality
- **Day 2**: `from_dict()` class method for alternative constructor

**Key methods to implement:**
- `__init__` with validation
- Property getters/setters for name, price, category
- Read-only property for SKU
- `apply_discount()` method
- `to_dict()` and `from_dict()` for serialization

### Step 2: Implement Cart and CartItem (Days 4-5)
These classes work together and depend on Product.

**Open:** `starter/cart.py`

**You'll practice:**
- **Day 5**: Composition (Cart contains CartItems)
- **Day 4**: Magic methods (`__len__`, `__iter__`)
- **Day 1**: Collection management with dictionaries
- **Day 3**: Property validation for quantities

**Key methods to implement:**
- `CartItem.__init__` with quantity validation
- `ShoppingCart.add_item()` with increment logic
- `__len__` for unique item count
- `__iter__` for looping over items
- `get_total()` for price calculation

### Step 3: Implement User (Days 2, 3, 5)
User composes ShoppingCart and tracks orders.

**Open:** `starter/user.py`

**You'll practice:**
- **Day 5**: Composition pattern (User has a Cart)
- **Day 2**: Static methods for validation (`validate_email()`)
- **Day 2**: Class methods for configuration (`set_email_whitelist()`)
- **Day 3**: Property validation for email format

**Key methods to implement:**
- `__init__` with email validation
- `cart` property (creates cart on demand)
- `orders` property returning a copy
- Static method `validate_email()`
- Class methods for whitelist management

### Step 4: Implement Order System (Days 2, 4, 5, 6)
Orders capture cart state at checkout.

**Open:** `starter/order.py`

**You'll practice:**
- **Day 1**: Enum for order status (OrderStatus)
- **Day 6**: State machine pattern (status transitions)
- **Day 2**: Factory methods (`from_cart()` classmethod)
- **Day 5**: Immutability (OrderItem captures product data snapshot)
- **Day 4**: Class-level counter for ID generation

**Key methods to implement:**
- `OrderStatus.__str__`
- `Order.update_status()` with transition validation
- `Order.cancel()` and `can_cancel()`
- `Order.generate_order_id()` class method
- `Order.from_cart()` factory method

### Step 5: Implement Inventory (Days 2, 3)
Inventory manages product availability.

**Open:** `starter/inventory.py`

**You'll practice:**
- **Day 2**: Class attributes (`LOW_STOCK_THRESHOLD`) and methods
- **Day 3**: Threshold management with validation
- **Day 1**: Dictionary operations for stock tracking

**Key methods to implement:**
- `stock_product()` and `reserve()`
- `get_low_stock_items()` using threshold
- Class methods `set_low_stock_threshold()` and `get_low_stock_threshold()`

---

## Project Workflow Tips

### For Each File:

1. **Read the docstrings** - They explain what each method should do
2. **Look at the TODO comments** - They guide implementation order
3. **Check the example usage** below to understand expected behavior
4. **Run the tests** for that specific class after implementing

### Testing Your Implementation:

```bash
# Test specific class (update import in test file first)
pytest week03_oop_basics/project/tests/test_ecommerce.py::TestProduct -v
pytest week03_oop_basics/project/tests/test_ecommerce.py::TestShoppingCart -v
pytest week03_oop_basics/project/tests/test_ecommerce.py::TestUser -v
pytest week03_oop_basics/project/tests/test_ecommerce.py::TestOrder -v
pytest week03_oop_basics/project/tests/test_ecommerce.py::TestInventory -v
```

## How to Run

### Run the Tests

From the repository root:

```bash
# Run all project tests
pytest week03_oop_basics/project/tests/

# Run with verbose output
pytest week03_oop_basics/project/tests/ -v

# Run with coverage
pytest week03_oop_basics/project/tests/ --cov=week03_oop_basics.project.reference_solution
```

### Run Against Your Implementation

To test your starter implementation instead of the reference solution:

1. Update the imports in `test_ecommerce.py` to import from `starter` instead of `reference_solution`
2. Run the tests as above

## Class Relationships

```
┌─────────────┐     has many     ┌──────────────┐
│    User     │─────────────────>│    Order     │
└──────┬──────┘                  └──────────────┘
       │                               │
       │ has one                  has many
       ▼                               ▼
┌─────────────┐                  ┌──────────────┐
│ShoppingCart │                  │  OrderItem   │
└──────┬──────┘                  └──────────────┘
       │                               │
       │ has many                  captures
       ▼                               │
┌─────────────┐                  ┌──────────────┐
│  CartItem   │                  │Product (data)│
└──────┬──────┘                  └──────────────┘
       │
       │ references
       ▼
┌─────────────┐
│   Product   │<─────────────────────────┐
└─────────────┘                          │
                                         │
                                ┌────────▼─────┐
                                │  Inventory   │
                                │ (tracks stock│
                                │   by SKU)    │
                                └──────────────┘
```

## Example Usage

```python
from week03_oop_basics.project.reference_solution import (
    Product, User, ShoppingCart, Order, Inventory
)

# Create products
laptop = Product("Laptop", 999.99, "Electronics", "TECH-001")
mouse = Product("Wireless Mouse", 29.99, "Electronics", "TECH-002")

# Create user
user = User("U001", "Alice Smith", "alice@example.com")

# Add items to cart
user.cart.add_item(laptop, 1)
user.cart.add_item(mouse, 2)

# Check cart total
print(f"Cart total: ${user.cart.get_total()}")  # $1059.97

# Manage inventory
inventory = Inventory()
inventory.stock_product("TECH-001", 100)
inventory.stock_product("TECH-002", 50)

# Check out (reserve inventory)
for item in user.cart:
    inventory.reserve(item.product.sku, item.quantity)

# Create order
order = Order.from_cart(user.user_id, user.cart.get_items())
user.add_order(order)

# Clear cart
user.cart.clear()

# Update order status
order.update_status(OrderStatus.CONFIRMED)
order.update_status(OrderStatus.SHIPPED)
```

## Design Decisions

### Why Composition Over Inheritance?

- **User and Cart**: A User has a Cart, not is a Cart
- **Cart and Items**: A Cart contains Items, separation allows flexible item management
- **Order and OrderItem**: Order captures a snapshot, OrderItem is immutable history

### Why Properties?

- Validation happens on every assignment
- Read-only attributes (SKU, Order ID) prevent accidental modification
- Encapsulation allows internal representation changes

### Why Enums for Status?

- Type safety: can't accidentally set invalid status
- Clear state machine with valid transitions
- Self-documenting code

## Common Pitfalls

1. **Forgetting validation**: Always validate in setters and `__init__`
2. **Returning mutable references**: Return copies of lists/dicts to prevent external modification
3. **Circular imports**: Use TYPE_CHECKING for type hints that would cause circular imports
4. **State leakage**: OrderItem should copy product data, not reference the Product
5. **Missing edge cases**: Empty strings, negative numbers, None values

## Testing Strategy

The test suite covers:

- **Unit tests**: Each class in isolation
- **Integration tests**: Class interactions
- **Edge cases**: Invalid inputs, boundary conditions
- **State transitions**: Order status changes
- **Error cases**: Validation failures, invalid operations

Total tests: 60+

## Success Criteria

Your implementation is complete when:

- [ ] All 60+ tests pass
- [ ] No `NotImplementedError` remains
- [ ] Proper validation on all setters
- [ ] Clean separation of concerns
- [ ] Clear docstrings and type hints
- [ ] No circular import issues

## Next Steps

After completing this project:

1. Review the reference solution to compare approaches
2. Consider implementing the stretch features
3. Add more comprehensive error handling
4. Create a simple CLI to interact with the system
5. Move on to Week 4: OOP Intermediate (Inheritance)
