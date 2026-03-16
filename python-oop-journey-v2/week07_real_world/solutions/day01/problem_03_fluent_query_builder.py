"""Reference solution for Problem 03: Fluent Query Builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self


@dataclass
class Query:
    """Represents a constructed query."""
    
    table: str = ""
    columns: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    orderings: list[tuple[str, str]] = field(default_factory=list)
    limit_value: int | None = None
    offset_value: int | None = None


class QueryBuilder:
    """Fluent query builder for constructing SQL-like queries."""
    
    def __init__(self) -> None:
        """Initialize a new query builder."""
        self._query = Query()
    
    def select(self, *columns: str) -> Self:
        """Specify columns to select."""
        self._query.columns.extend(columns)
        return self
    
    def from_table(self, table: str) -> Self:
        """Specify the table to query."""
        self._query.table = table
        return self
    
    def where(self, condition: str) -> Self:
        """Add a WHERE condition."""
        self._query.conditions.append(condition)
        return self
    
    def order_by(self, column: str, direction: str = "ASC") -> Self:
        """Add an ORDER BY clause."""
        direction_upper = direction.upper()
        if direction_upper not in ("ASC", "DESC"):
            raise ValueError(f"Direction must be 'ASC' or 'DESC', got '{direction}'")
        self._query.orderings.append((column, direction_upper))
        return self
    
    def limit(self, n: int) -> Self:
        """Set the LIMIT."""
        if n < 0:
            raise ValueError(f"Limit cannot be negative, got {n}")
        self._query.limit_value = n
        return self
    
    def offset(self, n: int) -> Self:
        """Set the OFFSET."""
        if n < 0:
            raise ValueError(f"Offset cannot be negative, got {n}")
        self._query.offset_value = n
        return self
    
    def build(self) -> Query:
        """Build and return the Query object."""
        if not self._query.table:
            raise ValueError("No table specified. Call from_table() first.")
        return Query(
            table=self._query.table,
            columns=self._query.columns.copy(),
            conditions=self._query.conditions.copy(),
            orderings=self._query.orderings.copy(),
            limit_value=self._query.limit_value,
            offset_value=self._query.offset_value,
        )
    
    def to_sql(self) -> str:
        """Generate SQL string from the query."""
        query = self.build()
        
        # SELECT clause
        if query.columns:
            columns_str = ", ".join(query.columns)
        else:
            columns_str = "*"
        sql = f"SELECT {columns_str} FROM {query.table}"
        
        # WHERE clause
        if query.conditions:
            sql += " WHERE " + " AND ".join(query.conditions)
        
        # ORDER BY clause
        if query.orderings:
            order_strs = [f"{col} {dir}" for col, dir in query.orderings]
            sql += " ORDER BY " + ", ".join(order_strs)
        
        # LIMIT
        if query.limit_value is not None:
            sql += f" LIMIT {query.limit_value}"
        
        # OFFSET
        if query.offset_value is not None:
            sql += f" OFFSET {query.offset_value}"
        
        return sql


class FilteredQueryBuilder(QueryBuilder):
    """Extended query builder with OR WHERE support."""
    
    def __init__(self) -> None:
        """Initialize with empty OR condition groups."""
        super().__init__()
        self._or_groups: list[list[str]] = []
    
    def or_where(self, *conditions: str) -> Self:
        """Add an OR group of conditions."""
        if conditions:
            self._or_groups.append(list(conditions))
        return self
    
    def to_sql(self) -> str:
        """Generate SQL with OR conditions."""
        # Build base query
        if not self._query.table:
            raise ValueError("No table specified. Call from_table() first.")
        
        # Build WHERE clauses
        where_clauses = self._query.conditions.copy()
        
        # Add OR groups
        for or_group in self._or_groups:
            if or_group:
                or_clause = " OR ".join(or_group)
                if len(or_group) > 1:
                    where_clauses.append(f"({or_clause})")
                else:
                    where_clauses.append(or_clause)
        
        # SELECT clause
        if self._query.columns:
            columns_str = ", ".join(self._query.columns)
        else:
            columns_str = "*"
        sql = f"SELECT {columns_str} FROM {self._query.table}"
        
        # WHERE clause
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        # ORDER BY clause
        if self._query.orderings:
            order_strs = [f"{col} {dir}" for col, dir in self._query.orderings]
            sql += " ORDER BY " + ", ".join(order_strs)
        
        # LIMIT
        if self._query.limit_value is not None:
            sql += f" LIMIT {self._query.limit_value}"
        
        # OFFSET
        if self._query.offset_value is not None:
            sql += f" OFFSET {self._query.offset_value}"
        
        return sql
