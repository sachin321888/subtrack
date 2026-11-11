from collections import defaultdict
from itertools import pairwise

from subtrack.models import Subscription, Transaction
from subtrack.normalize import normalize_merchant

# (typical gap in days, allowed drift in days)
INTERVALS = [(7, 1), (30, 4), (365, 10)]
MIN_CHARGES = 3


def _match_interval(gaps: list[int]) -> int | None:
    """Return the interval (7/30/365) that ALL gaps fit, else None."""
    for days, tolerance in INTERVALS:
        if all(abs(gap - days) <= tolerance for gap in gaps):
            return days
    return None


def detect_subscriptions(transactions: list[Transaction]) -> list[Subscription]:
    groups: dict[str, list[Transaction]] = defaultdict(list)
    for t in transactions:
        if t.amount < 0:  # ignore money coming in (salary, refunds)
            groups[normalize_merchant(t.description)].append(t)

    found = []
    for merchant, txs in groups.items():
        if len(txs) < MIN_CHARGES:
            continue
        txs.sort(key=lambda t: t.date)
        gaps = [(b.date - a.date).days for a, b in pairwise(txs)]
        interval = _match_interval(gaps)
        if interval is None:
            continue
        amounts = [abs(t.amount) for t in txs]
        if max(amounts) > 2 * min(amounts):  # wildly different amounts: not a plan
            continue
        found.append(
            Subscription(
                merchant=merchant,
                interval_days=interval,
                price_history=[(t.date, abs(t.amount)) for t in txs],
            )
        )
    return sorted(found, key=lambda s: s.merchant)