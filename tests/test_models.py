from datetime import date
from decimal import Decimal

from subtrack.models import Transaction


def test_charge_is_money_out():
    t = Transaction(date(2026, 1, 5), "NETFLIX.COM", Decimal("-499.00"))
    assert t.amount < 0
    assert t.merchant == ""