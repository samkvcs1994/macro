"""Composite index calculation helpers."""
from __future__ import annotations

from typing import Dict

import pandas as pd


def blend_indices(zs: dict[str, pd.Series], weights: dict[str, float]) -> pd.Series:
    """Blend standardized series using provided weights."""

    if not zs:
        raise ValueError("No series provided")
    total_weight = sum(weights.get(name, 0.0) for name in zs)
    if total_weight == 0:
        raise ValueError("Weights sum to zero")

    aligned = pd.DataFrame(zs).dropna(how="all").fillna(method="ffill")
    normalized_weights: Dict[str, float] = {}
    for name in aligned.columns:
        normalized_weights[name] = weights.get(name, 0.0) / total_weight

    blended = sum(aligned[col] * normalized_weights.get(col, 0.0) for col in aligned.columns)
    return blended


def scale_index(z: pd.Series, base: float = 100.0, mult: float = 10.0) -> pd.Series:
    """Scale a z-score series into an index."""

    return base + mult * z


def rebase(series: pd.Series, base_date: str, target: float = 100.0) -> pd.Series:
    """Rebase the series so that the value on base_date equals target."""

    if base_date not in series.index.strftime("%Y-%m-%d").tolist():
        return series
    index = series.index.strftime("%Y-%m-%d").tolist().index(base_date)
    current_value = series.iloc[index]
    if current_value == 0:
        return series
    factor = target / current_value
    return series * factor
