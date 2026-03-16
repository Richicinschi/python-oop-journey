"""Problem 01: Observer Stock Ticker

Topic: Observer Pattern
Difficulty: Medium

Implement the Observer pattern for a stock price monitoring system.

HINTS:
- Hint 1 (Conceptual): Focus on the one-to-many relationship. The Stock doesn't 
  need to know what observers do, just that they have an update() method.
- Hint 2 (Structural): Stock needs: __init__ with observers list, attach(), 
  detach(), notify(). Observers need: update() that receives the Stock.
- Hint 3 (Edge Case): What happens if an observer detaches itself during 
  notification? Consider iterating over a copy of the observers list.

PATTERN EXPLANATION:
The Observer pattern defines a one-to-many dependency between objects so that
when one object (the Subject) changes state, all its dependents (Observers)
are notified and updated automatically.

STRUCTURE:
- Subject (Stock): Maintains a list of observers and notifies them of changes
- Observer (StockObserver): Interface for objects that should be notified
- ConcreteObserver (PriceDisplay, AlertSystem): Receive and process updates

WHEN TO USE:
- When changes to one object require changing others
- When you need to maintain consistency across related objects
- For event handling systems, pub-sub architectures

EXAMPLE USAGE:
    stock = Stock("AAPL", 150.0)
    display = PriceDisplay()
    alerts = AlertSystem(high_threshold=200.0, low_threshold=100.0)
    
    stock.attach(display)
    stock.attach(alerts)
    
    stock.price = 175.0  # Both observers notified
    print(display.get_last_price())  # 175.0

TODO:
1. Create StockObserver abstract base class with update(self, stock: Stock) method
2. Create Stock class (Subject) that maintains price and list of observers
3. Implement attach() and detach() methods in Stock
4. Implement notify() to call update() on all observers
5. Create concrete observers: PriceDisplay and AlertSystem
6. PriceDisplay should track price history
7. AlertSystem should trigger when price crosses thresholds
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class StockObserver(ABC):
    """Abstract observer for stock price updates."""
    
    @abstractmethod
    def update(self, stock: Stock) -> None:
        """Receive update from stock.
        
        Args:
            stock: The stock that changed.
        """
        # TODO: Implement abstract update method
        raise NotImplementedError("update must be implemented")


class Stock:
    """Stock subject that notifies observers of price changes."""
    
    def __init__(self, symbol: str, initial_price: float) -> None:
        """Initialize stock with symbol and price.
        
        Args:
            symbol: Stock ticker symbol.
            initial_price: Starting price.
        """
        # TODO: Initialize symbol, price, and observers list
        raise NotImplementedError("Initialize stock")
    
    @property
    def symbol(self) -> str:
        """Get stock symbol."""
        # TODO: Return symbol
        raise NotImplementedError("Return symbol")
    
    @property
    def price(self) -> float:
        """Get current price."""
        # TODO: Return price
        raise NotImplementedError("Return price")
    
    @price.setter
    def price(self, value: float) -> None:
        """Set price and notify observers.
        
        Args:
            value: New price value.
        """
        # TODO: Update price and call notify()
        raise NotImplementedError("Set price and notify")
    
    def attach(self, observer: StockObserver) -> None:
        """Add an observer.
        
        Args:
            observer: Observer to add.
        """
        # TODO: Add observer to list
        raise NotImplementedError("Attach observer")
    
    def detach(self, observer: StockObserver) -> None:
        """Remove an observer.
        
        Args:
            observer: Observer to remove.
        """
        # TODO: Remove observer from list
        raise NotImplementedError("Detach observer")
    
    def notify(self) -> None:
        """Notify all observers of price change."""
        # TODO: Call update() on all observers
        raise NotImplementedError("Notify observers")


class PriceDisplay(StockObserver):
    """Observer that displays and tracks stock prices."""
    
    def __init__(self) -> None:
        """Initialize price display with empty history."""
        # TODO: Initialize price_history list
        raise NotImplementedError("Initialize display")
    
    def update(self, stock: Stock) -> None:
        """Receive price update.
        
        Args:
            stock: The stock that changed.
        """
        # TODO: Record price in history
        raise NotImplementedError("Update display")
    
    def get_price_history(self) -> List[float]:
        """Get recorded price history.
        
        Returns:
            List of observed prices.
        """
        # TODO: Return price history
        raise NotImplementedError("Return price history")
    
    def get_last_price(self) -> float | None:
        """Get most recent price.
        
        Returns:
            Last price or None if no history.
        """
        # TODO: Return last price or None
        raise NotImplementedError("Return last price")


class AlertSystem(StockObserver):
    """Observer that triggers alerts when price crosses thresholds."""
    
    def __init__(self, high_threshold: float, low_threshold: float) -> None:
        """Initialize alert system with thresholds.
        
        Args:
            high_threshold: Price above which to trigger high alert.
            low_threshold: Price below which to trigger low alert.
        """
        # TODO: Initialize thresholds and alerts list
        raise NotImplementedError("Initialize alerts")
    
    def update(self, stock: Stock) -> None:
        """Check price and trigger alerts if thresholds crossed.
        
        Args:
            stock: The stock that changed.
        """
        # TODO: Check thresholds and record alerts
        raise NotImplementedError("Check and trigger alerts")
    
    def get_alerts(self) -> List[str]:
        """Get all triggered alerts.
        
        Returns:
            List of alert messages.
        """
        # TODO: Return alerts list
        raise NotImplementedError("Return alerts")
