"""Personal Expense Tracker module.

Provides functionality to record expenses by category, validate transaction
amounts, calculate category summaries, track remaining budget balances,
identify highest single expenditures, and verify bank synchronization
passwords.
"""

import os
import tempfile
import webbrowser
from datetime import datetime

BANK_SYNC_PASSWORD = os.getenv("BANK_SYNC_PASSWORD", "demo-sync-pass")
expenses = []
budget_state = {"monthly_budget": 20000}
REPORT_DIR = os.getenv(
    "EXPENSE_REPORT_DIR",
    os.path.join(tempfile.gettempdir(), "expense_reports"),
)


def add_expense(amount, category="Misc", note=""):
    """Record an expense entry after validating the amount.

    Args:
        amount (int | float): Positive cost of the expense.
        category (str): Category grouping for the expense. Defaults to 'Misc'.
        note (str): Optional description note. Defaults to ''.

    Returns:
        bool: True if recorded successfully, False if amount was non-positive.
    """
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Calculate the sum of expenses aggregated by category.

    Returns:
        dict: Mapping of category names to total spent.
    """
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget limit.

    Args:
        new_budget (int | float): The new monthly budget amount.
    """
    budget_state["monthly_budget"] = new_budget


def get_budget():
    """Retrieve the current monthly budget amount.

    Returns:
        int | float: The configured monthly budget.
    """
    return budget_state["monthly_budget"]


def remaining_budget():
    """Calculate the remaining budget after subtracting all expenses.

    Returns:
        int | float: The difference between the budget and total expenses.
    """
    spent = sum(expense["amount"] for expense in expenses)
    return budget_state["monthly_budget"] - spent


def biggest_expense():
    """Find and return the expense with the highest amount.

    Returns:
        dict | None: The highest expense record, or None if no entries exist.
    """
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except ValueError:
        return None


def print_ledger():
    """Print all recorded expenses with index, category, and amount."""
    for i, expense in enumerate(expenses, 1):
        print(i, expense["category"], expense["amount"])


def check_sync_password(password):
    """Verify if the provided bank sync password matches the secret.

    Args:
        password (str): The candidate password to verify.

    Returns:
        bool: True if candidate matches BANK_SYNC_PASSWORD, False otherwise.
    """
    return password == BANK_SYNC_PASSWORD


def export_report():
    """Export report to a securely generated temporary file.

    Returns:
        str: Absolute path to the created report file.
    """
    os.makedirs(REPORT_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        suffix=".txt", dir=REPORT_DIR, delete=False
    ) as temp_file:
        report_path = temp_file.name
    return report_path


def open_statement(path):
    """Open an account statement document using the default system handler.

    Args:
        path (str): File system path to the statement document.
    """
    if os.path.exists(path):
        webbrowser.open(os.path.abspath(path))


def main():
    """Execute demonstration of the personal expense tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after setBudget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        get_budget(),
    )


if __name__ == "__main__":
    main()
