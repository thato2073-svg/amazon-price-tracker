from __future__ import annotations
import pandas as pd

def price_summary(history: pd.DataFrame) -> dict[str, float]:
    if history.empty:
        return {"current": float("nan"), "low": float("nan"), "high": float("nan"), "average": float("nan"), "change_from_average": float("nan")}
    prices = history["price"]
    current = float(prices.iloc[-1])
    average = float(prices.mean())
    return {
        "current": current,
        "low": float(prices.min()),
        "high": float(prices.max()),
        "average": average,
        "change_from_average": (current / average - 1) if average else float("nan"),
    }

def target_reached(current_price: float, target_price: float | None) -> bool:
    return target_price is not None and current_price <= target_price
