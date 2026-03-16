"""Problem 04: Chain of Responsibility Support Tickets

Topic: Chain of Responsibility Pattern
Difficulty: Medium

Implement a support ticket handling system using Chain of Responsibility.
Tickets are passed along a chain of handlers until one can process them.

HINTS:
- Hint 1 (Conceptual): Each handler decides: handle it OR pass to next. Handlers 
  don't know about each other, only the next handler in chain.
- Hint 2 (Structural): Base Handler has set_next() to build chain. handle() 
  method either processes or calls next.handle(). Concrete handlers override 
  can_handle() and process().
- Hint 3 (Edge Case): Ticket may reach end of chain unhandled. Return appropriate 
  message. Check for circular chains (A->B->A). Handler can modify ticket before 
  passing to next (e.g., add notes).
"""

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
    """Represents a support ticket.
    
    Attributes:
        id: Unique ticket identifier
        title: Brief title/description
        priority: Ticket priority level
        category: Ticket category (e.g., 'billing', 'technical', 'general')
    """
    
    def __init__(self, ticket_id: str, title: str, priority: TicketPriority, category: str) -> None:
        """Initialize a support ticket.
        
        Args:
            ticket_id: Unique identifier for the ticket
            title: Brief description of the issue
            priority: Priority level (LOW, MEDIUM, HIGH, CRITICAL)
            category: Category of the issue
        """
        raise NotImplementedError("Implement SupportTicket.__init__")
    
    def __repr__(self) -> str:
        """String representation of the ticket."""
        raise NotImplementedError("Implement SupportTicket.__repr__")


class SupportHandler(ABC):
    """Abstract base class for support ticket handlers.
    
    Each handler can either process a ticket or pass it to the next handler.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize handler with a name.
        
        Args:
            name: Name/role of this handler
        """
        raise NotImplementedError("Implement SupportHandler.__init__")
    
    def set_next(self, handler: SupportHandler) -> SupportHandler:
        """Set the next handler in the chain.
        
        Args:
            handler: The next handler to receive tickets this handler can't process
            
        Returns:
            The handler argument (for method chaining)
        """
        raise NotImplementedError("Implement SupportHandler.set_next")
    
    def handle(self, ticket: SupportTicket) -> str:
        """Handle a ticket or pass to next handler.
        
        This method implements the chain traversal logic.
        Should NOT be overridden by subclasses.
        
        Args:
            ticket: The support ticket to handle
            
        Returns:
            Result message indicating how the ticket was handled
        """
        raise NotImplementedError("Implement SupportHandler.handle")
    
    @abstractmethod
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Check if this handler can process the ticket.
        
        Args:
            ticket: The ticket to evaluate
            
        Returns:
            True if this handler can process the ticket, False otherwise
        """
        raise NotImplementedError("Implement can_handle")
    
    @abstractmethod
    def process(self, ticket: SupportTicket) -> str:
        """Process the ticket.
        
        Only called when can_handle() returns True.
        
        Args:
            ticket: The ticket to process
            
        Returns:
            Processing result message
        """
        raise NotImplementedError("Implement process")


class Level1Support(SupportHandler):
    """Level 1 Support: Handles LOW priority and 'general' category tickets."""
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Can handle LOW priority or 'general' category tickets."""
        raise NotImplementedError("Implement Level1Support.can_handle")
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        """Process ticket with Level 1 support response."""
        raise NotImplementedError("Implement Level1Support.process")


class Level2Support(SupportHandler):
    """Level 2 Support: Handles MEDIUM priority and 'billing' category tickets."""
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Can handle MEDIUM priority or 'billing' category tickets."""
        raise NotImplementedError("Implement Level2Support.can_handle")
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        """Process ticket with Level 2 support response."""
        raise NotImplementedError("Implement Level2Support.process")


class TechnicalSupport(SupportHandler):
    """Technical Support: Handles HIGH priority and 'technical' category tickets."""
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Can handle HIGH priority or 'technical' category tickets."""
        raise NotImplementedError("Implement TechnicalSupport.can_handle")
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        """Process ticket with technical support response."""
        raise NotImplementedError("Implement TechnicalSupport.process")


class ManagerSupport(SupportHandler):
    """Manager Support: Handles CRITICAL priority and escalated tickets.
    
    This is the final handler in the chain - it handles anything that reaches it.
    """
    
    @override
    def can_handle(self, ticket: SupportTicket) -> bool:
        """Can handle CRITICAL priority tickets OR any ticket (final handler)."""
        raise NotImplementedError("Implement ManagerSupport.can_handle")
    
    @override
    def process(self, ticket: SupportTicket) -> str:
        """Process ticket with manager response."""
        raise NotImplementedError("Implement ManagerSupport.process")


class SupportChain:
    """Facade for building and using the support chain.
    
    Provides a simple interface for creating the standard support chain.
    """
    
    def __init__(self) -> None:
        """Initialize and build the support chain."""
        raise NotImplementedError("Implement SupportChain.__init__")
    
    def submit_ticket(self, ticket: SupportTicket) -> str:
        """Submit a ticket to the chain for handling.
        
        Args:
            ticket: The support ticket to handle
            
        Returns:
            Result of ticket handling
        """
        raise NotImplementedError("Implement SupportChain.submit_ticket")
    
    def get_chain_description(self) -> str:
        """Return a description of the support chain.
        
        Returns:
            String showing the chain structure
        """
        raise NotImplementedError("Implement SupportChain.get_chain_description")
