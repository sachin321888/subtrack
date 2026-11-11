from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    date: date
    description: str
    amount: Decimal  # negative = money out
    merchant: str = ""


@dataclass
class Subscription:
    merchant: str
    interval_days: int
    price_history: list[tuple[date, Decimal]]  # (charge date, positive amount)

    @property
    def last_charged(self) -> date:
        return self.price_history[-1][0]

    @property
    def current_amount(self) -> Decimal:
        return self.price_history[-1][1]

    @property
    def next_expected(self) -> date:
        return self.last_charged + timedelta(days=self.interval_days)