import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from subtrack.models import Transaction


def load_transactions(
    path: str | Path, date_format: str = "%Y-%m-%d"
) -> list[Transaction]:
    """Read a bank-statement CSV and return a list of Transactions."""
    transactions = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):  # line 1 is the header
            try:
                transactions.append(
                    Transaction(
                        date=datetime.strptime(row["date"].strip(), date_format).date(),
                        description=row["description"].strip(),
                        amount=Decimal(row["amount"].strip().replace(",", "")),
                    )
                )
            except (KeyError, ValueError, InvalidOperation) as e:
                raise ValueError(f"Line {line_no}: bad row {row!r}: {e}") from e
    return transactions