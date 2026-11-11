from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from subtrack.detect import detect_subscriptions
from subtrack.importers.generic_csv import load_transactions

app = typer.Typer(help="Find recurring subscriptions in your bank statements.")
console = Console()

FileArg = Annotated[Path, typer.Argument(exists=True, help="Bank statement CSV")]


@app.callback()
def main() -> None:
    """subtrack command line interface."""


@app.command()
def show(file: FileArg) -> None:
    """Print all transactions found in a CSV file."""
    table = Table(title=f"Transactions in {file.name}")
    table.add_column("Date")
    table.add_column("Description")
    table.add_column("Amount", justify="right")
    for t in load_transactions(file):
        table.add_row(t.date.isoformat(), t.description, f"{t.amount:,.2f}")
    console.print(table)


@app.command()
def detect(file: FileArg) -> None:
    """List recurring subscriptions found in a CSV file."""
    subs = detect_subscriptions(load_transactions(file))
    if not subs:
        console.print("No recurring subscriptions found.")
        raise typer.Exit()

    table = Table(title="Recurring subscriptions")
    table.add_column("Merchant")
    table.add_column("Every (days)", justify="right")
    table.add_column("Amount", justify="right")
    table.add_column("Last charged")
    table.add_column("Next expected")
    table.add_column("Note")
    for s in subs:
        first_price = s.price_history[0][1]
        note = (
            f"price changed from {first_price:,.2f}"
            if first_price != s.current_amount
            else ""
        )
        table.add_row(
            s.merchant,
            str(s.interval_days),
            f"{s.current_amount:,.2f}",
            s.last_charged.isoformat(),
            s.next_expected.isoformat(),
            note,
        )
    console.print(table)

    monthly = sum(s.current_amount for s in subs if s.interval_days == 30)
    console.print(f"Monthly subscription total: {monthly:,.2f}")