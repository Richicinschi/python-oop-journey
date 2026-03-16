"""Tests for Problem 03: Fluent Query Builder."""

from __future__ import annotations

import pytest

from week07_real_world.solutions.day01.problem_03_fluent_query_builder import (
    FilteredQueryBuilder,
    Query,
    QueryBuilder,
)


class TestQuery:
    """Tests for Query dataclass."""
    
    def test_query_defaults(self) -> None:
        """Test Query default values."""
        query = Query()
        assert query.table == ""
        assert query.columns == []
        assert query.conditions == []
        assert query.orderings == []
        assert query.limit_value is None
        assert query.offset_value is None


class TestQueryBuilder:
    """Tests for QueryBuilder."""
    
    def test_simple_select(self) -> None:
        """Test simple SELECT query."""
        builder = QueryBuilder()
        query = builder.from_table("users").build()
        
        assert query.table == "users"
        assert query.columns == []
    
    def test_select_with_columns(self) -> None:
        """Test SELECT with specific columns."""
        builder = QueryBuilder()
        query = builder.select("id", "name", "email").from_table("users").build()
        
        assert query.columns == ["id", "name", "email"]
    
    def test_select_multiple_times(self) -> None:
        """Test that multiple select calls accumulate columns."""
        builder = QueryBuilder()
        query = (builder
            .select("id")
            .select("name")
            .from_table("users")
            .build())
        
        assert query.columns == ["id", "name"]
    
    def test_where_single_condition(self) -> None:
        """Test single WHERE condition."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .where("active = true")
            .build())
        
        assert query.conditions == ["active = true"]
    
    def test_where_multiple_conditions(self) -> None:
        """Test multiple WHERE conditions."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .where("active = true")
            .where("age >= 18")
            .build())
        
        assert query.conditions == ["active = true", "age >= 18"]
    
    def test_order_by_default_direction(self) -> None:
        """Test ORDER BY with default ASC direction."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .order_by("name")
            .build())
        
        assert query.orderings == [("name", "ASC")]
    
    def test_order_by_explicit_direction(self) -> None:
        """Test ORDER BY with explicit direction."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .order_by("created_at", "DESC")
            .build())
        
        assert query.orderings == [("created_at", "DESC")]
    
    def test_order_by_invalid_direction(self) -> None:
        """Test ORDER BY with invalid direction raises error."""
        builder = QueryBuilder()
        with pytest.raises(ValueError, match="Direction must be 'ASC' or 'DESC'"):
            builder.from_table("users").order_by("name", "INVALID")
    
    def test_order_by_case_insensitive(self) -> None:
        """Test ORDER BY direction is case insensitive."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .order_by("name", "desc")
            .build())
        
        assert query.orderings == [("name", "DESC")]
    
    def test_limit(self) -> None:
        """Test LIMIT."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .limit(10)
            .build())
        
        assert query.limit_value == 10
    
    def test_limit_negative_raises(self) -> None:
        """Test negative LIMIT raises error."""
        builder = QueryBuilder()
        with pytest.raises(ValueError, match="Limit cannot be negative"):
            builder.from_table("users").limit(-1)
    
    def test_offset(self) -> None:
        """Test OFFSET."""
        builder = QueryBuilder()
        query = (builder
            .from_table("users")
            .offset(20)
            .build())
        
        assert query.offset_value == 20
    
    def test_offset_negative_raises(self) -> None:
        """Test negative OFFSET raises error."""
        builder = QueryBuilder()
        with pytest.raises(ValueError, match="Offset cannot be negative"):
            builder.from_table("users").offset(-5)
    
    def test_build_without_table_raises(self) -> None:
        """Test building without table raises error."""
        builder = QueryBuilder()
        with pytest.raises(ValueError, match="No table specified"):
            builder.build()
    
    def test_method_chaining(self) -> None:
        """Test fluent interface with method chaining."""
        query = (QueryBuilder()
            .select("id", "name")
            .from_table("users")
            .where("active = true")
            .where("age >= 18")
            .order_by("name", "ASC")
            .limit(10)
            .offset(20)
            .build())
        
        assert query.columns == ["id", "name"]
        assert query.table == "users"
        assert query.conditions == ["active = true", "age >= 18"]
        assert query.orderings == [("name", "ASC")]
        assert query.limit_value == 10
        assert query.offset_value == 20


