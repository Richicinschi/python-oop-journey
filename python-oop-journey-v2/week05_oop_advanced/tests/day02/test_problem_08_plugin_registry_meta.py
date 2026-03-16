"""Tests for Problem 08: Plugin Registry Metaclass."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day02.problem_08_plugin_registry_meta import (
    BasePlugin,
    CSVParser,
    JSONParser,
    PDFExporter,
    PluginMeta,
)


class TestPluginMeta:
    """Tests for the PluginMeta metaclass."""
    
    def setup_method(self) -> None:
        """Clear registry before each test."""
        PluginMeta.clear_registry()
    
    def test_metaclass_exists(self) -> None:
        """Test that PluginMeta is defined."""
        assert isinstance(PluginMeta, type)
    
    def test_base_plugin_not_registered(self) -> None:
        """Test that BasePlugin is not in registry."""
        registry = PluginMeta.get_registry()
        for category in registry.values():
            assert BasePlugin not in category.values()
    
    def test_plugin_auto_registration(self) -> None:
        """Test that plugins are auto-registered."""
        PluginMeta.clear_registry()
        
        class TestPlugin(BasePlugin):
            plugin_category = "test"
            plugin_name = "test_plugin"
        
        assert PluginMeta.get_plugin("test", "test_plugin") is TestPlugin
    
    def test_get_plugins_by_category(self) -> None:
        """Test get_plugins_by_category method."""
        PluginMeta.clear_registry()
        
        class Plugin1(BasePlugin):
            plugin_category = "cat1"
            plugin_name = "p1"
        
        class Plugin2(BasePlugin):
            plugin_category = "cat1"
            plugin_name = "p2"
        
        cat1_plugins = PluginMeta.get_plugins_by_category("cat1")
        assert len(cat1_plugins) == 2
        assert "p1" in cat1_plugins
        assert "p2" in cat1_plugins
    
    def test_get_plugin_not_found(self) -> None:
        """Test get_plugin returns None for unknown plugin."""
        assert PluginMeta.get_plugin("unknown", "unknown") is None
    
    def test_clear_registry(self) -> None:
        """Test clear_registry clears all plugins."""
        class TempPlugin(BasePlugin):
            plugin_category = "temp"
            plugin_name = "temp_plugin"
        
        assert len(PluginMeta.get_registry()) > 0
        PluginMeta.clear_registry()
        assert len(PluginMeta.get_registry()) == 0
    
    def test_plugin_without_category_not_registered(self) -> None:
        """Test plugins without category/name are not registered."""
        PluginMeta.clear_registry()
        
        class Incomplete(BasePlugin):
            pass  # No plugin_category or plugin_name
        
        # Should not be in registry
        for category in PluginMeta.get_registry().values():
            assert "Incomplete" not in category


class TestBasePlugin:
    """Tests for the BasePlugin class."""
    
    def test_base_plugin_default_attributes(self) -> None:
        """Test BasePlugin default attribute values."""
        assert BasePlugin.plugin_category == ""
        assert BasePlugin.plugin_name == ""
        assert BasePlugin.plugin_version == "1.0.0"
        assert BasePlugin.plugin_priority == 0
        assert BasePlugin.plugin_dependencies == []
    
    def test_base_plugin_init(self) -> None:
        """Test BasePlugin initialization."""
        plugin = BasePlugin({"key": "value"})
        assert plugin.config == {"key": "value"}
        assert plugin._active is False
    
    def test_base_plugin_activate(self) -> None:
        """Test BasePlugin activate method."""
        plugin = BasePlugin()
        result = plugin.activate()
        
        assert plugin._active is True
        assert "activated" in result.lower()
    
    def test_base_plugin_deactivate(self) -> None:
        """Test BasePlugin deactivate method."""
        plugin = BasePlugin()
        plugin.activate()
        result = plugin.deactivate()
        
        assert plugin._active is False
        assert "deactivated" in result.lower()
    
    def test_base_plugin_get_info(self) -> None:
        """Test BasePlugin get_info method."""
        plugin = BasePlugin()
        info = plugin.get_info()
        
        assert "name" in info
        assert "category" in info
        assert "version" in info
        assert "priority" in info
        assert "dependencies" in info
        assert "active" in info


class TestCSVParser:
    """Tests for the CSVParser plugin."""
    
    def test_csv_parser_registration(self) -> None:
        """Test CSVParser is registered correctly."""
        PluginMeta.clear_registry()
        # Re-import or access to trigger registration
        csv_plugin = CSVParser
        
        assert csv_plugin.plugin_category == "parsers"
        assert csv_plugin.plugin_name == "csv"
        assert csv_plugin.plugin_version == "2.0.0"
    
    def test_csv_parser_init(self) -> None:
        """Test CSVParser initialization."""
        parser = CSVParser({"delimiter": ";"})
        assert parser.delimiter == ";"
    
    def test_csv_parser_parse(self) -> None:
        """Test CSVParser parse method."""
        parser = CSVParser()
        result = parser.parse("a,b,c\n1,2,3")
        
        assert result == [["a", "b", "c"], ["1", "2", "3"]]
    
    def test_csv_parser_parse_custom_delimiter(self) -> None:
        """Test CSVParser with custom delimiter."""
        parser = CSVParser({"delimiter": ";"})
        result = parser.parse("a;b;c")
        
        assert result == [["a", "b", "c"]]


class TestJSONParser:
    """Tests for the JSONParser plugin."""
    
    def test_json_parser_registration(self) -> None:
        """Test JSONParser is registered correctly."""
        assert JSONParser.plugin_category == "parsers"
        assert JSONParser.plugin_name == "json"
        assert JSONParser.plugin_version == "1.5.0"
    
    def test_json_parser_parse(self) -> None:
        """Test JSONParser parse method."""
        parser = JSONParser()
        result = parser.parse('{"key": "value", "num": 42}')
        
        assert result == {"key": "value", "num": 42}
    
    def test_json_parser_parse_list(self) -> None:
        """Test JSONParser with array JSON."""
        parser = JSONParser()
        result = parser.parse('[1, 2, 3]')
        
        assert result == [1, 2, 3]


class TestPDFExporter:
    """Tests for the PDFExporter plugin."""
    
    def test_pdf_exporter_registration(self) -> None:
        """Test PDFExporter is registered correctly."""
        assert PDFExporter.plugin_category == "exporters"
        assert PDFExporter.plugin_name == "pdf"
    
    def test_pdf_exporter_export(self) -> None:
        """Test PDFExporter export method."""
        exporter = PDFExporter()
        result = exporter.export({"data": "test"}, "output")
        
        assert "exported" in result.lower()
        assert "output.pdf" in result
