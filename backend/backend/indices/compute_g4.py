"""Computation of the G4 central-bank balance sheet aggregate."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

from ..etl.util import rolling_mean


@dataclass
class G4Config:
    use_fed_net: bool = True
    smooth_ma_months: int = 0


@dataclass
class G4Inputs:
    fed_total: pd.Series
    fed_on_rrp: pd.Series
    fed_tga: pd.Series
    ecb_usd: pd.Series
    boj_usd: pd.Series
    boe_usd: pd.Series
    snb_usd: pd.Series | None = None


COMPONENTS = ["fed", "ecb", "boj", "boe", "snb"]


def compute_g4_usd_level(cfg: G4Config, inputs: G4Inputs) -> pd.Series:
    """Aggregate converted central-bank balance sheets."""

    fed_component = inputs.fed_total
    if cfg.use_fed_net:
        fed_component = inputs.fed_total - inputs.fed_on_rrp.reindex(inputs.fed_total.index, method="ffill") - inputs.fed_tga.reindex(inputs.fed_total.index, method="ffill")

    components: Dict[str, pd.Series] = {
        "fed": fed_component,
        "ecb": inputs.ecb_usd,
        "boj": inputs.boj_usd,
        "boe": inputs.boe_usd,
    }
    if inputs.snb_usd is not None:
        components["snb"] = inputs.snb_usd

    aligned = pd.DataFrame({key: series for key, series in components.items()}).dropna(how="all")
    aligned = aligned.fillna(method="ffill")

    total = aligned.sum(axis=1)
    if cfg.smooth_ma_months > 1:
        total = rolling_mean(total, cfg.smooth_ma_months)

    return total