class TestQueryBuilderToSQL:
    """Tests for QueryBuilder.to_sql()."""
    
    def test_to_sql_simple(self) -> None:
        """Test simple SQL generation."""
        sql = (QueryBuilder()
            .from_table("users")
            .to_sql())
        
        assert sql == "SELECT * FROM users"
    
    def test_to_sql_with_columns(self) -> None:
        """Test SQL with specific columns."""
        sql = (QueryBuilder()
            .select("id", "name")
            .from_table("users")
            .to_sql())
        
        assert sql == "SELECT id, name FROM users"
    
    def test_to_sql_with_where(self) -> None:
        """Test SQL with WHERE clause."""
        sql = (QueryBuilder()
            .from_table("users")
            .where("active = true")
            .to_sql())
        
        assert sql == "SELECT * FROM users WHERE active = true"
    
    def test_to_sql_with_multiple_where(self) -> None:
        """Test SQL with multiple WHERE conditions."""
        sql = (QueryBuilder()
            .from_table("users")
            .where("active = true")
            .where("age >= 18")
            .to_sql())
        
        assert sql == "SELECT * FROM users WHERE active = true AND age >= 18"
    
    def test_to_sql_with_order_by(self) -> None:
        """Test SQL with ORDER BY."""
        sql = (QueryBuilder()
            .from_table("users")
            .order_by("name", "DESC")
            .to_sql())
        
        assert sql == "SELECT * FROM users ORDER BY name DESC"
    
    def test_to_sql_with_multiple_order_by(self) -> None:
        """Test SQL with multiple ORDER BY clauses."""
        sql = (QueryBuilder()
            .from_table("users")
            .order_by("department", "ASC")
            .order_by("name", "ASC")
            .to_sql())
        
        assert sql == "SELECT * FROM users ORDER BY department ASC, name ASC"
    
    def test_to_sql_with_limit(self) -> None:
        """Test SQL with LIMIT."""
        sql = (QueryBuilder()
            .from_table("users")
            .limit(10)
            .to_sql())
        
        assert sql == "SELECT * FROM users LIMIT 10"
    
    def test_to_sql_with_offset(self) -> None:
        """Test SQL with OFFSET."""
        sql = (QueryBuilder()
            .from_table("users")
            .offset(20)
            .to_sql())
        
        assert sql == "SELECT * FROM users OFFSET 20"
    
    def test_to_sql_complete(self) -> None:
        """Test complete SQL generation."""
        sql = (QueryBuilder()
            .select("id", "name", "email")
            .from_table("users")
            .where("active = true")
            .where("age >= 18")
            .order_by("created_at", "DESC")
            .limit(10)
            .offset(20)
            .to_sql())
        
        expected = "SELECT id, name, email FROM users WHERE active = true AND age >= 18 ORDER BY created_at DESC LIMIT 10 OFFSET 20"
        assert sql == expected


class TestFilteredQueryBuilder:
    """Tests for FilteredQueryBuilder with OR support."""
    
    def test_or_where_single_condition(self) -> None:
        """Test OR WHERE with single condition."""
        sql = (FilteredQueryBuilder()
            .from_table("users")
            .where("active = true")
            .or_where("role = admin")
            .to_sql())
        
        assert "WHERE active = true AND role = admin" in sql
    
    def test_or_where_multiple_conditions(self) -> None:
        """Test OR WHERE with multiple conditions in group."""
        sql = (FilteredQueryBuilder()
            .from_table("users")
            .where("active = true")
            .or_where("role = admin", "role = moderator")
            .to_sql())
        
        assert "WHERE active = true AND (role = admin OR role = moderator)" in sql
    
    def test_or_where_multiple_groups(self) -> None:
        """Test multiple OR WHERE groups."""
        sql = (FilteredQueryBuilder()
            .from_table("users")
            .where("active = true")
            .or_where("role = admin", "role = moderator")
            .or_where("department = IT", "department = Engineering")
            .to_sql())
        
        assert "active = true" in sql
        assert "(role = admin OR role = moderator)" in sql
        assert "(department = IT OR department = Engineering)" in sql
    
    def test_filtered_builder_inherits_query_builder(self) -> None:
        """Test that FilteredQueryBuilder inherits from QueryBuilder."""
        assert issubclass(FilteredQueryBuilder, QueryBuilder)
