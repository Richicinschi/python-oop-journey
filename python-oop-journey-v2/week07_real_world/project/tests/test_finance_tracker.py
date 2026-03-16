"""Comprehensive tests for Personal Finance Tracker.

Tests cover domain models, repositories, and services.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from week07_real_world.project.reference_solution.account import (
    Account, AccountType, create_account
)
from week07_real_world.project.reference_solution.category import (
    Category, CategoryType, create_category, get_default_categories
)
from week07_real_world.project.reference_solution.transaction import (
    Transaction, TransactionType, Transfer, create_transaction, create_transfer
)
from week07_real_world.project.reference_solution.budget import (
    Budget, BudgetPeriod, BudgetAlert, create_budget
)
from week07_real_world.project.reference_solution.report import (
    MonthlySummary, CategoryBreakdown, AccountBalanceHistory, BudgetReport,
    format_currency, generate_spending_trend, generate_text_report, calculate_running_balance
)
from week07_real_world.project.reference_solution.repositories import (
    AccountRepository, TransactionRepository, CategoryRepository, BudgetRepository,
    InMemoryRepository
)
from week07_real_world.project.reference_solution.services import (
    FinanceService, BudgetService, MonthlySummary as ServiceMonthlySummary
)


# =============================================================================
# Account Tests
# =============================================================================

class TestAccount:
    """Tests for Account domain model."""
    
    def test_account_creation(self) -> None:
        """Test basic account creation."""
        account = Account(name="Test Account", account_type=AccountType.CHECKING, balance=100.0)
        assert account.name == "Test Account"
        assert account.account_type == AccountType.CHECKING
        assert account.balance == 100.0
        assert account.currency == "USD"
        assert account.is_active is True
    
    def test_account_creation_with_currency(self) -> None:
        """Test account creation with non-default currency."""
        account = Account(name="Euro Account", account_type=AccountType.SAVINGS, balance=500.0, currency="EUR")
        assert account.currency == "EUR"
    
    def test_account_creation_empty_name_raises(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Account(name="", account_type=AccountType.CHECKING)
    
    def test_account_creation_negative_balance_for_non_credit_raises(self) -> None:
        """Test that negative balance raises error for non-credit accounts."""
        with pytest.raises(ValueError, match="cannot have negative balance"):
            Account(name="Test", account_type=AccountType.CHECKING, balance=-100.0)
    
    def test_account_creation_negative_balance_for_credit_allowed(self) -> None:
        """Test that negative balance is allowed for credit accounts."""
        account = Account(name="Credit Card", account_type=AccountType.CREDIT, balance=-500.0)
        assert account.balance == -500.0
    
    def test_account_deposit_checking(self) -> None:
        """Test deposit into checking account."""
        account = Account(name="Checking", account_type=AccountType.CHECKING, balance=100.0)
        result = account.deposit(50.0)
        assert result is True
        assert account.balance == 150.0
    
    def test_account_deposit_credit_reduces_balance(self) -> None:
        """Test deposit into credit account reduces balance owed."""
        account = Account(name="Credit", account_type=AccountType.CREDIT, balance=500.0)
        result = account.deposit(100.0)
        assert result is True
        assert account.balance == 400.0
    
    def test_account_deposit_zero_or_negative_fails(self) -> None:
        """Test that deposit with non-positive amount fails."""
        account = Account(name="Checking", account_type=AccountType.CHECKING, balance=100.0)
        assert account.deposit(0) is False
        assert account.deposit(-10) is False
        assert account.balance == 100.0
    
    def test_account_withdraw_checking_sufficient_funds(self) -> None:
        """Test successful withdrawal from checking account."""
        account = Account(name="Checking", account_type=AccountType.CHECKING, balance=100.0)
        result = account.withdraw(50.0)
        assert result is True
        assert account.balance == 50.0
    
    def test_account_withdraw_checking_insufficient_funds(self) -> None:
        """Test withdrawal failure with insufficient funds."""
        account = Account(name="Checking", account_type=AccountType.CHECKING, balance=50.0)
        result = account.withdraw(100.0)
        assert result is False
        assert account.balance == 50.0
    
    def test_account_withdraw_credit_always_succeeds(self) -> None:
        """Test that credit withdrawals always succeed."""
        account = Account(name="Credit", account_type=AccountType.CREDIT, balance=0.0)
        result = account.withdraw(1000.0)
        assert result is True
        assert account.balance == 1000.0
    
    def test_account_can_withdraw(self) -> None:
        """Test can_withdraw check method."""
        account = Account(name="Checking", account_type=AccountType.CHECKING, balance=100.0)
        assert account.can_withdraw(50.0) is True
        assert account.can_withdraw(100.0) is True
        assert account.can_withdraw(101.0) is False
        assert account.can_withdraw(-10.0) is False
    
    def test_account_to_dict(self) -> None:
        """Test account serialization to dict."""
        account = Account(name="Test", account_type=AccountType.SAVINGS, balance=1000.0)
        data = account.to_dict()
        assert data["name"] == "Test"
        assert data["account_type"] == "SAVINGS"
        assert data["balance"] == 1000.0
        assert "id" in data
        assert "created_at" in data
    
    def test_account_from_dict(self) -> None:
        """Test account deserialization from dict."""
        original = Account(name="Test", account_type=AccountType.INVESTMENT, balance=5000.0)
        data = original.to_dict()
        restored = Account.from_dict(data)
        assert restored.name == original.name
        assert restored.account_type == original.account_type
        assert restored.balance == original.balance
        assert restored.id == original.id


class TestAccountFactory:
    """Tests for account factory function."""
    
    def test_create_account(self) -> None:
        """Test factory function creates account correctly."""
        account = create_account("My Checking", AccountType.CHECKING, 500.0, "USD")
        assert account.name == "My Checking"
        assert account.account_type == AccountType.CHECKING
        assert account.balance == 500.0
    
    def test_create_account_empty_name_raises(self) -> None:
        """Test factory with empty name raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            create_account("", AccountType.CHECKING)


