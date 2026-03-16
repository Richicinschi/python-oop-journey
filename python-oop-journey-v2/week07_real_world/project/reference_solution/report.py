"""Report generation module.

Generate financial reports including summaries, breakdowns, and trends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


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
class AccountBalanceHistory:
    """Balance history for an account over time."""
    
    account_id: str
    account_name: str
    start_balance: float
    end_balance: float
    daily_balances: list[tuple[date, float]] = field(default_factory=list)
    min_balance: float = 0.0
    max_balance: float = 0.0
    
    def __post_init__(self) -> None:
        """Calculate min/max from daily balances."""
        if self.daily_balances:
            balances = [b for _, b in self.daily_balances]
            self.min_balance = min(balances)
            self.max_balance = max(balances)


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


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format an amount as currency string.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{amount:,.2f}"


def generate_spending_trend(
    monthly_expenses: list[tuple[int, int, float]]
) -> list[tuple[int, int, float, float]]:
    """Generate month-over-month spending trend.
    
    Args:
        monthly_expenses: List of (year, month, amount) tuples
        
    Returns:
        List of (year, month, amount, change_percentage) tuples
    """
    if not monthly_expenses:
        return []
    
    # Sort by date
    sorted_expenses = sorted(monthly_expenses, key=lambda x: (x[0], x[1]))
    
    result = []
    previous_amount: Optional[float] = None
    
    for year, month, amount in sorted_expenses:
        if previous_amount is None or previous_amount == 0:
            change_pct = 0.0
        else:
            change_pct = ((amount - previous_amount) / previous_amount) * 100
        
        result.append((year, month, amount, round(change_pct, 2)))
        previous_amount = amount
    
    return result


def generate_text_report(summary: MonthlySummary) -> str:
    """Generate a formatted text report from a monthly summary.
    
    Args:
        summary: Monthly summary to format
        
    Returns:
        Formatted text report
    """
    lines = [
        "=" * 50,
        f"Monthly Financial Report - {summary.year}-{summary.month:02d}",
        "=" * 50,
        "",
        f"Total Income:    {format_currency(summary.total_income)}",
        f"Total Expenses:  {format_currency(summary.total_expenses)}",
        f"Net Flow:        {format_currency(summary.net_flow)}",
        f"Transactions:    {summary.transaction_count}",
        "",
        "Savings Rate:    {:.1f}%".format(summary.savings_rate()),
        "Status:          {}".format("Profitable" if summary.is_profitable() else "Deficit"),
        "",
    ]
    
    if summary.top_expense_categories:
        lines.append("Top Expense Categories:")
        for name, amount in summary.top_expense_categories:
            lines.append(f"  - {name}: {format_currency(amount)}")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def calculate_running_balance(
    transactions: list,
    start_balance: float = 0.0
) -> list[tuple[date, float]]:
    """Calculate running balance from a list of transactions.
    
    Args:
        transactions: List of transactions with date and signed_amount()
        start_balance: Starting balance
        
    Returns:
        List of (date, balance) tuples
    """
    # Sort transactions by date
    sorted_tx = sorted(transactions, key=lambda x: x.date)
    
    running_balance = start_balance
    result: list[tuple[date, float]] = []
    
    for tx in sorted_tx:
        running_balance += tx.signed_amount()
        result.append((tx.date, running_balance))
    
    return result
