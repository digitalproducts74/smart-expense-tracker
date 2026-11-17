from datetime import date
from pathlib import Path
import csv

from .database import connect


def _to_cents(amount):
    """Convert a positive decimal amount to integer cents without float math."""
    from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

    try:
        value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError("Amount must be a valid number.")
    if not value.is_finite() or value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return int(value * 100)


def add_expense(db_path, amount, category, note="", expense_date=None):
    cents = _to_cents(amount)
    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    expense_date = expense_date or date.today().isoformat()
    try:
        date.fromisoformat(expense_date)
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD format.")

    with connect(db_path) as db:
        cursor = db.execute(
            "INSERT INTO expenses (date, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (expense_date, category, cents, note.strip()),
        )
        return cursor.lastrowid


def list_expenses(db_path, category=None):
    query = "SELECT id, date, category, amount_cents, note FROM expenses"
    params = ()
    if category:
        query += " WHERE lower(category) = lower(?)"
        params = (category.strip(),)
    query += " ORDER BY date DESC, id DESC"
    with connect(db_path) as db:
        return [dict(row) for row in db.execute(query, params).fetchall()]


def total_expenses(db_path):
    with connect(db_path) as db:
        row = db.execute("SELECT COALESCE(SUM(amount_cents), 0) AS total FROM expenses").fetchone()
        return row["total"]


def delete_expense(db_path, expense_id):
    with connect(db_path) as db:
        cursor = db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount == 1


def export_csv(db_path, output_path):
    rows = list_expenses(db_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "date", "category", "amount", "note"])
        for row in rows:
            writer.writerow([
                row["id"], row["date"], row["category"],
                f'{row["amount_cents"] / 100:.2f}', row["note"]
            ])
    return len(rows)
