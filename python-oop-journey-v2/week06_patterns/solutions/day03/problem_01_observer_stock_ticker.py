"""Solution: Observer Stock Ticker.

Implements the Observer pattern for stock price monitoring.

WHY OBSERVER?
The Observer pattern creates a publish-subscribe relationship between objects.
This is ideal when:
- Changes to one object require updating multiple other objects
- You want loose coupling between the subject and observers
- The number of dependent objects is unknown or changes dynamically

KEY BENEFIT: The Stock class doesn't need to know what PriceDisplay or
AlertSystem do with the data. We can add new observer types (ChartPlotter,
Logger) without modifying the Stock class.
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
        pass


class Stock:
    """Stock subject that notifies observers of price changes.
    
    The Subject maintains a list of observers and notifies them automatically
    when its state changes. This decouples the subject from knowing specifics
    about its observers.
    """
    
    def __init__(self, symbol: str, initial_price: float) -> None:
        """Initialize stock with symbol and price.
        
        Args:
            symbol: Stock ticker symbol.
            initial_price: Starting price.
        """
        self._symbol = symbol
        self._price = initial_price
        self._observers: List[StockObserver] = []
    
    @property
    def symbol(self) -> str:
        """Get stock symbol."""
        return self._symbol
    
    @property
    def price(self) -> float:
        """Get current price."""
        return self._price
    
    @price.setter
    def price(self, value: float) -> None:
        """Set price and notify observers.
        
        The key insight: when state changes, we automatically notify all
        registered observers. They receive the entire subject object, allowing
        them to pull any data they need (price, symbol, etc.).
        
        Args:
            value: New price value.
        """
        self._price = value
        self.notify()  # Push notification to all observers
    
    def attach(self, observer: StockObserver) -> None:
        """Add an observer.
        
        Args:
            observer: Observer to add.
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: StockObserver) -> None:
        """Remove an observer.
        
        Args:
            observer: Observer to remove.
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers of price change."""
        for observer in self._observers:
            observer.update(self)


class PriceDisplay(StockObserver):
    """Observer that displays and tracks stock prices."""
    
    def __init__(self) -> None:
        """Initialize price display with empty history."""
        self._price_history: List[float] = []
    
    def update(self, stock: Stock) -> None:
        """Receive price update.
        
        Args:
            stock: The stock that changed.
        """
        self._price_history.append(stock.price)
    
    def get_price_history(self) -> List[float]:
        """Get recorded price history.
        
        Returns:
            List of observed prices.
        """
        return self._price_history.copy()
    
    def get_last_price(self) -> float | None:
        """Get most recent price.
        
        Returns:
            Last price or None if no history.
        """
        if self._price_history:
            return self._price_history[-1]
        return None


class AlertSystem(StockObserver):
    """Observer that triggers alerts when price crosses thresholds."""
    
    def __init__(self, high_threshold: float, low_threshold: float) -> None:
        """Initialize alert system with thresholds.
        
        Args:
            high_threshold: Price above which to trigger high alert.
            low_threshold: Price below which to trigger low alert.
        """
        self._high_threshold = high_threshold
        self._low_threshold = low_threshold
        self._alerts: List[str] = []
    
    def update(self, stock: Stock) -> None:
        """Check price and trigger alerts if thresholds crossed.
        
        Args:
            stock: The stock that changed.
        """
        price = stock.price
        if price > self._high_threshold:
            self._alerts.append(f"HIGH ALERT: {stock.symbol} at ${price:.2f}")
        elif price < self._low_threshold:
            self._alerts.append(f"LOW ALERT: {stock.symbol} at ${price:.2f}")
    
    def get_alerts(self) -> List[str]:
        """Get all triggered alerts.
        
        Returns:
            List of alert messages.
        """
        return self._alerts.copy()
