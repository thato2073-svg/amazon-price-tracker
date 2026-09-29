from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProductSnapshot:
    url: str
    title: str
    price: float
    currency: str
    captured_at: datetime
