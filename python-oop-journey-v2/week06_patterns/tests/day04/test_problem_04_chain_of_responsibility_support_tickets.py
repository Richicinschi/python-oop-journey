"""Tests for Problem 04: Chain of Responsibility Support Tickets."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day04.problem_04_chain_of_responsibility_support_tickets import (
    TicketPriority,
    SupportTicket,
    SupportHandler,
    Level1Support,
    Level2Support,
    TechnicalSupport,
    ManagerSupport,
    SupportChain,
)


class TestTicketPriority:
    """Tests for TicketPriority enum."""
    
    def test_priority_levels_exist(self) -> None:
        """All priority levels are defined."""
        assert TicketPriority.LOW
        assert TicketPriority.MEDIUM
        assert TicketPriority.HIGH
        assert TicketPriority.CRITICAL


class TestSupportTicket:
    """Tests for SupportTicket class."""
    
    def test_ticket_creation(self) -> None:
        """Ticket can be created with all fields."""
        ticket = SupportTicket("TKT-001", "Login issue", TicketPriority.HIGH, "technical")
        assert ticket.ticket_id == "TKT-001"
        assert ticket.title == "Login issue"
        assert ticket.priority == TicketPriority.HIGH
        assert ticket.category == "technical"
    
    def test_ticket_repr(self) -> None:
        """Ticket has useful repr."""
        ticket = SupportTicket("TKT-001", "Test", TicketPriority.LOW, "general")
        repr_str = repr(ticket)
        assert "TKT-001" in repr_str
        assert "Test" in repr_str


class TestLevel1Support:
    """Tests for Level1Support handler."""
    
    def test_handles_low_priority(self) -> None:
        """Level 1 handles LOW priority tickets."""
        handler = Level1Support()
        ticket = SupportTicket("T1", "Question", TicketPriority.LOW, "billing")
        assert handler.can_handle(ticket)
    
    def test_handles_general_category(self) -> None:
        """Level 1 handles 'general' category tickets."""
        handler = Level1Support()
        ticket = SupportTicket("T1", "Question", TicketPriority.HIGH, "general")
        assert handler.can_handle(ticket)
    
    def test_does_not_handle_high_priority(self) -> None:
        """Level 1 does not handle HIGH priority non-general tickets."""
        handler = Level1Support()
        ticket = SupportTicket("T1", "Urgent", TicketPriority.HIGH, "technical")
        assert not handler.can_handle(ticket)
    
    def test_processing_message(self) -> None:
        """Processing returns appropriate message."""
        handler = Level1Support()
        ticket = SupportTicket("T1", "Help", TicketPriority.LOW, "general")
        result = handler.process(ticket)
        assert "Level 1 Support" in result
        assert "T1" in result


class TestLevel2Support:
    """Tests for Level2Support handler."""
    
    def test_handles_medium_priority(self) -> None:
        """Level 2 handles MEDIUM priority tickets."""
        handler = Level2Support()
        ticket = SupportTicket("T1", "Issue", TicketPriority.MEDIUM, "general")
        assert handler.can_handle(ticket)
    
    def test_handles_billing_category(self) -> None:
        """Level 2 handles 'billing' category tickets."""
        handler = Level2Support()
        ticket = SupportTicket("T1", "Refund", TicketPriority.LOW, "billing")
        assert handler.can_handle(ticket)
    
    def test_processing_message(self) -> None:
        """Processing returns appropriate message."""
        handler = Level2Support()
        ticket = SupportTicket("T1", "Billing", TicketPriority.MEDIUM, "billing")
        result = handler.process(ticket)
        assert "Level 2 Support" in result


class TestTechnicalSupport:
    """Tests for TechnicalSupport handler."""
    
    def test_handles_high_priority(self) -> None:
        """Technical handles HIGH priority tickets."""
        handler = TechnicalSupport()
        ticket = SupportTicket("T1", "Bug", TicketPriority.HIGH, "billing")
        assert handler.can_handle(ticket)
    
    def test_handles_technical_category(self) -> None:
        """Technical handles 'technical' category tickets."""
        handler = TechnicalSupport()
        ticket = SupportTicket("T1", "Error", TicketPriority.LOW, "technical")
        assert handler.can_handle(ticket)
    
    def test_processing_message(self) -> None:
        """Processing returns appropriate message."""
        handler = TechnicalSupport()
        ticket = SupportTicket("T1", "Crash", TicketPriority.HIGH, "technical")
        result = handler.process(ticket)
        assert "Technical Support" in result
        assert "investigation" in result.lower()


class TestManagerSupport:
    """Tests for ManagerSupport handler."""
    
    def test_handles_critical_priority(self) -> None:
        """Manager handles CRITICAL priority tickets."""
        handler = ManagerSupport()
        ticket = SupportTicket("T1", "Outage", TicketPriority.CRITICAL, "general")
        assert handler.can_handle(ticket)
    
    def test_handles_any_ticket(self) -> None:
        """Manager acts as catch-all for unhandled tickets."""
        handler = ManagerSupport()
        ticket = SupportTicket("T1", "Anything", TicketPriority.LOW, "unknown")
        assert handler.can_handle(ticket)
    
    def test_processing_message(self) -> None:
        """Processing returns appropriate message."""
        handler = ManagerSupport()
        ticket = SupportTicket("T1", "Escalation", TicketPriority.CRITICAL, "billing")
        result = handler.process(ticket)
        assert "Manager" in result
        assert "Executive" in result


class TestHandlerChain:
    """Tests for handler chaining behavior."""
    
    def test_set_next_returns_handler(self) -> None:
        """set_next returns the next handler for chaining."""
        h1 = Level1Support()
        h2 = Level2Support()
        result = h1.set_next(h2)
        assert result is h2
    
    def test_chain_passing(self) -> None:
        """Ticket passes to next handler when not handled."""
        level1 = Level1Support()
        level2 = Level2Support()
        level1.set_next(level2)
        
        # MEDIUM priority + billing ticket should pass from Level1 to Level2
        ticket = SupportTicket("T1", "Issue", TicketPriority.MEDIUM, "billing")
        result = level1.handle(ticket)
        
        assert "Level 2 Support" in result
    
    def test_chain_stops_when_handled(self) -> None:
        """Ticket stops at first handler that can process it."""
        level1 = Level1Support()
        level2 = Level2Support()
        level1.set_next(level2)
        
        # LOW priority ticket handled by Level1
        ticket = SupportTicket("T1", "Question", TicketPriority.LOW, "technical")
        result = level1.handle(ticket)
        
        assert "Level 1 Support" in result
    
    def test_unhandled_ticket_no_handler(self) -> None:
        """Ticket with no handler returns appropriate message."""
        handler = Level1Support()
        ticket = SupportTicket("T1", "Unknown", TicketPriority.HIGH, "unknown")
        result = handler.handle(ticket)
        
        assert "No handler available" in result


class TestSupportChainFacade:
    """Tests for SupportChain facade."""
    
    def test_chain_initialization(self) -> None:
        """SupportChain initializes with all handlers."""
        chain = SupportChain()
        assert chain is not None
    
    def test_submit_ticket_returns_result(self) -> None:
        """Submitting ticket returns handler result."""
        chain = SupportChain()
        ticket = SupportTicket("T1", "Help", TicketPriority.LOW, "general")
        result = chain.submit_ticket(ticket)
        
        assert isinstance(result, str)
        assert "Support" in result or "Manager" in result
    
    def test_chain_description(self) -> None:
        """Chain description shows handler order."""
        chain = SupportChain()
        description = chain.get_chain_description()
        
        assert "Level 1 Support" in description
        assert "Level 2 Support" in description
        assert "Technical Support" in description
        assert "Manager" in description
        assert "->" in description
    
    def test_low_priority_ticket_handled_by_level1(self) -> None:
        """LOW priority ticket goes to Level 1."""
        chain = SupportChain()
        ticket = SupportTicket("T1", "Question", TicketPriority.LOW, "technical")
        result = chain.submit_ticket(ticket)
        
        assert "Level 1 Support" in result
    
    def test_medium_priority_ticket_handled_by_level2(self) -> None:
        """MEDIUM priority ticket goes to Level 2."""
        chain = SupportChain()
        ticket = SupportTicket("T1", "Issue", TicketPriority.MEDIUM, "technical")
        result = chain.submit_ticket(ticket)
        
        assert "Level 2 Support" in result
    
    def test_high_priority_ticket_handled_by_technical(self) -> None:
        """HIGH priority ticket goes to Technical Support."""
        chain = SupportChain()
        ticket = SupportTicket("T1", "Bug", TicketPriority.HIGH, "technical")
        result = chain.submit_ticket(ticket)
        
        assert "Technical Support" in result
    
    def test_critical_ticket_handled_by_manager(self) -> None:
        """CRITICAL priority ticket goes to Manager."""
        chain = SupportChain()
        ticket = SupportTicket("T1", "Outage", TicketPriority.CRITICAL, "general")
        result = chain.submit_ticket(ticket)
        
        assert "Manager" in result


class TestChainOfResponsibilityPattern:
    """Tests verifying the Chain of Responsibility pattern."""
    
    def test_handler_is_abstract(self) -> None:
        """SupportHandler cannot be instantiated directly."""
        with pytest.raises(TypeError):
            SupportHandler("Test")  # type: ignore[abstract]
    
    def test_all_handlers_inherit_base(self) -> None:
        """All handlers inherit from SupportHandler."""
        assert issubclass(Level1Support, SupportHandler)
        assert issubclass(Level2Support, SupportHandler)
        assert issubclass(TechnicalSupport, SupportHandler)
        assert issubclass(ManagerSupport, SupportHandler)
    
    def test_chain_is_linear(self) -> None:
        """Handlers form a linear chain."""
        h1 = Level1Support()
        h2 = Level2Support()
        h3 = TechnicalSupport()
        
        h1.set_next(h2).set_next(h3)
        
        assert h1._next is h2
        assert h2._next is h3
        assert h3._next is None
