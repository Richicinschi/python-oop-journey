"""Tests for Problem 01: Observer Stock Ticker."""

from __future__ import annotations

import pytest
from abc import ABC

from week06_patterns.solutions.day03.problem_01_observer_stock_ticker import (
    StockObserver,
    Stock,
    PriceDisplay,
    AlertSystem,
)


class TestStockObserver:
    """Test StockObserver abstract base class."""
    
    def test_stock_observer_is_abstract(self) -> None:
        """Test that StockObserver cannot be instantiated."""
        assert issubclass(StockObserver, ABC)
        with pytest.raises(TypeError, match="abstract"):
            StockObserver()
    
    def test_stock_observer_has_update_method(self) -> None:
        """Test that StockObserver defines update method."""
        assert hasattr(StockObserver, 'update')


class TestStock:
    """Test Stock subject class."""
    
    def test_initialization(self) -> None:
        """Test stock initialization."""
        stock = Stock("AAPL", 150.0)
        assert stock.symbol == "AAPL"
        assert stock.price == 150.0
    
    def test_price_update(self) -> None:
        """Test price can be updated."""
        stock = Stock("AAPL", 150.0)
        stock.price = 155.0
        assert stock.price == 155.0
    
    def test_attach_observer(self) -> None:
        """Test attaching observer."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        stock.attach(display)
        
        stock.price = 155.0
        assert len(display.get_price_history()) == 1
    
    def test_detach_observer(self) -> None:
        """Test detaching observer."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        stock.attach(display)
        stock.detach(display)
        
        stock.price = 155.0
        assert len(display.get_price_history()) == 0
    
    def test_multiple_observers_notified(self) -> None:
        """Test all observers are notified."""
        stock = Stock("AAPL", 150.0)
        display1 = PriceDisplay()
        display2 = PriceDisplay()
        
        stock.attach(display1)
        stock.attach(display2)
        stock.price = 155.0
        
        assert len(display1.get_price_history()) == 1
        assert len(display2.get_price_history()) == 1
    
    def test_duplicate_attach_ignored(self) -> None:
        """Test attaching same observer twice is handled."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        
        stock.attach(display)
        stock.attach(display)  # Duplicate attach
        stock.price = 155.0
        
        # Should only get one notification
        assert len(display.get_price_history()) == 1


class TestPriceDisplay:
    """Test PriceDisplay observer."""
    
    def test_initialization(self) -> None:
        """Test display initializes with empty history."""
        display = PriceDisplay()
        assert display.get_price_history() == []
        assert display.get_last_price() is None
    
    def test_update_records_price(self) -> None:
        """Test update records the stock price."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        
        stock.attach(display)
        stock.price = 155.0
        
        assert display.get_price_history() == [155.0]
        assert display.get_last_price() == 155.0
    
    def test_multiple_updates(self) -> None:
        """Test multiple price updates are recorded."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        
        stock.attach(display)
        stock.price = 155.0
        stock.price = 160.0
        stock.price = 158.0
        
        assert display.get_price_history() == [155.0, 160.0, 158.0]
        assert display.get_last_price() == 158.0
    
    def test_get_price_history_returns_copy(self) -> None:
        """Test get_price_history returns a copy."""
        stock = Stock("AAPL", 150.0)
        display = PriceDisplay()
        
        stock.attach(display)
        stock.price = 155.0
        
        history = display.get_price_history()
        history.append(999.0)
        
        # Original should be unchanged
        assert display.get_price_history() == [155.0]


class TestAlertSystem:
    """Test AlertSystem observer."""
    
    def test_initialization(self) -> None:
        """Test alert system initialization."""
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        assert alerts.get_alerts() == []
    
    def test_high_alert_triggered(self) -> None:
        """Test alert when price exceeds high threshold."""
        stock = Stock("AAPL", 190.0)
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        
        stock.attach(alerts)
        stock.price = 210.0
        
        assert len(alerts.get_alerts()) == 1
        assert "HIGH ALERT" in alerts.get_alerts()[0]
        assert "210.0" in alerts.get_alerts()[0]
    
    def test_low_alert_triggered(self) -> None:
        """Test alert when price goes below low threshold."""
        stock = Stock("AAPL", 110.0)
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        
        stock.attach(alerts)
        stock.price = 90.0
        
        assert len(alerts.get_alerts()) == 1
        assert "LOW ALERT" in alerts.get_alerts()[0]
        assert "90.0" in alerts.get_alerts()[0]
    
    def test_no_alert_in_normal_range(self) -> None:
        """Test no alert when price is within normal range."""
        stock = Stock("AAPL", 150.0)
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        
        stock.attach(alerts)
        stock.price = 150.0
        stock.price = 180.0
        stock.price = 120.0
        
        assert len(alerts.get_alerts()) == 0
    
    def test_multiple_alerts(self) -> None:
        """Test multiple alerts can be triggered."""
        stock = Stock("AAPL", 150.0)
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        
        stock.attach(alerts)
        stock.price = 210.0  # High alert
        stock.price = 90.0   # Low alert
        stock.price = 220.0  # High alert again
        
        assert len(alerts.get_alerts()) == 3
        assert "HIGH ALERT" in alerts.get_alerts()[0]
        assert "LOW ALERT" in alerts.get_alerts()[1]
        assert "HIGH ALERT" in alerts.get_alerts()[2]
    
    def test_get_alerts_returns_copy(self) -> None:
        """Test get_alerts returns a copy."""
        stock = Stock("AAPL", 210.0)
        alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
        
        stock.attach(alerts)
        stock.price = 220.0
        
        alert_list = alerts.get_alerts()
        alert_list.append("Modified")
        
        # Original should be unchanged
        assert len(alerts.get_alerts()) == 1
