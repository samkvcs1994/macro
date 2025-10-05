"""Shared ETL utilities for time-series transformation."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

import pandas as pd


def resample_month_end(df: pd.DataFrame, how: Literal["eom", "mean"] = "eom", column: str = "value") -> pd.Series:
    """Resample a dataframe to month-end frequency.

    Parameters
    ----------
    df: pd.DataFrame
        Input dataframe with a datetime index and at least one value column.
    how: Literal["eom", "mean"]
        Aggregation rule. "eom" picks the last observation within the month,
        while "mean" returns the monthly average.
    column: str
        Column to resample.
    """

    if df.empty:
        raise ValueError("Input dataframe is empty")

    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("Dataframe must be indexed by DatetimeIndex")

    freq = "M"
    if how == "eom":
        return df[column].resample(freq).last().dropna()
    if how == "mean":
        return df[column].resample(freq).mean().dropna()
    raise ValueError(f"Unsupported aggregation rule: {how}")


def fx_convert_to_usd(df: pd.Series, ccy: str, fx_df: pd.Series, rule: Literal["eom", "avg"] = "eom") -> pd.Series:
    """Convert a currency series to USD using FX rates.

    Parameters
    ----------
    df: pd.Series
        Series indexed by datetime containing values in the original currency.
    ccy: str
        Currency code of the input series.
    fx_df: pd.Series
        FX series representing USD pairs (e.g., EUR/USD) where the quote is units of USD per foreign currency.
    rule: Literal["eom", "avg"]
        Whether to use end-of-month or average FX rates.
    """

    if ccy.upper() == "USD":
        return df

    if rule not in {"eom", "avg"}:
        raise ValueError("rule must be either 'eom' or 'avg'")

    fx_resampled = fx_df.resample("M")
    fx_series = fx_resampled.last() if rule == "eom" else fx_resampled.mean()

    aligned = df.reindex(fx_series.index).fillna(method="ffill")
    if aligned.isna().any():
        aligned = aligned.fillna(method="bfill")

    return aligned * fx_series


def month_end(dt: datetime) -> datetime:
    """Return the month-end for the provided datetime."""

    return (dt + pd.offsets.MonthEnd(0)).to_pydatetime()


def rolling_mean(series: pd.Series, window_months: int) -> pd.Series:
    """Apply a simple moving average with the given window."""

    if window_months <= 1:
        return series
    return series.rolling(window=window_months, min_periods=1).mean()
