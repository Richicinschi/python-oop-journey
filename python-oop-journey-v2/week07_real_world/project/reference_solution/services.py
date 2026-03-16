"""Service layer for business logic.

Services encapsulate business operations and orchestrate between
repositories and domain models.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

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
from week07_real_world.project.reference_solution.repositories import (
    AccountRepository, TransactionRepository, CategoryRepository, BudgetRepository
)


@dataclass
class MonthlySummary:
    """Summary of financial activity for a month."""
    
    year: int
    month: int
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_flow: float = 0.0
    transaction_count: int = 0
    top_expense_categories: list[tuple[str, float]] = field(default_factory=list)
    
    def is_profitable(self) -> bool:
        """Check if month had positive cash flow."""
        return self.net_flow > 0
    
    def savings_rate(self) -> float:
        """Calculate savings rate as percentage of income."""
        if self.total_income <= 0:
            return 0.0
        return (self.net_flow / self.total_income) * 100


@dataclass
class CategoryBreakdown:
    """Breakdown of spending by category."""
    
    category_id: str
    category_name: str
    total_amount: float
    percentage: float
    transaction_count: int


@dataclass
class BudgetReport:
    """Report on budget performance."""
    
    budget_id: str
    category_name: str
    budget_amount: float
    spent_amount: float
    remaining_amount: float
    utilization_percentage: float
    period_start: date
    period_end: date
    is_on_track: bool
    
    def get_status(self) -> str:
        """Get a status string."""
        if self.utilization_percentage >= 100:
            return "over_budget"
        elif self.utilization_percentage >= 80:
            return "near_limit"
        return "under_budget"


class FinanceService:
    """Main service for personal finance operations.
    
    Orchestrates between repositories and provides high-level
    business operations.
    """
    
    def __init__(
        self,
        account_repo: AccountRepository,
        transaction_repo: TransactionRepository,
        category_repo: CategoryRepository,
        budget_repo: Optional[BudgetRepository] = None
    ) -> None:
        """Initialize the finance service.
        
        Args:
            account_repo: Repository for accounts
            transaction_repo: Repository for transactions
            category_repo: Repository for categories
            budget_repo: Optional repository for budgets
        """
        self._accounts = account_repo
        self._transactions = transaction_repo
        self._categories = category_repo
        self._budgets = budget_repo or BudgetRepository()
    
    # Account operations
    
    def create_account(
        self,
        name: str,
        account_type: str,
        initial_balance: float = 0.0,
        currency: str = "USD"
    ) -> Account:
        """Create a new account.
        
        Args:
            name: Account name
            account_type: Account type string (checking, savings, credit, investment)
            initial_balance: Starting balance
            currency: Currency code
            
        Returns:
            The created account
        """
        acc_type = AccountType[account_type.upper()]
        account = create_account(name, acc_type, initial_balance, currency)
        return self._accounts.add(account)
    
    def get_account(self, account_id: str) -> Optional[Account]:
        """Get an account by ID."""
        return self._accounts.get(account_id)
    
    def get_all_accounts(self) -> list[Account]:
        """Get all accounts."""
        return self._accounts.get_all()
    
    def delete_account(self, account_id: str) -> bool:
        """Delete an account (only if no transactions exist)."""
        transactions = self._transactions.get_by_account(account_id)
        if transactions:
            return False
        return self._accounts.delete(account_id)
    
    # Category operations
    
    def create_category(
        self,
        name: str,
        category_type: str,
        color: Optional[str] = None,
        icon: Optional[str] = None
    ) -> Category:
        """Create a new category."""
        cat_type = CategoryType[category_type.upper()]
        category = create_category(name, cat_type, color, icon)
        return self._categories.add(category)
    
    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by ID."""
        return self._categories.get(category_id)
    
    def find_category_by_name(self, name: str) -> Optional[Category]:
        """Find a category by name."""
        return self._categories.find_by_name(name)
    
    def setup_default_categories(self) -> list[Category]:
        """Add default categories to the system."""
        defaults = get_default_categories()
        added = []
        for category in defaults:
            existing = self._categories.find_by_name(category.name)
            if not existing:
                added.append(self._categories.add(category))
        return added
    
    # Transaction operations
    
    def record_transaction(
        self,
        account_id: str,
        category_id: str,
        amount: float,
        type: str,
        description: str = "",
        tx_date: Optional[date] = None,
        tags: Optional[list[str]] = None
    ) -> Transaction:
        """Record a new transaction.
        
        Args:
            account_id: Account ID
            category_id: Category ID
            amount: Transaction amount
            type: Transaction type (income, expense, transfer)
            description: Optional description
            tx_date: Optional date (defaults to today)
            tags: Optional tags
            
        Returns:
            The created transaction
        """
        tx_type = TransactionType[type.upper()]
        
        # Update account balance
        account = self._accounts.get(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        if tx_type == TransactionType.INCOME:
            account.deposit(amount)
        else:
            if not account.withdraw(amount):
                raise ValueError("Insufficient funds")
        
        self._accounts.update(account)
        
        # Create and store transaction
        transaction = create_transaction(
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            type=tx_type,
            description=description,
            tx_date=tx_date,
            tags=tags
        )
        return self._transactions.add(transaction)
    
    def transfer_between_accounts(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        description: str = "",
        transfer_date: Optional[date] = None
    ) -> tuple[Transaction, Transaction]:
        """Transfer money between two accounts.
        
        Args:
            from_account_id: Source account
            to_account_id: Destination account
            amount: Amount to transfer
            description: Optional description
            transfer_date: Optional date
            
        Returns:
            Tuple of (outgoing_transaction, incoming_transaction)
        """
        # Get or create transfer category
        transfer_cat = self._categories.find_by_name("Transfer")
        if not transfer_cat:
            transfer_cat = self.create_category("Transfer", "expense")
        
        # Create transfer object
        transfer = create_transfer(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            description=description,
            tx_date=transfer_date
        )
        
        # Execute transfer
        outgoing, incoming = transfer.create_transactions(transfer_cat.id)
        
        # Update account balances
        from_account = self._accounts.get(from_account_id)
        to_account = self._accounts.get(to_account_id)
        
        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")
        
        from_account.withdraw(amount)
        to_account.deposit(amount)
        
        self._accounts.update(from_account)
        self._accounts.update(to_account)
        
        # Store transactions
        self._transactions.add(outgoing)
        self._transactions.add(incoming)
        
        return outgoing, incoming
    
    def get_transactions_for_account(self, account_id: str) -> list[Transaction]:
        """Get all transactions for an account."""
        return self._transactions.get_by_account(account_id)
    
    # Report generation
    
    def generate_monthly_summary(self, year: int, month: int) -> MonthlySummary:
        """Generate a monthly summary report."""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        transactions = self._transactions.get_by_date_range(start_date, end_date)
        
        total_income = 0.0
        total_expenses = 0.0
        expense_by_category: dict[str, float] = {}
        
        for tx in transactions:
            category = self._categories.get(tx.category_id)
            category_name = category.name if category else "Unknown"
            
            if tx.type == TransactionType.INCOME:
                total_income += tx.amount
            elif tx.type == TransactionType.EXPENSE:
                total_expenses += tx.amount
                expense_by_category[category_name] = expense_by_category.get(category_name, 0.0) + tx.amount
        
        # Sort categories by amount
        top_expenses = sorted(
            expense_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return MonthlySummary(
            year=year,
            month=month,
            total_income=total_income,
            total_expenses=total_expenses,
            net_flow=total_income - total_expenses,
            transaction_count=len(transactions),
            top_expense_categories=top_expenses
        )
    
    def generate_category_breakdown(
        self,
        start_date: date,
        end_date: date,
        category_type: Optional[str] = None
    ) -> list[CategoryBreakdown]:
        """Generate spending breakdown by category."""
        transactions = self._transactions.get_by_date_range(start_date, end_date)
        
        # Filter by type if specified
        if category_type:
            cat_type = CategoryType[category_type.upper()]
            filtered_transactions = []
            for tx in transactions:
                category = self._categories.get(tx.category_id)
                if category and category.type == cat_type:
                    filtered_transactions.append(tx)
            transactions = filtered_transactions
        
        # Aggregate by category
        category_totals: dict[str, tuple[str, float, int]] = {}
        total_amount = 0.0
        
        for tx in transactions:
            category = self._categories.get(tx.category_id)
            if not category:
                continue
            
            cat_id = category.id
            cat_name = category.name
            
            if cat_id not in category_totals:
                category_totals[cat_id] = (cat_name, 0.0, 0)
            
            current = category_totals[cat_id]
            category_totals[cat_id] = (
                current[0],
                current[1] + tx.amount,
                current[2] + 1
            )
            total_amount += tx.amount
        
        # Create breakdowns
        breakdowns = []
        for cat_id, (name, amount, count) in category_totals.items():
            percentage = (amount / total_amount * 100) if total_amount > 0 else 0.0
            breakdowns.append(CategoryBreakdown(
                category_id=cat_id,
                category_name=name,
                total_amount=amount,
                percentage=round(percentage, 2),
                transaction_count=count
            ))
        
        # Sort by amount descending
        breakdowns.sort(key=lambda x: x.total_amount, reverse=True)
        return breakdowns
    
    def export_transactions_to_csv(
        self,
        filepath: str | Path,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> bool:
        """Export transactions to CSV."""
        if start_date and end_date:
            transactions = self._transactions.get_by_date_range(start_date, end_date)
        else:
            transactions = self._transactions.get_all()
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date', 'Account', 'Category', 'Type', 'Amount', 'Description', 'Tags'
            ])
            
            for tx in transactions:
                account = self._accounts.get(tx.account_id)
                category = self._categories.get(tx.category_id)
                
                writer.writerow([
                    tx.date.isoformat(),
                    account.name if account else 'Unknown',
                    category.name if category else 'Unknown',
                    tx.type.name,
                    tx.amount,
                    tx.description,
                    ','.join(tx.tags)
                ])
        
        return True


class BudgetService:
    """Service for budget operations."""
    
    def __init__(
        self,
        budget_repo: BudgetRepository,
        category_repo: CategoryRepository,
        transaction_repo: TransactionRepository
    ) -> None:
        """Initialize the budget service."""
        self._budgets = budget_repo
        self._categories = category_repo
        self._transactions = transaction_repo
    
    def create_budget(
        self,
        category_id: str,
        amount: float,
        period: str = "monthly",
        alert_threshold: float = 80.0
    ) -> Budget:
        """Create a new budget."""
        budget_period = BudgetPeriod[period.upper()]
        budget = create_budget(
            category_id=category_id,
            amount=amount,
            period=budget_period,
            alert_threshold=alert_threshold
        )
        return self._budgets.add(budget)
    
    def get_budget(self, budget_id: str) -> Optional[Budget]:
        """Get a budget by ID."""
        return self._budgets.get(budget_id)
    
    def get_budget_for_category(self, category_id: str) -> Optional[Budget]:
        """Get the active budget for a category."""
        return self._budgets.get_by_category(category_id)
    
    def calculate_spent_for_budget(self, budget: Budget) -> float:
        """Calculate amount spent for a budget's category in its period."""
        period_start, period_end = budget.get_period_dates()
        transactions = self._transactions.get_by_date_range(period_start, period_end)
        
        spent = 0.0
        for tx in transactions:
            if tx.category_id == budget.category_id and tx.type == TransactionType.EXPENSE:
                spent += tx.amount
        
        return spent
    
    def check_budget_alerts(self) -> list[BudgetAlert]:
        """Check all budgets and return triggered alerts."""
        alerts = []
        
        for budget in self._budgets.get_active_budgets():
            spent = self.calculate_spent_for_budget(budget)
            
            if budget.is_alert_triggered(spent):
                category = self._categories.get(budget.category_id)
                category_name = category.name if category else "Unknown"
                remaining = budget.get_remaining(spent)
                utilization = budget.get_utilization_percentage(spent)
                
                if utilization >= 100:
                    message = f"Over budget! You've spent ${spent:.2f} of ${budget.amount:.2f} for {category_name}"
                else:
                    message = f"Warning: {utilization:.1f}% of {category_name} budget used (${spent:.2f}/${budget.amount:.2f})"
                
                alerts.append(BudgetAlert(
                    budget_id=budget.id,
                    category_id=budget.category_id,
                    category_name=category_name,
                    budget_amount=budget.amount,
                    spent_amount=spent,
                    remaining_amount=remaining,
                    utilization_percentage=utilization,
                    message=message
                ))
        
        return alerts
    
    def generate_budget_report(self, budget_id: str) -> Optional[BudgetReport]:
        """Generate a detailed report for a budget."""
        budget = self._budgets.get(budget_id)
        if not budget:
            return None
        
        category = self._categories.get(budget.category_id)
        category_name = category.name if category else "Unknown"
        
        spent = self.calculate_spent_for_budget(budget)
        remaining = budget.get_remaining(spent)
        utilization = budget.get_utilization_percentage(spent)
        period_start, period_end = budget.get_period_dates()
        
        return BudgetReport(
            budget_id=budget.id,
            category_name=category_name,
            budget_amount=budget.amount,
            spent_amount=spent,
            remaining_amount=remaining,
            utilization_percentage=utilization,
            period_start=period_start,
            period_end=period_end,
            is_on_track=utilization < 100
        )
    
    def generate_all_budget_reports(self) -> list[BudgetReport]:
        """Generate reports for all active budgets."""
        reports = []
        for budget in self._budgets.get_active_budgets():
            report = self.generate_budget_report(budget.id)
            if report:
                reports.append(report)
        return reports
