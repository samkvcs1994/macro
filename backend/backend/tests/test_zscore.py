import pandas as pd
import pytest

from backend.indices.standardize import zscore


def test_zscore_basic():
    idx = pd.date_range("2020-01-31", periods=6, freq="M")
    series = pd.Series([1, 2, 3, 4, 5, 6], index=idx)
    result = zscore(series, window_months=3)
    assert pytest.approx(result.iloc[-1], rel=1e-6) == (6 - 5) / 0.8164965809
