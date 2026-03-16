"""Reference solution for Problem 04: Chain of Responsibility Support Tickets."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import override


class TicketPriority(Enum):
    """Priority levels for support tickets."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class SupportTicket:
    """Represents a support ticket."""
    
    def __init__(self, ticket_id: str, title: str, priority: TicketPriority, category: str) -> None:
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.category = category
    
    def __repr__(self) -> str:
        return f"SupportTicket({self.ticket_id!r}, {self.title!r}, {self.priority.name}, {self.category!r})"


class SupportHandler(ABC):
    """Abstract base class for support ticket handlers."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._next: SupportHandler | None = None
    
    def set_next(self, handler: SupportHandler) -> SupportHandler:
        """Set the next handler in the chain."""
        self._next = handler
        return handler
    
    def handle(self, ticket: SupportTicket) -> str:
        """Handle a ticket or pass to next handler."""
        if self.can_handle(ticket):
            return self.process(ticket)
        if self._next:
            return self._next.handle(ticket)
        return f"No handler available for ticket {ticket.ticket_id}"
    
    @abstractmethod
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Check if this handler can process the ticket."""
        pass
    
    @abstractmethod
    def process(self, ticket: SupportTicket) -> str:
        """Process the ticket."""
        pass


class Level1Support(SupportHandler):
    """Level 1 Support: Handles LOW priority and 'general' category tickets."""
    
    def __init__(self) -> None:
        super().__init__("Level 1 Support")
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        # Handle LOW priority (any category) OR general category (but not CRITICAL)
        if ticket.priority == TicketPriority.CRITICAL:
            return False
        return ticket.priority == TicketPriority.LOW or ticket.category == "general"
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        return f"[{self.name}] Processed {ticket.ticket_id}: '{ticket.title}' - Standard response sent"


class Level2Support(SupportHandler):
    """Level 2 Support: Handles MEDIUM priority and 'billing' category tickets."""
    
    def __init__(self) -> None:
        super().__init__("Level 2 Support")
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        # Handle MEDIUM priority or billing category (but not CRITICAL or HIGH technical)
        if ticket.priority == TicketPriority.CRITICAL:
            return False
        if ticket.priority == TicketPriority.HIGH and ticket.category == "technical":
            return False
        return ticket.priority == TicketPriority.MEDIUM or ticket.category == "billing"
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        return f"[{self.name}] Processed {ticket.ticket_id}: '{ticket.title}' - Account reviewed"


class TechnicalSupport(SupportHandler):
    """Technical Support: Handles HIGH priority and 'technical' category tickets."""
    
    def __init__(self) -> None:
        super().__init__("Technical Support")
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        # Handle HIGH priority (except CRITICAL) or technical category
        if ticket.priority == TicketPriority.CRITICAL:
            return False
        return ticket.priority == TicketPriority.HIGH or ticket.category == "technical"
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        return f"[{self.name}] Processed {ticket.ticket_id}: '{ticket.title}' - Technical investigation started"


class ManagerSupport(SupportHandler):
    """Manager Support: Handles CRITICAL priority and escalated tickets."""
    
    def __init__(self) -> None:
        super().__init__("Manager")
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        return ticket.priority == TicketPriority.CRITICAL or True
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        return f"[{self.name}] Processed {ticket.ticket_id}: '{ticket.title}' - Executive review initiated"


class SupportChain:
    """Facade for building and using the support chain."""
    
    def __init__(self) -> None:
        self._level1 = Level1Support()
        self._level2 = Level2Support()
        self._tech = TechnicalSupport()
        self._manager = ManagerSupport()
        
        # Build chain: Level1 -> Level2 -> Technical -> Manager
        self._level1.set_next(self._level2).set_next(self._tech).set_next(self._manager)
        self._head = self._level1
    
    def submit_ticket(self, ticket: SupportTicket) -> str:
        """Submit a ticket to the chain for handling."""
        return self._head.handle(ticket)
    
    def get_chain_description(self) -> str:
        """Return a description of the support chain."""
        handlers = []
        current: SupportHandler | None = self._head
        while current:
            handlers.append(current.name)
            current = current._next
        return " -> ".join(handlers)
