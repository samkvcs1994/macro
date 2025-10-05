"""Utilities for transforming raw series into standardized scores."""
from __future__ import annotations

import pandas as pd


def zscore(series: pd.Series, window_months: int, expanding_until: int | None = None) -> pd.Series:
    """Compute a rolling z-score for a series."""

    if series.empty:
        raise ValueError("Series is empty")

    if window_months <= 1:
        raise ValueError("window_months must be greater than 1")

    expanding_until = expanding_until or window_months

    z = pd.Series(index=series.index, dtype=float)
    for idx, value in series.items():
        window_end = series.index.get_loc(idx) + 1
        start_idx = max(0, window_end - window_months)
        window_series = series.iloc[start_idx:window_end]
        if window_end < expanding_until:
            window_series = series.iloc[:window_end]
        mean = window_series.mean()
        std = window_series.std(ddof=0)
        if std == 0:
            z[idx] = 0.0
        else:
            z[idx] = (value - mean) / std
    return z
