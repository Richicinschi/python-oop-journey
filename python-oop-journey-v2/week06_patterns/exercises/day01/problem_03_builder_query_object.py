"""Problem 03: Builder Query Object

Topic: Builder Pattern
Difficulty: Medium

Implement the Builder pattern to construct SQL queries step by step.
The QueryBuilder should allow method chaining to build complex queries.
"""

from __future__ import annotations

from typing import Self, Any


class Query:
    """Product class representing a SQL query.
    
    This is the complex object that the builder constructs.
    """
    
    def __init__(self) -> None:
        self.select_columns: list[str] = []
        self.from_table: str = ""
        self.where_conditions: list[str] = []
        self.order_by: str = ""
        self.limit_value: int | None = None
    
    def __str__(self) -> str:
        """Build and return the SQL query string.
        
        Returns:
            A properly formatted SQL query string
            Format: "SELECT col1, col2 FROM table WHERE cond1 AND cond2 ORDER BY col LIMIT n"
        """
        raise NotImplementedError("Implement Query.__str__")


class QueryBuilder:
    """Builder class for constructing Query objects.
    
    Supports method chaining for fluent interface.
    """
    
    def __init__(self) -> None:
        """Initialize with a new Query instance."""
        raise NotImplementedError("Implement QueryBuilder.__init__")
    
    def select(self, *columns: str) -> Self:
        """Add SELECT columns.
        
        Args:
            *columns: Column names to select
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.select")
    
    def from_table(self, table: str) -> Self:
        """Set the FROM table.
        
        Args:
            table: Table name
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.from_table")
    
    def where(self, condition: str) -> Self:
        """Add a WHERE condition.
        
        Multiple conditions should be combined with AND.
        
        Args:
            condition: WHERE clause condition
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.where")
    
    def order_by(self, column: str, direction: str = "ASC") -> Self:
        """Set ORDER BY clause.
        
        Args:
            column: Column to order by
            direction: Sort direction (ASC or DESC)
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.order_by")
    
    def limit(self, count: int) -> Self:
        """Set LIMIT clause.
        
        Args:
            count: Maximum number of rows
            
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.limit")
    
    def build(self) -> Query:
        """Build and return the Query object.
        
        Returns:
            The constructed Query instance
        """
        raise NotImplementedError("Implement QueryBuilder.build")
    
    def reset(self) -> Self:
        """Reset the builder to start a new query.
        
        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Implement QueryBuilder.reset")


class SQLQueryDirector:
    """Director class that knows common query patterns.
    
    The director provides convenience methods for building
    specific types of queries using the builder.
    """
    
    def __init__(self, builder: QueryBuilder) -> None:
        """Initialize with a QueryBuilder.
        
        Args:
            builder: The builder to use for construction
        """
        raise NotImplementedError("Implement SQLQueryDirector.__init__")
    
    def build_select_all(self, table: str) -> Query:
        """Build a SELECT * query.
        
        Args:
            table: Table name
            
        Returns:
            Query selecting all columns from table
        """
        raise NotImplementedError("Implement SQLQueryDirector.build_select_all")
    
    def build_select_by_id(self, table: str, id_column: str, id_value: str) -> Query:
        """Build a SELECT * WHERE id = value query.
        
        Args:
            table: Table name
            id_column: Name of the ID column
            id_value: Value to match
            
        Returns:
            Query selecting by ID
        """
        raise NotImplementedError("Implement SQLQueryDirector.build_select_by_id")
    
    def build_paginated(self, table: str, columns: list[str], page: int, page_size: int) -> Query:
        """Build a paginated query.
        
        Args:
            table: Table name
            columns: Columns to select
            page: Page number (1-based)
            page_size: Number of items per page
            
        Returns:
            Query with LIMIT and OFFSET
        """
        raise NotImplementedError("Implement SQLQueryDirector.build_paginated")