# =============================================================================
# Category Tests
# =============================================================================

class TestCategory:
    """Tests for Category domain model."""
    
    def test_category_creation(self) -> None:
        """Test basic category creation."""
        category = Category(name="Groceries", type=CategoryType.EXPENSE, color="#FF5733")
        assert category.name == "Groceries"
        assert category.type == CategoryType.EXPENSE
        assert category.color == "#FF5733"
        assert category.is_active is True
    
    def test_category_creation_empty_name_raises(self) -> None:
        """Test that empty category name raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Category(name="", type=CategoryType.EXPENSE)
    
    def test_category_is_income(self) -> None:
        """Test is_income method."""
        income_cat = Category(name="Salary", type=CategoryType.INCOME)
        expense_cat = Category(name="Food", type=CategoryType.EXPENSE)
        assert income_cat.is_income() is True
        assert income_cat.is_expense() is False
        assert expense_cat.is_income() is False
        assert expense_cat.is_expense() is True
    
    def test_category_to_dict(self) -> None:
        """Test category serialization."""
        category = Category(name="Test", type=CategoryType.INCOME)
        data = category.to_dict()
        assert data["name"] == "Test"
        assert data["type"] == "INCOME"
        assert "id" in data
    
    def test_category_from_dict(self) -> None:
        """Test category deserialization."""
        original = Category(name="Test", type=CategoryType.EXPENSE, color="#FFF")
        data = original.to_dict()
        restored = Category.from_dict(data)
        assert restored.name == original.name
        assert restored.type == original.type
        assert restored.color == original.color


class TestCategoryFactory:
    """Tests for category factory functions."""
    
    def test_create_category(self) -> None:
        """Test category factory function."""
        category = create_category("Utilities", CategoryType.EXPENSE, "#0000FF", "bolt")
        assert category.name == "Utilities"
        assert category.color == "#0000FF"
        assert category.icon == "bolt"
    
    def test_get_default_categories(self) -> None:
        """Test default categories are returned."""
        categories = get_default_categories()
        assert len(categories) >= 10
        income_cats = [c for c in categories if c.type == CategoryType.INCOME]
        expense_cats = [c for c in categories if c.type == CategoryType.EXPENSE]
        assert len(income_cats) >= 3
        assert len(expense_cats) >= 5


# =============================================================================
# Transaction Tests
# =============================================================================

class TestTransaction:
    """Tests for Transaction domain model."""
    
    def test_transaction_creation(self) -> None:
        """Test basic transaction creation."""
        tx = Transaction(
            account_id="acc-1",
            category_id="cat-1",
            amount=100.0,
            type=TransactionType.EXPENSE,
            description="Test purchase"
        )
        assert tx.account_id == "acc-1"
        assert tx.amount == 100.0
        assert tx.type == TransactionType.EXPENSE
        assert tx.description == "Test purchase"
    
    def test_transaction_creation_negative_amount_raises(self) -> None:
        """Test that negative amount raises error."""
        with pytest.raises(ValueError, match="must be positive"):
            Transaction(account_id="acc-1", category_id="cat-1", amount=-10.0, type=TransactionType.EXPENSE)
    
    def test_transaction_creation_zero_amount_raises(self) -> None:
        """Test that zero amount raises error."""
        with pytest.raises(ValueError, match="must be positive"):
            Transaction(account_id="acc-1", category_id="cat-1", amount=0, type=TransactionType.EXPENSE)
    
    def test_transaction_creation_missing_account_raises(self) -> None:
        """Test that missing account_id raises error."""
        with pytest.raises(ValueError, match="Account ID is required"):
            Transaction(account_id="", category_id="cat-1", amount=10.0, type=TransactionType.EXPENSE)
    
    def test_transaction_type_checks(self) -> None:
        """Test type check methods."""
        income = Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.INCOME)
        expense = Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.EXPENSE)
        transfer = Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.TRANSFER)
        
        assert income.is_income() is True
        assert income.is_expense() is False
        assert expense.is_expense() is True
        assert transfer.is_transfer() is True
    
    def test_transaction_signed_amount(self) -> None:
        """Test signed amount calculation."""
        income = Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.INCOME)
        expense = Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.EXPENSE)
        
        assert income.signed_amount() == 100.0
        assert expense.signed_amount() == -100.0
    
    def test_transaction_to_dict(self) -> None:
        """Test transaction serialization."""
        tx = Transaction(account_id="a", category_id="c", amount=50.0, type=TransactionType.EXPENSE)
        data = tx.to_dict()
        assert data["amount"] == 50.0
        assert data["type"] == "EXPENSE"
        assert "id" in data
    
    def test_transaction_from_dict(self) -> None:
        """Test transaction deserialization."""
        original = Transaction(
            account_id="a", category_id="c", amount=50.0, type=TransactionType.EXPENSE,
            tags=["food", "groceries"]
        )
        data = original.to_dict()
        restored = Transaction.from_dict(data)
        assert restored.amount == original.amount
        assert restored.tags == original.tags


class TestTransfer:
    """Tests for Transfer domain model."""
    
    def test_transfer_creation(self) -> None:
        """Test transfer creation."""
        transfer = Transfer(from_account_id="acc-1", to_account_id="acc-2", amount=100.0)
        assert transfer.from_account_id == "acc-1"
        assert transfer.to_account_id == "acc-2"
        assert transfer.amount == 100.0
    
    def test_transfer_same_account_raises(self) -> None:
        """Test that transfer to same account raises error."""
        with pytest.raises(ValueError, match="same account"):
            Transfer(from_account_id="acc-1", to_account_id="acc-1", amount=100.0)
    
    def test_transfer_negative_amount_raises(self) -> None:
        """Test that negative transfer amount raises error."""
        with pytest.raises(ValueError, match="must be positive"):
            Transfer(from_account_id="acc-1", to_account_id="acc-2", amount=-100.0)
    
    def test_transfer_create_transactions(self) -> None:
        """Test that transfer creates two transactions."""
        transfer = Transfer(from_account_id="acc-1", to_account_id="acc-2", amount=100.0, description="Test transfer")
        outgoing, incoming = transfer.create_transactions("transfer-cat")
        
        assert outgoing.account_id == "acc-1"
        assert outgoing.to_account_id == "acc-2"
        assert outgoing.amount == 100.0
        assert outgoing.type == TransactionType.TRANSFER
        
        assert incoming.account_id == "acc-2"
        assert incoming.to_account_id == "acc-1"
        assert incoming.amount == 100.0


class TestTransactionFactory:
    """Tests for transaction factory functions."""
    
    def test_create_transaction(self) -> None:
        """Test transaction factory."""
        tx = create_transaction("acc-1", "cat-1", 50.0, TransactionType.EXPENSE, description="Test")
        assert tx.amount == 50.0
        assert tx.type == TransactionType.EXPENSE
    
    def test_create_transfer_factory(self) -> None:
        """Test transfer factory."""
        transfer = create_transfer("acc-1", "acc-2", 100.0, description="Test transfer")
        assert transfer.amount == 100.0
        assert transfer.from_account_id == "acc-1"


# =============================================================================
# Budget Tests
# =============================================================================

class TestBudget:
    """Tests for Budget domain model."""
    
    def test_budget_creation(self) -> None:
        """Test basic budget creation."""
        budget = Budget(category_id="cat-1", amount=500.0, period=BudgetPeriod.MONTHLY)
        assert budget.category_id == "cat-1"
        assert budget.amount == 500.0
        assert budget.period == BudgetPeriod.MONTHLY
        assert budget.alert_threshold == 80.0
    
    def test_budget_creation_invalid_amount_raises(self) -> None:
        """Test that non-positive amount raises error."""
        with pytest.raises(ValueError, match="must be positive"):
            Budget(category_id="cat-1", amount=0)
    
    def test_budget_creation_invalid_threshold_raises(self) -> None:
        """Test that invalid threshold raises error."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            Budget(category_id="cat-1", amount=100.0, alert_threshold=150.0)
    
    def test_budget_get_period_dates_monthly(self) -> None:
        """Test monthly period date calculation."""
        budget = Budget(category_id="cat-1", amount=100.0, period=BudgetPeriod.MONTHLY)
        start, end = budget.get_period_dates()
        assert start.day == 1
        assert end >= start
    
    def test_budget_is_alert_triggered(self) -> None:
        """Test alert threshold detection."""
        budget = Budget(category_id="cat-1", amount=100.0, alert_threshold=80.0)
        assert budget.is_alert_triggered(79.0) is False
        assert budget.is_alert_triggered(80.0) is True
        assert budget.is_alert_triggered(100.0) is True
    
    def test_budget_get_remaining(self) -> None:
        """Test remaining budget calculation."""
        budget = Budget(category_id="cat-1", amount=100.0)
        assert budget.get_remaining(50.0) == 50.0
        assert budget.get_remaining(100.0) == 0.0
        assert budget.get_remaining(150.0) == -50.0
    
    def test_budget_get_utilization_percentage(self) -> None:
        """Test utilization percentage calculation."""
        budget = Budget(category_id="cat-1", amount=100.0)
        assert budget.get_utilization_percentage(50.0) == 50.0
        assert budget.get_utilization_percentage(100.0) == 100.0
        assert budget.get_utilization_percentage(150.0) == 150.0
    
    def test_budget_to_dict(self) -> None:
        """Test budget serialization."""
        budget = Budget(category_id="cat-1", amount=100.0)
        data = budget.to_dict()
        assert data["amount"] == 100.0
        assert data["period"] == "MONTHLY"
    
    def test_budget_from_dict(self) -> None:
        """Test budget deserialization."""
        original = Budget(category_id="cat-1", amount=200.0, period=BudgetPeriod.WEEKLY)
        data = original.to_dict()
        restored = Budget.from_dict(data)
        assert restored.amount == original.amount
        assert restored.period == original.period


