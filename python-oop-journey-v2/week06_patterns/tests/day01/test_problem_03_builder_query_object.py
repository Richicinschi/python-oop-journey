"""Tests for Problem 03: Builder Query Object."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day01.problem_03_builder_query_object import (
    Query, QueryBuilder, SQLQueryDirector
)


class TestQuery:
    """Tests for the Query product class."""
    
    def test_empty_query_defaults_to_select_all(self) -> None:
        query = Query()
        assert str(query) == "SELECT *"
    
    def test_query_with_columns(self) -> None:
        query = Query()
        query.select_columns = ["name", "email"]
        query.from_table = "users"
        assert str(query) == "SELECT name, email FROM users"
    
    def test_query_with_where(self) -> None:
        query = Query()
        query.select_columns = ["*"]
        query.from_table = "users"
        query.where_conditions = ["age > 18"]
        assert str(query) == "SELECT * FROM users WHERE age > 18"
    
    def test_query_with_multiple_where(self) -> None:
        query = Query()
        query.select_columns = ["*"]
        query.from_table = "users"
        query.where_conditions = ["age > 18", "active = 1"]
        assert str(query) == "SELECT * FROM users WHERE age > 18 AND active = 1"
    
    def test_query_with_order_by(self) -> None:
        query = Query()
        query.select_columns = ["name"]
        query.from_table = "users"
        query.order_by = "name ASC"
        assert str(query) == "SELECT name FROM users ORDER BY name ASC"
    
    def test_query_with_limit(self) -> None:
        query = Query()
        query.from_table = "users"
        query.limit_value = 10
        assert str(query) == "SELECT * FROM users LIMIT 10"
    
    def test_full_query(self) -> None:
        query = Query()
        query.select_columns = ["name", "email"]
        query.from_table = "users"
        query.where_conditions = ["active = 1"]
        query.order_by = "name ASC"
        query.limit_value = 5
        assert str(query) == "SELECT name, email FROM users WHERE active = 1 ORDER BY name ASC LIMIT 5"


class TestQueryBuilder:
    """Tests for the QueryBuilder class."""
    
    def test_init_creates_empty_query(self) -> None:
        builder = QueryBuilder()
        query = builder.build()
        assert isinstance(query, Query)
    
    def test_select_single_column(self) -> None:
        builder = QueryBuilder()
        query = builder.select("name").build()
        assert query.select_columns == ["name"]
    
    def test_select_multiple_columns(self) -> None:
        builder = QueryBuilder()
        query = builder.select("name", "email", "age").build()
        assert query.select_columns == ["name", "email", "age"]
    
    def test_select_chained_calls(self) -> None:
        builder = QueryBuilder()
        query = builder.select("name").select("email").build()
        assert query.select_columns == ["name", "email"]
    
    def test_from_table(self) -> None:
        builder = QueryBuilder()
        query = builder.from_table("users").build()
        assert query.from_table == "users"
    
    def test_where_single(self) -> None:
        builder = QueryBuilder()
        query = builder.where("age > 18").build()
        assert query.where_conditions == ["age > 18"]
    
    def test_where_multiple(self) -> None:
        builder = QueryBuilder()
        query = builder.where("age > 18").where("active = 1").build()
        assert query.where_conditions == ["age > 18", "active = 1"]
    
    def test_order_by_default_direction(self) -> None:
        builder = QueryBuilder()
        query = builder.order_by("name").build()
        assert query.order_by == "name ASC"
    
    def test_order_by_desc(self) -> None:
        builder = QueryBuilder()
        query = builder.order_by("created_at", "DESC").build()
        assert query.order_by == "created_at DESC"
    
    def test_limit(self) -> None:
        builder = QueryBuilder()
        query = builder.limit(10).build()
        assert query.limit_value == 10
    
    def test_method_chaining(self) -> None:
        builder = QueryBuilder()
        query = (builder
            .select("name", "email")
            .from_table("users")
            .where("active = 1")
            .order_by("name")
            .limit(5)
            .build())
        
        assert query.select_columns == ["name", "email"]
        assert query.from_table == "users"
        assert query.where_conditions == ["active = 1"]
        assert query.order_by == "name ASC"
        assert query.limit_value == 5
    
    def test_reset_creates_new_query(self) -> None:
        builder = QueryBuilder()
        query1 = builder.select("name").from_table("users").build()
        query2 = builder.reset().from_table("posts").build()
        
        assert query1.from_table == "users"
        assert query2.from_table == "posts"
        assert query2.select_columns == []
    
    def test_str_after_build(self) -> None:
        builder = QueryBuilder()
        query = (builder
            .select("name", "email")
            .from_table("users")
            .where("active = 1")
            .order_by("name", "DESC")
            .limit(10)
            .build())
        
        expected = "SELECT name, email FROM users WHERE active = 1 ORDER BY name DESC LIMIT 10"
        assert str(query) == expected


class TestSQLQueryDirector:
    """Tests for the SQLQueryDirector class."""
    
    def test_init(self) -> None:
        builder = QueryBuilder()
        director = SQLQueryDirector(builder)
        assert director._builder is builder
    
    def test_build_select_all(self) -> None:
        builder = QueryBuilder()
        director = SQLQueryDirector(builder)
        query = director.build_select_all("users")
        
        assert str(query) == "SELECT * FROM users"
    
    def test_build_select_by_id(self) -> None:
        builder = QueryBuilder()
        director = SQLQueryDirector(builder)
        query = director.build_select_by_id("users", "id", "123")
        
        assert str(query) == "SELECT * FROM users WHERE id = 123"
    
    def test_build_paginated(self) -> None:
        builder = QueryBuilder()
        director = SQLQueryDirector(builder)
        query = director.build_paginated("users", ["name", "email"], page=2, page_size=10)
        
        assert "SELECT name, email FROM users" in str(query)
        assert "LIMIT 10" in str(query)
    
    def test_director_reuses_builder(self) -> None:
        builder = QueryBuilder()
        director = SQLQueryDirector(builder)
        
        query1 = director.build_select_all("users")
        query2 = director.build_select_all("posts")
        
        assert str(query1) == "SELECT * FROM users"
        assert str(query2) == "SELECT * FROM posts"


class TestBuilderPattern:
    """Tests demonstrating builder pattern benefits."""
    
    def test_same_builder_different_queries(self) -> None:
        """Test that the same builder can create different queries."""
        builder = QueryBuilder()
        
        simple_query = builder.reset().from_table("users").build()
        complex_query = (builder
            .reset()
            .select("name", "email", "age")
            .from_table("users")
            .where("active = 1")
            .where("age >= 18")
            .order_by("created_at", "DESC")
            .limit(100)
            .build())
        
        assert str(simple_query) == "SELECT * FROM users"
        assert "SELECT name, email, age FROM users WHERE active = 1 AND age >= 18 ORDER BY created_at DESC LIMIT 100" == str(complex_query)
    
    def test_step_by_step_construction(self) -> None:
        """Test that query can be built step by step."""
        builder = QueryBuilder()
        
        # Step 1: Select columns
        builder.select("name", "email")
        
        # Step 2: Add table
        builder.from_table("users")
        
        # Step 3: Add condition
        builder.where("active = 1")
        
        # Build at the end
        query = builder.build()
        
        assert str(query) == "SELECT name, email FROM users WHERE active = 1"
