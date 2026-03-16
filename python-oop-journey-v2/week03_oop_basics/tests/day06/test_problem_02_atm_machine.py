"""Tests for Problem 02: ATM Machine."""

from __future__ import annotations

import pytest

from week03_oop_basics.solutions.day06.problem_02_atm_machine import (
    Account,
    ATM,
    Card,
    Deposit,
    TransactionType,
    Withdrawal,
)


class TestAccount:
    """Tests for Account class."""
    
    def test_account_creation(self) -> None:
        """Test account initialization."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.account_id == "ACC001"
        assert account.owner_name == "John Doe"
        assert account.balance == 100.0
    
    def test_account_default_balance(self) -> None:
        """Test account default zero balance."""
        account = Account("ACC001", "John Doe")
        assert account.balance == 0.0
    
    def test_deposit_success(self) -> None:
        """Test successful deposit."""
        account = Account("ACC001", "John Doe")
        assert account.deposit(50.0) is True
        assert account.balance == 50.0
    
    def test_deposit_negative_amount(self) -> None:
        """Test deposit with negative amount fails."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.deposit(-50.0) is False
        assert account.balance == 100.0
    
    def test_deposit_zero(self) -> None:
        """Test deposit with zero fails."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.deposit(0.0) is False
        assert account.balance == 100.0
    
    def test_withdraw_success(self) -> None:
        """Test successful withdrawal."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.withdraw(50.0) is True
        assert account.balance == 50.0
    
    def test_withdraw_insufficient_funds(self) -> None:
        """Test withdrawal with insufficient funds fails."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.withdraw(150.0) is False
        assert account.balance == 100.0
    
    def test_withdraw_negative_amount(self) -> None:
        """Test withdrawal with negative amount fails."""
        account = Account("ACC001", "John Doe", 100.0)
        assert account.withdraw(-50.0) is False
        assert account.balance == 100.0
    
    def test_get_transaction_history(self) -> None:
        """Test transaction history tracking."""
        account = Account("ACC001", "John Doe")
        account.add_transaction(Deposit("TXN001", "ACC001", 100.0))
        
        history = account.get_transaction_history()
        assert len(history) == 1
        assert history[0].transaction_id == "TXN001"


class TestCard:
    """Tests for Card class."""
    
    def test_card_creation(self) -> None:
        """Test card initialization."""
        card = Card("CARD123", "1234", "ACC001")
        assert card.card_number == "CARD123"
        assert card.account_id == "ACC001"
        assert card.is_blocked is False
    
    def test_validate_pin_correct(self) -> None:
        """Test PIN validation with correct PIN."""
        card = Card("CARD123", "1234", "ACC001")
        assert card.validate_pin("1234") is True
    
    def test_validate_pin_incorrect(self) -> None:
        """Test PIN validation with incorrect PIN."""
        card = Card("CARD123", "1234", "ACC001")
        assert card.validate_pin("9999") is False
    
    def test_validate_pin_blocked_card(self) -> None:
        """Test PIN validation on blocked card."""
        card = Card("CARD123", "1234", "ACC001")
        card.block()
        assert card.validate_pin("1234") is False
    
    def test_block_card(self) -> None:
        """Test blocking a card."""
        card = Card("CARD123", "1234", "ACC001")
        card.block()
        assert card.is_blocked is True


class TestTransaction:
    """Tests for Transaction classes."""
    
    def test_deposit_creation(self) -> None:
        """Test deposit transaction creation."""
        deposit = Deposit("TXN001", "ACC001", 100.0)
        assert deposit.transaction_id == "TXN001"
        assert deposit.account_id == "ACC001"
        assert deposit.amount == 100.0
        assert deposit.get_transaction_type() == TransactionType.DEPOSIT
    
    def test_deposit_process(self) -> None:
        """Test deposit processing."""
        account = Account("ACC001", "John Doe", 50.0)
        deposit = Deposit("TXN001", "ACC001", 100.0)
        
        assert deposit.process(account) is True
        assert account.balance == 150.0
    
    def test_withdrawal_creation(self) -> None:
        """Test withdrawal transaction creation."""
        withdrawal = Withdrawal("TXN001", "ACC001", 50.0)
        assert withdrawal.get_transaction_type() == TransactionType.WITHDRAWAL
    
    def test_withdrawal_process_success(self) -> None:
        """Test successful withdrawal processing."""
        account = Account("ACC001", "John Doe", 100.0)
        withdrawal = Withdrawal("TXN001", "ACC001", 50.0)
        
        assert withdrawal.process(account) is True
        assert account.balance == 50.0
    
    def test_withdrawal_process_insufficient(self) -> None:
        """Test withdrawal with insufficient funds."""
        account = Account("ACC001", "John Doe", 30.0)
        withdrawal = Withdrawal("TXN001", "ACC001", 50.0)
        
        assert withdrawal.process(account) is False
        assert account.balance == 30.0


class TestATM:
    """Tests for ATM class."""
    
    def test_atm_creation(self) -> None:
        """Test ATM initialization."""
        atm = ATM("ATM001", "Main Street")
        assert atm._atm_id == "ATM001"
    
    def test_insert_card_success(self) -> None:
        """Test successful card insertion."""
        atm = ATM("ATM001", "Main Street")
        card = Card("CARD123", "1234", "ACC001")
        
        assert atm.insert_card(card) is True
    
    def test_insert_blocked_card(self) -> None:
        """Test inserting blocked card fails."""
        atm = ATM("ATM001", "Main Street")
        card = Card("CARD123", "1234", "ACC001")
        card.block()
        
        assert atm.insert_card(card) is False
    
    def test_insert_card_when_occupied(self) -> None:
        """Test inserting card when ATM occupied fails."""
        atm = ATM("ATM001", "Main Street")
        card1 = Card("CARD123", "1234", "ACC001")
        card2 = Card("CARD456", "5678", "ACC002")
        
        atm.insert_card(card1)
        assert atm.insert_card(card2) is False
    
    def test_enter_pin_correct(self) -> None:
        """Test correct PIN entry."""
        atm = ATM("ATM001", "Main Street")
        card = Card("CARD123", "1234", "ACC001")
        
        atm.insert_card(card)
        assert atm.enter_pin("1234") is True
    
    def test_enter_pin_incorrect(self) -> None:
        """Test incorrect PIN entry."""
        atm = ATM("ATM001", "Main Street")
        card = Card("CARD123", "1234", "ACC001")
        
        atm.insert_card(card)
        assert atm.enter_pin("9999") is False
    
    def test_enter_pin_no_card(self) -> None:
        """Test PIN entry with no card inserted."""
        atm = ATM("ATM001", "Main Street")
        assert atm.enter_pin("1234") is False
    
    def test_check_balance(self) -> None:
        """Test balance check."""
        atm = ATM("ATM001", "Main Street")
        account = Account("ACC001", "John Doe", 500.0)
        atm.add_account(account)
        
        card = Card("CARD123", "1234", "ACC001")
        atm.insert_card(card)
        atm.enter_pin("1234")
        
        assert atm.check_balance() == 500.0
    
    def test_check_balance_not_authenticated(self) -> None:
        """Test balance check without authentication."""
        atm = ATM("ATM001", "Main Street")
        account = Account("ACC001", "John Doe", 500.0)
        atm.add_account(account)
        
        card = Card("CARD123", "1234", "ACC001")
        atm.insert_card(card)
        # Not entering PIN
        
        assert atm.check_balance() is None
    
    def test_deposit_cash(self) -> None:
        """Test cash deposit."""
        atm = ATM("ATM001", "Main Street")
        account = Account("ACC001", "John Doe", 100.0)
        atm.add_account(account)
        
        card = Card("CARD123", "1234", "ACC001")
        atm.insert_card(card)
        atm.enter_pin("1234")
        
        assert atm.deposit_cash(50.0) is True
        assert account.balance == 150.0
        assert len(account.get_transaction_history()) == 1
    
    def test_withdraw_cash(self) -> None:
        """Test cash withdrawal."""
        atm = ATM("ATM001", "Main Street")
        account = Account("ACC001", "John Doe", 100.0)
        atm.add_account(account)
        
        card = Card("CARD123", "1234", "ACC001")
        atm.insert_card(card)
        atm.enter_pin("1234")
        
        assert atm.withdraw_cash(30.0) is True
        assert account.balance == 70.0
    
    def test_withdraw_insufficient_funds(self) -> None:
        """Test withdrawal with insufficient funds."""
        atm = ATM("ATM001", "Main Street")
        account = Account("ACC001", "John Doe", 50.0)
        atm.add_account(account)
        
        card = Card("CARD123", "1234", "ACC001")
        atm.insert_card(card)
        atm.enter_pin("1234")
        
        assert atm.withdraw_cash(100.0) is False
        assert account.balance == 50.0
    
    def test_eject_card(self) -> None:
        """Test card ejection."""
        atm = ATM("ATM001", "Main Street")
        card = Card("CARD123", "1234", "ACC001")
        
        atm.insert_card(card)
        ejected = atm.eject_card()
        
        assert ejected == card
        assert atm.check_balance() is None  # Session ended
    
    def test_eject_card_no_card(self) -> None:
        """Test eject when no card inserted."""
        atm = ATM("ATM001", "Main Street")
        assert atm.eject_card() is None
