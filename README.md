# Smart Expense Tracker

A beginner-friendly command-line application for recording personal expenses with Python and SQLite.

## Features

- Add expenses with a date, category, amount, and optional note.
- List all expenses or filter by category.
- Calculate total spending.
- Delete an expense by its ID.
- Export expenses to CSV.
- Store money as integer cents to avoid common floating-point rounding errors.
- Run automated tests with pytest.

## Requirements

- Python 3.10 or newer
- pip

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/smart-expense-tracker.git
cd smart-expense-tracker
python -m venv .venv
```

Activate the virtual environment:

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Add an expense:

```bash
python -m expense_tracker add 12.50 Food --note "Lunch" --date 2026-01-15
```

List expenses:

```bash
python -m expense_tracker list
```

Filter by category:

```bash
python -m expense_tracker list --category Food
```

Show the total:

```bash
python -m expense_tracker total
```

Delete an expense (replace `1` with its ID):

```bash
python -m expense_tracker delete 1
```

Export to CSV:

```bash
python -m expense_tracker export expenses.csv
```

Use a specific database file:

```bash
python -m expense_tracker --db ./my-expenses.sqlite3 list
```

The default database is stored in your home directory. Amounts are currency-neutral; choose one currency per database and use it consistently.

## Run tests

```bash
pytest
```

## Project structure

```text
smart-expense-tracker/
├── expense_tracker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── core.py
│   └── database.py
├── tests/
│   └── test_core.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Learning roadmap

1. Add monthly summaries.
2. Add budgets and spending alerts.
3. Add charts using matplotlib.
4. Add a graphical interface.
5. Add support for importing bank-export CSV files.

## License

MIT