class TestBudgetAlert:
    """Tests for BudgetAlert."""
    
    def test_budget_alert_is_critical(self) -> None:
        """Test critical alert detection."""
        alert_under = BudgetAlert(
            budget_id="b-1", category_id="c-1", category_name="Food",
            budget_amount=100.0, spent_amount=80.0, remaining_amount=20.0,
            utilization_percentage=80.0, message="Warning"
        )
        alert_over = BudgetAlert(
            budget_id="b-1", category_id="c-1", category_name="Food",
            budget_amount=100.0, spent_amount=120.0, remaining_amount=-20.0,
            utilization_percentage=120.0, message="Over budget!"
        )
        assert alert_under.is_critical() is False
        assert alert_over.is_critical() is True


class TestBudgetFactory:
    """Tests for budget factory."""
    
    def test_create_budget(self) -> None:
        """Test budget factory function."""
        budget = create_budget("cat-1", 500.0, BudgetPeriod.MONTHLY)
        assert budget.amount == 500.0
        assert budget.period == BudgetPeriod.MONTHLY


# =============================================================================
# Report Tests
# =============================================================================

class TestReportModels:
    """Tests for report data models."""
    
    def test_monthly_summary_is_profitable(self) -> None:
        """Test profit detection in monthly summary."""
        profitable = MonthlySummary(2024, 1, total_income=5000.0, total_expenses=3000.0, net_flow=2000.0)
        deficit = MonthlySummary(2024, 1, total_income=3000.0, total_expenses=5000.0, net_flow=-2000.0)
        assert profitable.is_profitable() is True
        assert deficit.is_profitable() is False
    
    def test_monthly_summary_savings_rate(self) -> None:
        """Test savings rate calculation."""
        summary = MonthlySummary(2024, 1, total_income=5000.0, net_flow=1000.0)
        assert summary.savings_rate() == 20.0
        
        zero_income = MonthlySummary(2024, 1, total_income=0.0, net_flow=0.0)
        assert zero_income.savings_rate() == 0.0
    
    def test_budget_report_get_status(self) -> None:
        """Test budget status determination."""
        today = date.today()
        under = BudgetReport("b-1", "Food", 100.0, 50.0, 50.0, 50.0, today, today, True)
        near = BudgetReport("b-1", "Food", 100.0, 85.0, 15.0, 85.0, today, today, True)
        over = BudgetReport("b-1", "Food", 100.0, 110.0, -10.0, 110.0, today, today, False)
        
        assert under.get_status() == "under_budget"
        assert near.get_status() == "near_limit"
        assert over.get_status() == "over_budget"


