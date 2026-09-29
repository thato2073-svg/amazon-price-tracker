from __future__ import annotations
from pricewatch.analytics import target_reached
from pricewatch.scraper import fetch_product
from pricewatch.storage import save_snapshot

def check_product(url: str, target_price: float | None = None):
    snapshot = fetch_product(url)
    save_snapshot(snapshot, target_price)
    return snapshot, target_reached(snapshot.price, target_price)
