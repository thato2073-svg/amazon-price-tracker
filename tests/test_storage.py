from datetime import datetime, timezone
from pathlib import Path
from pricewatch.models import ProductSnapshot
from pricewatch.storage import history, products, save_snapshot

def test_storage_round_trip(tmp_path: Path):
    db = tmp_path / "prices.db"
    snapshot = ProductSnapshot("https://amazon.ca/dp/X", "Item", 42.5, "CAD", datetime.now(timezone.utc))
    save_snapshot(snapshot, 40.0, db)
    assert history(snapshot.url, db)["price"].tolist() == [42.5]
    catalog = products(db)
    assert catalog.iloc[0]["title"] == "Item"
    assert catalog.iloc[0]["target_price"] == 40.0


def test_product_without_target_returns_missing_target(tmp_path: Path):
    db = tmp_path / "prices-no-target.db"
    snapshot = ProductSnapshot("https://amazon.ca/dp/Y", "No Target Item", 105.98, "CAD", datetime.now(timezone.utc))
    save_snapshot(snapshot, None, db)
    catalog = products(db)
    assert catalog.iloc[0]["current_price"] == 105.98
    assert catalog.iloc[0]["target_price"] != catalog.iloc[0]["target_price"]