class TestReportUtilities:
    """Tests for report utility functions."""
    
    def test_format_currency_usd(self) -> None:
        """Test USD currency formatting."""
        assert format_currency(100.50, "USD") == "$100.50"
        assert format_currency(1000.0, "USD") == "$1,000.00"
    
    def test_format_currency_eur(self) -> None:
        """Test EUR currency formatting."""
        assert format_currency(100.50, "EUR") == "€100.50"
    
    def test_generate_spending_trend(self) -> None:
        """Test spending trend calculation."""
        data = [
            (2024, 1, 1000.0),
            (2024, 2, 1200.0),
            (2024, 3, 1100.0)
        ]
        trend = generate_spending_trend(data)
        assert len(trend) == 3
        assert trend[0][3] == 0.0  # First month has no change
        assert trend[1][3] == 20.0  # 20% increase
        assert trend[2][3] == -8.33  # Approximate decrease
    
    def test_generate_text_report(self) -> None:
        """Test text report generation."""
        summary = MonthlySummary(
            year=2024, month=1,
            total_income=5000.0, total_expenses=3000.0,
            net_flow=2000.0, transaction_count=25,
            top_expense_categories=[("Food", 800.0), ("Rent", 1500.0)]
        )
        report = generate_text_report(summary)
        assert "2024-01" in report
        assert "$5,000.00" in report
        assert "Profitable" in report
        assert "Food" in report


