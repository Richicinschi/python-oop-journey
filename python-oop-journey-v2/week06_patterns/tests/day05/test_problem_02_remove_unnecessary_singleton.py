"""Tests for Problem 02: Remove Unnecessary Singleton."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day05.problem_02_remove_unnecessary_singleton import (
    ApiClient,
    AppConfig,
    ConfigurableService,
    DatabaseConnection,
    ServiceLocator,
)


class TestAppConfig:
    """Tests for AppConfig (non-singleton)."""
    
    def test_config_with_defaults(self) -> None:
        config = AppConfig()
        assert config.get_database_url() == "postgresql://localhost/mydb"
        assert config.get_api_key() == "secret_key_123"
        assert config.get_timeout() == 30
        assert config.is_debug() is False
    
    def test_config_with_custom_values(self) -> None:
        custom_config = {
            "database_url": "mysql://localhost/testdb",
            "api_key": "custom_key",
            "timeout": 60,
            "debug": True,
        }
        config = AppConfig(custom_config)
        
        assert config.get_database_url() == "mysql://localhost/testdb"
        assert config.get_api_key() == "custom_key"
        assert config.get_timeout() == 60
        assert config.is_debug() is True
    
    def test_config_set_value(self) -> None:
        config = AppConfig()
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"
    
    def test_multiple_configs_are_independent(self) -> None:
        """Key benefit: multiple independent instances possible."""
        prod_config = AppConfig({
            "database_url": "prod-db.example.com",
            "api_key": "prod_key",
        })
        test_config = AppConfig({
            "database_url": "test-db.example.com",
            "api_key": "test_key",
        })
        
        assert prod_config.get_database_url() != test_config.get_database_url()
        assert prod_config.get_api_key() != test_config.get_api_key()


class TestDatabaseConnection:
    """Tests for DatabaseConnection with DI."""
    
    def test_connection_with_injected_config(self) -> None:
        config = AppConfig({"database_url": "test://localhost"})
        db = DatabaseConnection(config)
        
        assert db._url == "test://localhost"
        assert not db.is_connected()
    
    def test_connect_and_disconnect(self) -> None:
        config = AppConfig()
        db = DatabaseConnection(config)
        
        connect_result = db.connect()
        assert "Connected" in connect_result
        assert db.is_connected()
        
        disconnect_result = db.disconnect()
        assert "Disconnected" in disconnect_result
        assert not db.is_connected()
    
    def test_query_requires_connection(self) -> None:
        config = AppConfig()
        db = DatabaseConnection(config)
        
        with pytest.raises(RuntimeError, match="Not connected"):
            db.query("SELECT * FROM users")
    
    def test_query_when_connected(self) -> None:
        config = AppConfig()
        db = DatabaseConnection(config)
        db.connect()
        
        result = db.query("SELECT * FROM users")
        assert isinstance(result, list)
        assert result[0]["query"] == "SELECT * FROM users"
    
    def test_db_uses_injected_config_not_singleton(self) -> None:
        """Database receives config via injection, not global singleton."""
        test_config = AppConfig({"database_url": "test-db-url"})
        db = DatabaseConnection(test_config)
        
        # Verify it uses the injected config
        assert "test-db-url" in db._url


class TestApiClient:
    """Tests for ApiClient with DI."""
    
    def test_api_client_with_injected_config(self) -> None:
        config = AppConfig({"api_key": "my_api_key", "timeout": 45})
        client = ApiClient(config)
        
        assert client._api_key == "my_api_key"
        assert client._timeout == 45
    
    def test_make_request_uses_config(self) -> None:
        config = AppConfig({"api_key": "secret123", "timeout": 30})
        client = ApiClient(config)
        
        result = client.make_request("/users")
        
        assert result["endpoint"] == "/users"
        assert result["api_key"] == "secret123"
        assert result["timeout"] == 30
    
    def test_get_timeout(self) -> None:
        config = AppConfig({"timeout": 120})
        client = ApiClient(config)
        
        assert client.get_timeout() == 120


class TestConfigurableService:
    """Tests for ConfigurableService."""
    
    def test_service_composes_dependencies(self) -> None:
        config = AppConfig()
        db = DatabaseConnection(config)
        api = ApiClient(config)
        
        service = ConfigurableService(db, api)
        
        assert service._db is db
        assert service._api is api
    
    def test_fetch_and_store(self) -> None:
        config = AppConfig()
        db = DatabaseConnection(config)
        db.connect()
        api = ApiClient(config)
        
        service = ConfigurableService(db, api)
        result = service.fetch_and_store("/data", "my_table")
        
        assert result["status"] == "success"
        assert "api_response" in result
        assert "db_result" in result
    
    def test_get_db_connection_string(self) -> None:
        config = AppConfig({"database_url": "my-db-url"})
        db = DatabaseConnection(config)
        api = ApiClient(config)
        
        service = ConfigurableService(db, api)
        assert service.get_db_connection_string() == "my-db-url"
    
    def test_get_api_key(self) -> None:
        config = AppConfig({"api_key": "my-key"})
        db = DatabaseConnection(config)
        api = ApiClient(config)
        
        service = ConfigurableService(db, api)
        assert service.get_api_key() == "my-key"


class TestServiceLocator:
    """Tests for ServiceLocator."""
    
    def test_register_and_get_config(self) -> None:
        locator = ServiceLocator()
        config = AppConfig()
        
        locator.register_config(config)
        assert locator.get_config() is config
    
    def test_get_config_without_register_raises(self) -> None:
        locator = ServiceLocator()
        
        with pytest.raises(RuntimeError, match="Config not registered"):
            locator.get_config()
    
    def test_create_database_connection(self) -> None:
        locator = ServiceLocator()
        config = AppConfig({"database_url": "locator-test-db"})
        locator.register_config(config)
        
        db = locator.create_database_connection()
        assert isinstance(db, DatabaseConnection)
        assert db._url == "locator-test-db"
    
    def test_create_api_client(self) -> None:
        locator = ServiceLocator()
        config = AppConfig({"api_key": "locator-key"})
        locator.register_config(config)
        
        client = locator.create_api_client()
        assert isinstance(client, ApiClient)
        assert client._api_key == "locator-key"


class TestDependencyInjectionBenefits:
    """Tests demonstrating benefits of DI over Singleton."""
    
    def test_testability_with_mock_config(self) -> None:
        """We can inject test configurations easily."""
        # Test config with test values
        test_config = AppConfig({
            "database_url": "mock://test-db",
            "api_key": "test-key-123",
        })
        
        # Create components with test config
        db = DatabaseConnection(test_config)
        api = ApiClient(test_config)
        
        # Verify they use test values, not production values
        assert db._url == "mock://test-db"
        assert api._api_key == "test-key-123"
    
    def test_no_hidden_dependencies(self) -> None:
        """Dependencies are explicit, not hidden."""
        config = AppConfig()
        
        # Dependencies are explicit in constructor
        db = DatabaseConnection(config)
        
        # We can see what the dependency is
        assert db._config is config
    
    def test_independent_instances(self) -> None:
        """Each instance is independent - no global state."""
        config1 = AppConfig({"database_url": "db1"})
        config2 = AppConfig({"database_url": "db2"})
        
        db1 = DatabaseConnection(config1)
        db2 = DatabaseConnection(config2)
        
        # Changes to one don't affect the other
        db1.connect()
        assert db1.is_connected()
        assert not db2.is_connected()  # Independent state
