import pandas as pd
from pricewatch.demo import demo_history

def test_demo_history_is_deterministic_shape_and_varies():
    frame = demo_history(60)
    assert len(frame) == 60
    assert list(frame.columns) == ["price"]
    assert frame["price"].nunique() > 10
    assert frame["price"].min() < frame["price"].max()
    assert isinstance(frame.index, pd.DatetimeIndex)
