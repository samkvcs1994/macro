"""Computation for the BIS Global Liquidity Indicator aggregate."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..etl.util import rolling_mean


@dataclass
class CreditConfig:
    step_hold_gli: bool = True
    smooth_ma_months: int = 0


@dataclass
class CreditInputs:
    usd: pd.Series
    eur_usd: pd.Series
    jpy_usd: pd.Series


def compute_gli_credit_usd(cfg: CreditConfig, inputs: CreditInputs) -> pd.Series:
    """Combine BIS GLI components into a monthly USD series."""

    combined = inputs.usd + inputs.eur_usd + inputs.jpy_usd
    combined = combined.sort_index()

    if cfg.step_hold_gli:
        monthly = combined.resample("M").ffill()
    else:
        monthly = combined.resample("M").interpolate("linear")

    if cfg.smooth_ma_months > 1:
        monthly = rolling_mean(monthly, cfg.smooth_ma_months)

    return monthly
