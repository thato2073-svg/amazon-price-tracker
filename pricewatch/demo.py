from __future__ import annotations
import numpy as np
import pandas as pd

def demo_history(days: int = 60) -> pd.DataFrame:
    """Return deterministic synthetic history for UI demonstration only."""
    index = pd.date_range(end=pd.Timestamp.now(tz="UTC").normalize(), periods=days, freq="D")
    x = np.arange(days)
    trend = 139.99 - 0.28 * x
    cycles = 12 * np.sin(x / 4.2) + 5 * np.sin(x / 1.9)
    sale_events = np.where((x >= 20) & (x <= 25), -24, 0) + np.where((x >= 47) & (x <= 51), -18, 0)
    prices = np.maximum(69.99, trend + cycles + sale_events)
    return pd.DataFrame({"price": np.round(prices, 2)}, index=index)
