from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from subtrack.importers.generic_csv import load_transactions

FIXTURES = Path(__file__).parent / "fixtures"


def test_loads_all_rows():
    txs = load_transactions(FIXTURES / "sample_statement.csv")
    assert len(txs) == 12
    assert txs[0].date == date(2026, 1, 3)
    assert txs[0].amount == Decimal("-499.00")


def test_bad_amount_reports_the_line(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("date,description,amount\n2026-01-05,NETFLIX,abc\n")
    with pytest.raises(ValueError, match="Line 2"):
        load_transactions(bad)