import pandas as pd
import pytest

from backend.etl.util import fx_convert_to_usd, resample_month_end


def test_resample_month_end_last_value():
    idx = pd.date_range("2022-01-01", periods=10, freq="D")
    df = pd.DataFrame({"value": range(10)}, index=idx)
    resampled = resample_month_end(df)
    assert resampled.iloc[0] == 9


def test_fx_convert_to_usd_handles_usd():
    idx = pd.date_range("2021-01-31", periods=3, freq="M")
    series = pd.Series([1.0, 2.0, 3.0], index=idx)
    fx = pd.Series([1.1, 1.2, 1.3], index=idx)
    converted = fx_convert_to_usd(series, "USD", fx)
    pd.testing.assert_series_equal(converted, series)


def test_fx_convert_to_usd_multiplies_rates():
    idx = pd.date_range("2021-01-31", periods=3, freq="M")
    series = pd.Series([1.0, 2.0, 3.0], index=idx)
    fx_idx = pd.date_range("2021-01-01", periods=90, freq="D")
    fx = pd.Series(1.0, index=fx_idx)
    result = fx_convert_to_usd(series, "EUR", fx)
    assert pytest.approx(result.iloc[0]) == 1.0
