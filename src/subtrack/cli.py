from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from subtrack.importers.generic_csv import load_transactions

app = typer.Typer(help="Find recurring subscriptions in your bank statements.")
console = Console()


@app.callback()
def main() -> None:
    """subtrack command line interface."""


@app.command()
def show(file: Path = typer.Argument(..., exists=True, help="Bank statement CSV")):
    """Print all transactions found in a CSV file."""
    table = Table(title=f"Transactions in {file.name}")
    table.add_column("Date")
    table.add_column("Description")
    table.add_column("Amount", justify="right")
    for t in load_transactions(file):
        table.add_row(t.date.isoformat(), t.description, f"{t.amount:,.2f}")
    console.print(table)