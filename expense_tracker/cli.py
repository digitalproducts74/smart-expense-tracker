import argparse
from pathlib import Path

from .core import add_expense, list_expenses, total_expenses, delete_expense, export_csv
from .database import DEFAULT_DB


def money(cents):
    return f"{cents / 100:.2f}"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track personal expenses from your terminal."
    )
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Database file path")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add an expense")
    add.add_argument("amount", help="Positive amount, e.g. 12.50")
    add.add_argument("category", help="Category, e.g. Food")
    add.add_argument("--note", default="", help="Optional note")
    add.add_argument("--date", dest="expense_date", help="Date YYYY-MM-DD")

    listing = commands.add_parser("list", help="List expenses")
    listing.add_argument("--category", help="Filter by category")

    commands.add_parser("total", help="Show total expenses")

    delete = commands.add_parser("delete", help="Delete an expense by ID")
    delete.add_argument("id", type=int)

    export = commands.add_parser("export", help="Export expenses to CSV")
    export.add_argument("file", help="Output CSV path")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            expense_id = add_expense(
                args.db, args.amount, args.category, args.note, args.expense_date
            )
            print(f"Added expense #{expense_id}.")
        elif args.command == "list":
            rows = list_expenses(args.db, args.category)
            if not rows:
                print("No expenses found.")
            for row in rows:
                print(
                    f'#{row["id"]} | {row["date"]} | {row["category"]} | '
                    f'{money(row["amount_cents"])} | {row["note"]}'
                )
        elif args.command == "total":
            print(f"Total: {money(total_expenses(args.db))}")
        elif args.command == "delete":
            if delete_expense(args.db, args.id):
                print(f"Deleted expense #{args.id}.")
            else:
                print(f"Expense #{args.id} was not found.")
        elif args.command == "export":
            count = export_csv(args.db, args.file)
            print(f"Exported {count} expense(s) to {Path(args.file)}.")
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