# =============================================================================
# Repository Tests
# =============================================================================

class TestInMemoryRepository:
    """Tests for base repository implementation."""
    
    def test_add_and_get(self) -> None:
        """Test adding and retrieving items."""
        repo = InMemoryRepository[Account]()
        account = Account(name="Test", account_type=AccountType.CHECKING)
        repo.add(account)
        
        retrieved = repo.get(account.id)
        assert retrieved is not None
        assert retrieved.name == "Test"
    
    def test_get_nonexistent_returns_none(self) -> None:
        """Test that getting nonexistent item returns None."""
        repo = InMemoryRepository[Account]()
        assert repo.get("nonexistent") is None
    
    def test_get_all(self) -> None:
        """Test getting all items."""
        repo = InMemoryRepository[Account]()
        repo.add(Account(name="A1", account_type=AccountType.CHECKING))
        repo.add(Account(name="A2", account_type=AccountType.SAVINGS))
        
        all_items = repo.get_all()
        assert len(all_items) == 2
    
    def test_update(self) -> None:
        """Test updating an item."""
        repo = InMemoryRepository[Account]()
        account = Account(name="Old", account_type=AccountType.CHECKING)
        repo.add(account)
        
        account.name = "New"
        repo.update(account)
        
        retrieved = repo.get(account.id)
        assert retrieved.name == "New"
    
    def test_update_nonexistent_raises(self) -> None:
        """Test updating nonexistent item raises error."""
        repo = InMemoryRepository[Account]()
        account = Account(name="Test", account_type=AccountType.CHECKING)
        with pytest.raises(KeyError):
            repo.update(account)
    
    def test_delete(self) -> None:
        """Test deleting an item."""
        repo = InMemoryRepository[Account]()
        account = Account(name="Test", account_type=AccountType.CHECKING)
        repo.add(account)
        
        assert repo.delete(account.id) is True
        assert repo.get(account.id) is None
    
    def test_delete_nonexistent_returns_false(self) -> None:
        """Test deleting nonexistent item returns False."""
        repo = InMemoryRepository[Account]()
        assert repo.delete("nonexistent") is False
    
    def test_clear(self) -> None:
        """Test clearing all items."""
        repo = InMemoryRepository[Account]()
        repo.add(Account(name="Test", account_type=AccountType.CHECKING))
        repo.clear()
        assert repo.count() == 0


class TestAccountRepository:
    """Tests for AccountRepository."""
    
    def test_get_by_type(self) -> None:
        """Test filtering accounts by type."""
        repo = AccountRepository()
        repo.add(Account(name="Checking", account_type=AccountType.CHECKING))
        repo.add(Account(name="Savings", account_type=AccountType.SAVINGS))
        repo.add(Account(name="Credit", account_type=AccountType.CREDIT))
        
        checking_accounts = repo.get_by_type(AccountType.CHECKING)
        assert len(checking_accounts) == 1
        assert checking_accounts[0].name == "Checking"
    
    def test_get_active(self) -> None:
        """Test getting only active accounts."""
        repo = AccountRepository()
        active = Account(name="Active", account_type=AccountType.CHECKING, is_active=True)
        inactive = Account(name="Inactive", account_type=AccountType.CHECKING, is_active=False)
        repo.add(active)
        repo.add(inactive)
        
        active_accounts = repo.get_active()
        assert len(active_accounts) == 1
        assert active_accounts[0].name == "Active"
    
    def test_get_total_balance(self) -> None:
        """Test total balance calculation."""
        repo = AccountRepository()
        repo.add(Account(name="Checking", account_type=AccountType.CHECKING, balance=1000.0))
        repo.add(Account(name="Savings", account_type=AccountType.SAVINGS, balance=2000.0))
        repo.add(Account(name="Credit", account_type=AccountType.CREDIT, balance=500.0))
        
        # Credit balance should be subtracted
        assert repo.get_total_balance() == 2500.0
    
    def test_save_and_load_from_file(self) -> None:
        """Test file persistence."""
        import tempfile
        import os
        
        repo = AccountRepository()
        repo.add(Account(name="Test", account_type=AccountType.CHECKING, balance=1000.0))
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            filepath = os.path.join(tmp_dir, "accounts.json")
            repo.save_to_file(filepath)
            
            new_repo = AccountRepository()
            new_repo.load_from_file(filepath)
            
            assert new_repo.count() == 1
            account = new_repo.get_all()[0]
            assert account.name == "Test"
            assert account.balance == 1000.0


