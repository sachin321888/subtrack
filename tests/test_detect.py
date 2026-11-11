from datetime import date
from decimal import Decimal
from pathlib import Path

from subtrack.detect import detect_subscriptions
from subtrack.importers.generic_csv import load_transactions
from subtrack.models import Transaction

FIXTURES = Path(__file__).parent / "fixtures"


def _sample():
    return detect_subscriptions(load_transactions(FIXTURES / "sample_statement.csv"))


def test_finds_the_three_subscriptions():
    assert [s.merchant for s in _sample()] == [
        "Gym Fitzone Membership",
        "Netflix",
        "Spotify",
    ]


def test_ignores_one_off_purchases_and_income():
    merchants = [s.merchant for s in _sample()]
    assert "Swiggy" not in merchants
    assert "Salary Credit" not in merchants


def test_all_sample_subscriptions_are_monthly():
    assert all(s.interval_days == 30 for s in _sample())


def test_netflix_price_hike_is_in_history():
    netflix = next(s for s in _sample() if s.merchant == "Netflix")
    assert netflix.price_history[0][1] == Decimal("499.00")
    assert netflix.current_amount == Decimal("649.00")
    assert netflix.next_expected == date(2026, 4, 2)


def test_irregular_charges_are_not_subscriptions():
    txs = [
        Transaction(date(2026, 1, 1), "CAFE ROYALE", Decimal(-200)),
        Transaction(date(2026, 1, 12), "CAFE ROYALE", Decimal(-180)),
        Transaction(date(2026, 3, 2), "CAFE ROYALE", Decimal(-220)),
    ]
    assert detect_subscriptions(txs) == []