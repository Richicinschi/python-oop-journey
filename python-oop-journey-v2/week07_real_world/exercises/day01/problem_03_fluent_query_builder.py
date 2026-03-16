"""Problem 03: Fluent Query Builder

Topic: API Design with Classes - Fluent Interface
Difficulty: Medium

Implement a fluent query builder that allows chaining methods
to construct database-like queries in a readable, intuitive way.

HINTS AND DEBUGGING:

HINT 1 (Conceptual): 
A fluent interface (method chaining) requires each method to return 
the object itself (self) so the next method can be called on it.
Think: builder.where("x").where("y") means where() must return builder.

HINT 2 (Structural):
- Use a dataclass to store query state (table, columns, conditions, etc.)
- Each method modifies state and returns self
- build() validates and returns the Query object
- to_sql() generates the SQL string from the Query state

HINT 3 (Edge Cases):
- Multiple select() calls should accumulate columns, not replace
- Multiple where() calls should accumulate conditions with AND
- order_by direction must be "ASC" or "DESC" (case-insensitive)
- Limit and offset cannot be negative
- Calling build() without from_table() should raise ValueError

DEBUGGING - Common Fluent Interface Mistakes:

1. Forgetting to return self:
   # WRONG - returns None implicitly
   def where(self, condition): 
       self.conditions.append(condition)
   
   # RIGHT - returns self for chaining
   def where(self, condition):
       self.conditions.append(condition)
       return self

2. Not storing state between calls:
   # WRONG - creates new Query each time
   def __init__(self): self._query = Query()
   def select(self, cols): return Query(cols=cols)  # Loses previous state!
   
   # RIGHT - modify existing state
   def select(self, *cols): 
       self._query.columns.extend(cols)
       return self

3. Not validating in build():
   # Missing validation leads to confusing SQL errors
   # Always validate required fields before building

4. Case sensitivity issues:
   # User might pass "asc", "Asc", or "ASC"
   # Normalize with direction.upper() before checking
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self


@dataclass
class Query:
    """Represents a constructed query.
    
    Attributes:
        table: Table name to query
        columns: Columns to select (empty means all)
        conditions: WHERE clause conditions
        orderings: ORDER BY clauses
        limit_value: Maximum results to return
        offset_value: Number of results to skip
    """
    table: str = ""
    columns: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    orderings: list[tuple[str, str]] = field(default_factory=list)
    limit_value: int | None = None
    offset_value: int | None = None


class QueryBuilder:
    """Fluent query builder for constructing SQL-like queries.
    
    Usage:
        query = (QueryBuilder()
            .select("id", "name", "email")
            .from_table("users")
            .where("active = true")
            .where("age >= 18")
            .order_by("name", "ASC")
            .limit(10)
            .build())
    """
    
    def __init__(self) -> None:
        """Initialize a new query builder."""
        raise NotImplementedError("Implement QueryBuilder.__init__")
    
    def select(self, *columns: str) -> Self:
        """Specify columns to select.
        
        Args:
            *columns: Column names to include
            
        Returns:
            Self for method chaining
            
        Example:
            builder.select("id", "name")
        """
        raise NotImplementedError("Implement QueryBuilder.select")
    
    def from_table(self, table: str) -> Self:
        """Specify the table to query.
        
        Args:
            table: Table name
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.from_table")
    
    def where(self, condition: str) -> Self:
        """Add a WHERE condition.
        
        Multiple conditions are combined with AND.
        
        Args:
            condition: Condition string (e.g., "age > 18")
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.where")
    
    def order_by(self, column: str, direction: str = "ASC") -> Self:
        """Add an ORDER BY clause.
        
        Args:
            column: Column to sort by
            direction: Sort direction ("ASC" or "DESC")
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If direction is not "ASC" or "DESC"
        """
        raise NotImplementedError("Implement QueryBuilder.order_by")
    
    def limit(self, n: int) -> Self:
        """Set the LIMIT.
        
        Args:
            n: Maximum number of results
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If n is negative
        """
        raise NotImplementedError("Implement QueryBuilder.limit")
    
    def offset(self, n: int) -> Self:
        """Set the OFFSET.
        
        Args:
            n: Number of results to skip
            
        Returns:
            Self for method chaining
            
        Raises:
            ValueError: If n is negative
        """
        raise NotImplementedError("Implement QueryBuilder.offset")
    
    def build(self) -> Query:
        """Build and return the Query object.
        
        Returns:
            Query object representing the constructed query
            
        Raises:
            ValueError: If no table has been specified
        """
        raise NotImplementedError("Implement QueryBuilder.build")
    
    def to_sql(self) -> str:
        """Generate SQL string from the query.
        
        Returns:
            SQL SELECT statement string
            
        Format:
            SELECT col1, col2 FROM table WHERE condition1 AND condition2
            ORDER BY col ASC LIMIT n OFFSET m
        """
        raise NotImplementedError("Implement QueryBuilder.to_sql")


class FilteredQueryBuilder(QueryBuilder):
    """Extended query builder with OR WHERE support.
    
    Adds the ability to build queries with OR conditions
    using a more specialized syntax.
    """
    
    def __init__(self) -> None:
        """Initialize with empty OR condition groups."""
        raise NotImplementedError("Implement FilteredQueryBuilder.__init__")
    
    def or_where(self, *conditions: str) -> Self:
        """Add an OR group of conditions.
        
        All conditions in an or_where group are combined with OR.
        Multiple or_where calls create separate OR groups.
        
        Args:
            *conditions: Conditions to OR together
            
        Returns:
            Self for method chaining
            
        Example:
            builder.where("active = true").or_where("role = admin", "role = moderator")
            # Results in: WHERE active = true AND (role = admin OR role = moderator)
        """
        raise NotImplementedError("Implement FilteredQueryBuilder.or_where")