class TestTransactionRepository:
    """Tests for TransactionRepository."""
    
    def test_get_by_account(self) -> None:
        """Test filtering by account."""
        repo = TransactionRepository()
        repo.add(Transaction(account_id="acc-1", category_id="cat-1", amount=100.0, type=TransactionType.EXPENSE))
        repo.add(Transaction(account_id="acc-2", category_id="cat-1", amount=50.0, type=TransactionType.EXPENSE))
        
        acc1_transactions = repo.get_by_account("acc-1")
        assert len(acc1_transactions) == 1
    
    def test_get_by_category(self) -> None:
        """Test filtering by category."""
        repo = TransactionRepository()
        repo.add(Transaction(account_id="acc-1", category_id="cat-1", amount=100.0, type=TransactionType.EXPENSE))
        repo.add(Transaction(account_id="acc-1", category_id="cat-2", amount=50.0, type=TransactionType.EXPENSE))
        
        cat1_transactions = repo.get_by_category("cat-1")
        assert len(cat1_transactions) == 1
    
    def test_get_by_date_range(self) -> None:
        """Test filtering by date range."""
        repo = TransactionRepository()
        repo.add(Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.EXPENSE, date=date(2024, 1, 15)))
        repo.add(Transaction(account_id="a", category_id="c", amount=50.0, type=TransactionType.EXPENSE, date=date(2024, 2, 15)))
        
        jan_transactions = repo.get_by_date_range(date(2024, 1, 1), date(2024, 1, 31))
        assert len(jan_transactions) == 1
    
    def test_get_by_type(self) -> None:
        """Test filtering by transaction type."""
        repo = TransactionRepository()
        repo.add(Transaction(account_id="a", category_id="c", amount=100.0, type=TransactionType.INCOME))
        repo.add(Transaction(account_id="a", category_id="c", amount=50.0, type=TransactionType.EXPENSE))
        
        income_transactions = repo.get_by_type(TransactionType.INCOME)
        assert len(income_transactions) == 1
    
    def test_get_total_by_category(self) -> None:
        """Test total calculation by category."""
        repo = TransactionRepository()
        repo.add(Transaction(account_id="a", category_id="cat-1", amount=100.0, type=TransactionType.EXPENSE))
        repo.add(Transaction(account_id="a", category_id="cat-1", amount=50.0, type=TransactionType.EXPENSE))
        repo.add(Transaction(account_id="a", category_id="cat-2", amount=75.0, type=TransactionType.EXPENSE))
        
        assert repo.get_total_by_category("cat-1") == 150.0


class TestCategoryRepository:
    """Tests for CategoryRepository."""
    
    def test_get_by_type(self) -> None:
        """Test filtering by category type."""
        repo = CategoryRepository()
        repo.add(Category(name="Salary", type=CategoryType.INCOME))
        repo.add(Category(name="Food", type=CategoryType.EXPENSE))
        
        income_cats = repo.get_by_type(CategoryType.INCOME)
        assert len(income_cats) == 1
        assert income_cats[0].name == "Salary"
    
    def test_get_income_and_expense_categories(self) -> None:
        """Test convenience methods for category types."""
        repo = CategoryRepository()
        repo.add(Category(name="Salary", type=CategoryType.INCOME))
        repo.add(Category(name="Food", type=CategoryType.EXPENSE))
        
        assert len(repo.get_income_categories()) == 1
        assert len(repo.get_expense_categories()) == 1
    
    def test_find_by_name(self) -> None:
        """Test finding category by name."""
        repo = CategoryRepository()
        repo.add(Category(name="Groceries", type=CategoryType.EXPENSE))
        
        found = repo.find_by_name("groceries")  # Case insensitive
        assert found is not None
        assert found.name == "Groceries"
        
        not_found = repo.find_by_name("nonexistent")
        assert not_found is None


