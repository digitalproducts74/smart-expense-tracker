import csv
import pytest

from expense_tracker.core import (
    add_expense, list_expenses, total_expenses, delete_expense, export_csv
)


def test_add_and_list_expense(tmp_path):
    db = tmp_path / "test.db"
    expense_id = add_expense(db, "12.50", "Food", "Lunch", "2026-01-15")
    rows = list_expenses(db)
    assert rows[0]["id"] == expense_id
    assert rows[0]["amount_cents"] == 1250
    assert rows[0]["category"] == "Food"
    assert rows[0]["note"] == "Lunch"


def test_total_expenses_uses_integer_cents(tmp_path):
    db = tmp_path / "test.db"
    add_expense(db, "0.10", "Other", expense_date="2026-01-01")
    add_expense(db, "0.20", "Other", expense_date="2026-01-02")
    assert total_expenses(db) == 30


def test_category_filter_is_case_insensitive(tmp_path):
    db = tmp_path / "test.db"
    add_expense(db, "5", "Food", expense_date="2026-01-01")
    add_expense(db, "8", "Transport", expense_date="2026-01-01")
    assert len(list_expenses(db, "food")) == 1


@pytest.mark.parametrize("amount", ["0", "-1", "abc", "NaN"])
def test_invalid_amount_is_rejected(tmp_path, amount):
    with pytest.raises(ValueError):
        add_expense(tmp_path / "test.db", amount, "Food")


def test_empty_category_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        add_expense(tmp_path / "test.db", "2", "  ")


def test_delete_expense(tmp_path):
    db = tmp_path / "test.db"
    expense_id = add_expense(db, "5", "Food", expense_date="2026-01-01")
    assert delete_expense(db, expense_id) is True
    assert delete_expense(db, expense_id) is False
    assert list_expenses(db) == []


def test_export_csv(tmp_path):
    db = tmp_path / "test.db"
    add_expense(db, "3.25", "Books", "Python", "2026-02-01")
    output = tmp_path / "exports" / "expenses.csv"
    assert export_csv(db, output) == 1
    with output.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0]["amount"] == "3.25"
    assert rows[0]["note"] == "Python"
