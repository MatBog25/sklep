from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from pydantic import Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Waluta(str, Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class TimestampMixin:
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