class TestBudgetRepository:
    """Tests for BudgetRepository."""
    
    def test_get_by_category(self) -> None:
        """Test getting budget by category."""
        repo = BudgetRepository()
        budget = Budget(category_id="cat-1", amount=500.0)
        repo.add(budget)
        
        found = repo.get_by_category("cat-1")
        assert found is not None
        assert found.amount == 500.0
    
    def test_get_active_budgets(self) -> None:
        """Test getting only active budgets."""
        repo = BudgetRepository()
        repo.add(Budget(category_id="cat-1", amount=100.0, is_active=True))
        repo.add(Budget(category_id="cat-2", amount=200.0, is_active=False))
        
        active = repo.get_active_budgets()
        assert len(active) == 1
    
    def test_get_by_period(self) -> None:
        """Test filtering by budget period."""
        repo = BudgetRepository()
        repo.add(Budget(category_id="cat-1", amount=100.0, period=BudgetPeriod.MONTHLY))
        repo.add(Budget(category_id="cat-2", amount=200.0, period=BudgetPeriod.WEEKLY))
        
        monthly = repo.get_by_period(BudgetPeriod.MONTHLY)
        assert len(monthly) == 1


# =============================================================================
# Service Tests
# =============================================================================

class TestFinanceService:
    """Tests for FinanceService."""
    
    def setup_method(self) -> None:
        """Set up fresh repositories for each test."""
        self.account_repo = AccountRepository()
        self.transaction_repo = TransactionRepository()
        self.category_repo = CategoryRepository()
        self.service = FinanceService(
            self.account_repo, self.transaction_repo, self.category_repo
        )
    
    def test_create_account(self) -> None:
        """Test account creation through service."""
        account = self.service.create_account("My Checking", "checking", 1000.0)
        assert account.name == "My Checking"
        assert account.balance == 1000.0
    
    def test_get_account(self) -> None:
        """Test account retrieval through service."""
        created = self.service.create_account("Test", "checking")
        retrieved = self.service.get_account(created.id)
        assert retrieved is not None
        assert retrieved.name == "Test"
    
    def test_create_category(self) -> None:
        """Test category creation through service."""
        category = self.service.create_category("Food", "expense", "#FF0000")
        assert category.name == "Food"
        assert category.type == CategoryType.EXPENSE
    
    def test_find_category_by_name(self) -> None:
        """Test category lookup by name."""
        self.service.create_category("Utilities", "expense")
        found = self.service.find_category_by_name("utilities")
        assert found is not None
    
    def test_setup_default_categories(self) -> None:
        """Test setting up default categories."""
        added = self.service.setup_default_categories()
        assert len(added) > 0
        # Should not duplicate
        added_again = self.service.setup_default_categories()
        assert len(added_again) == 0
    
    def test_record_income_transaction(self) -> None:
        """Test recording income transaction."""
        account = self.service.create_account("Checking", "checking", 1000.0)
        category = self.service.create_category("Salary", "income")
        
        tx = self.service.record_transaction(
            account.id, category.id, 500.0, "income", "Paycheck"
        )
        
        assert tx.amount == 500.0
        assert tx.type == TransactionType.INCOME
        
        # Account balance should be updated
        updated_account = self.service.get_account(account.id)
        assert updated_account.balance == 1500.0
    
    def test_record_expense_transaction(self) -> None:
        """Test recording expense transaction."""
        account = self.service.create_account("Checking", "checking", 1000.0)
        category = self.service.create_category("Food", "expense")
        
        tx = self.service.record_transaction(
            account.id, category.id, 100.0, "expense", "Groceries"
        )
        
        assert tx.amount == 100.0
        assert tx.type == TransactionType.EXPENSE
        
        # Account balance should be updated
        updated_account = self.service.get_account(account.id)
        assert updated_account.balance == 900.0
    
    def test_record_transaction_insufficient_funds(self) -> None:
        """Test that expense with insufficient funds raises error."""
        account = self.service.create_account("Checking", "checking", 50.0)
        category = self.service.create_category("Food", "expense")
        
        with pytest.raises(ValueError, match="Insufficient funds"):
            self.service.record_transaction(
                account.id, category.id, 100.0, "expense"
            )
    
    def test_transfer_between_accounts(self) -> None:
        """Test transferring between accounts."""
        checking = self.service.create_account("Checking", "checking", 1000.0)
        savings = self.service.create_account("Savings", "savings", 500.0)
        
        outgoing, incoming = self.service.transfer_between_accounts(
            checking.id, savings.id, 200.0, "Monthly savings"
        )
        
        # Check transactions created
        assert outgoing.account_id == checking.id
        assert incoming.account_id == savings.id
        assert outgoing.amount == 200.0
        
        # Check balances updated
        updated_checking = self.service.get_account(checking.id)
        updated_savings = self.service.get_account(savings.id)
        assert updated_checking.balance == 800.0
        assert updated_savings.balance == 700.0
    
    def test_generate_monthly_summary(self) -> None:
        """Test monthly summary generation."""
        account = self.service.create_account("Checking", "checking", 0.0)
        income_cat = self.service.create_category("Salary", "income")
        expense_cat = self.service.create_category("Food", "expense")
        
        # Add transactions
        self.service.record_transaction(account.id, income_cat.id, 5000.0, "income", tx_date=date(2024, 1, 15))
        self.service.record_transaction(account.id, expense_cat.id, 1000.0, "expense", tx_date=date(2024, 1, 10))
        self.service.record_transaction(account.id, expense_cat.id, 500.0, "expense", tx_date=date(2024, 1, 20))
        
        summary = self.service.generate_monthly_summary(2024, 1)
        
        assert summary.total_income == 5000.0
        assert summary.total_expenses == 1500.0
        assert summary.net_flow == 3500.0
        assert summary.transaction_count == 3
    
    def test_generate_category_breakdown(self) -> None:
        """Test category breakdown generation."""
        account = self.service.create_account("Checking", "checking", 5000.0)
        food_cat = self.service.create_category("Food", "expense")
        util_cat = self.service.create_category("Utilities", "expense")
        
        self.service.record_transaction(account.id, food_cat.id, 200.0, "expense", tx_date=date(2024, 1, 1))
        self.service.record_transaction(account.id, food_cat.id, 100.0, "expense", tx_date=date(2024, 1, 2))
        self.service.record_transaction(account.id, util_cat.id, 150.0, "expense", tx_date=date(2024, 1, 3))
        
        breakdown = self.service.generate_category_breakdown(
            date(2024, 1, 1), date(2024, 1, 31), "expense"
        )
        
        assert len(breakdown) == 2
        # Should be sorted by amount descending
        assert breakdown[0].total_amount == 300.0  # Food
        assert breakdown[1].total_amount == 150.0  # Utilities
    
    def test_export_transactions_to_csv(self) -> None:
        """Test CSV export functionality."""
        import tempfile
        import os
        
        account = self.service.create_account("Checking", "checking", 1000.0)
        category = self.service.create_category("Food", "expense")
        self.service.record_transaction(account.id, category.id, 50.0, "expense", "Lunch")
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            filepath = os.path.join(tmp_dir, "transactions.csv")
            result = self.service.export_transactions_to_csv(filepath)
            
            assert result is True
            assert os.path.exists(filepath)
            
            # Verify CSV content
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 2  # Header + 1 transaction


