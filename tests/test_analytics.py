import pandas as pd
from pricewatch.analytics import price_summary, target_reached

def test_price_summary():
    frame = pd.DataFrame({"price": [100.0, 80.0, 90.0]})
    result = price_summary(frame)
    assert result["current"] == 90.0
    assert result["low"] == 80.0
    assert result["high"] == 100.0
    assert result["average"] == 90.0
    assert result["change_from_average"] == 0.0

def test_target_reached():
    assert target_reached(79.99, 80.0)
    assert not target_reached(80.01, 80.0)
    assert not target_reached(50.0, None)
