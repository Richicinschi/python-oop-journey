"""Reference solution for Problem 03: Builder Query Object."""

from __future__ import annotations

from typing import Self


class Query:
    """Product class representing a SQL query."""
    
    def __init__(self) -> None:
        self.select_columns: list[str] = []
        self.from_table: str = ""
        self.where_conditions: list[str] = []
        self.order_by: str = ""
        self.limit_value: int | None = None
    
    def __str__(self) -> str:
        """Build and return the SQL query string."""
        parts: list[str] = []
        
        # SELECT clause
        if self.select_columns:
            parts.append(f"SELECT {', '.join(self.select_columns)}")
        else:
            parts.append("SELECT *")
        
        # FROM clause
        if self.from_table:
            parts.append(f"FROM {self.from_table}")
        
        # WHERE clause
        if self.where_conditions:
            parts.append(f"WHERE {' AND '.join(self.where_conditions)}")
        
        # ORDER BY clause
        if self.order_by:
            parts.append(f"ORDER BY {self.order_by}")
        
        # LIMIT clause
        if self.limit_value is not None:
            parts.append(f"LIMIT {self.limit_value}")
        
        return " ".join(parts)


class QueryBuilder:
    """Builder class for constructing Query objects."""
    
    def __init__(self) -> None:
        """Initialize with a new Query instance."""
        self._query = Query()
    
    def select(self, *columns: str) -> Self:
        """Add SELECT columns."""
        self._query.select_columns.extend(columns)
        return self
    
    def from_table(self, table: str) -> Self:
        """Set the FROM table."""
        self._query.from_table = table
        return self
    
    def where(self, condition: str) -> Self:
        """Add a WHERE condition."""
        self._query.where_conditions.append(condition)
        return self
    
    def order_by(self, column: str, direction: str = "ASC") -> Self:
        """Set ORDER BY clause."""
        self._query.order_by = f"{column} {direction}"
        return self
    
    def limit(self, count: int) -> Self:
        """Set LIMIT clause."""
        self._query.limit_value = count
        return self
    
    def build(self) -> Query:
        """Build and return the Query object."""
        return self._query
    
    def reset(self) -> Self:
        """Reset the builder to start a new query."""
        self._query = Query()
        return self


class SQLQueryDirector:
    """Director class that knows common query patterns."""
    
    def __init__(self, builder: QueryBuilder) -> None:
        """Initialize with a QueryBuilder."""
        self._builder = builder
    
    def build_select_all(self, table: str) -> Query:
        """Build a SELECT * query."""
        return (self._builder
            .reset()
            .from_table(table)
            .build())
    
    def build_select_by_id(self, table: str, id_column: str, id_value: str) -> Query:
        """Build a SELECT * WHERE id = value query."""
        return (self._builder
            .reset()
            .from_table(table)
            .where(f"{id_column} = {id_value}")
            .build())
    
    def build_paginated(self, table: str, columns: list[str], page: int, page_size: int) -> Query:
        """Build a paginated query."""
        offset = (page - 1) * page_size
        return (self._builder
            .reset()
            .select(*columns)
            .from_table(table)
            .limit(page_size)
            .build())