class TestBudgetService:
    """Tests for BudgetService."""
    
    def setup_method(self) -> None:
        """Set up fresh repositories for each test."""
        self.budget_repo = BudgetRepository()
        self.category_repo = CategoryRepository()
        self.transaction_repo = TransactionRepository()
        self.service = BudgetService(
            self.budget_repo, self.category_repo, self.transaction_repo
        )
    
    def test_create_budget(self) -> None:
        """Test budget creation through service."""
        category = Category(name="Food", type=CategoryType.EXPENSE)
        self.category_repo.add(category)
        
        budget = self.service.create_budget(category.id, 500.0, "monthly", 80.0)
        
        assert budget.amount == 500.0
        assert budget.period == BudgetPeriod.MONTHLY
    
    def test_calculate_spent_for_budget(self) -> None:
        """Test spending calculation for budget."""
        category = Category(name="Food", type=CategoryType.EXPENSE)
        self.category_repo.add(category)
        
        budget = self.service.create_budget(category.id, 500.0, "monthly")
        
        # Add expense transaction
        self.transaction_repo.add(Transaction(
            account_id="a", category_id=category.id,
            amount=150.0, type=TransactionType.EXPENSE,
            date=date.today()
        ))
        
        spent = self.service.calculate_spent_for_budget(budget)
        assert spent == 150.0
    
    def test_check_budget_alerts(self) -> None:
        """Test budget alert generation."""
        category = Category(name="Food", type=CategoryType.EXPENSE)
        self.category_repo.add(category)
        
        # Create budget with 80% alert threshold
        budget = self.service.create_budget(category.id, 100.0, "monthly", 80.0)
        
        # Add expense at 85% of budget
        self.transaction_repo.add(Transaction(
            account_id="a", category_id=category.id,
            amount=85.0, type=TransactionType.EXPENSE,
            date=date.today()
        ))
        
        alerts = self.service.check_budget_alerts()
        
        assert len(alerts) == 1
        assert alerts[0].utilization_percentage == 85.0
        assert "85.0%" in alerts[0].message
    
    def test_generate_budget_report(self) -> None:
        """Test budget report generation."""
        category = Category(name="Food", type=CategoryType.EXPENSE)
        self.category_repo.add(category)
        
        budget = self.service.create_budget(category.id, 200.0, "monthly")
        
        self.transaction_repo.add(Transaction(
            account_id="a", category_id=category.id,
            amount=100.0, type=TransactionType.EXPENSE,
            date=date.today()
        ))
        
        report = self.service.generate_budget_report(budget.id)
        
        assert report is not None
        assert report.budget_amount == 200.0
        assert report.spent_amount == 100.0
        assert report.remaining_amount == 100.0
        assert report.utilization_percentage == 50.0
        assert report.is_on_track is True


# Test count: 88 tests
