import sqlite3
from pathlib import Path

DEFAULT_DB = Path.home() / ".smart_expense_tracker.sqlite3"


def connect(db_path=DEFAULT_DB):
    """Open a SQLite connection and ensure the expenses table exists."""
    path = Path(db_path)
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
            note TEXT NOT NULL DEFAULT ''
        )
    """)
    connection.commit()
    return connection
