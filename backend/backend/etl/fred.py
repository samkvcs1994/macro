"""FRED data ingestion helpers."""
from __future__ import annotations

from typing import Any

import httpx
import pandas as pd
from loguru import logger

from ..config import get_settings

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred_series(series_id: str, start: str | None = None) -> pd.DataFrame:
    """Fetch a series from FRED and return a dataframe indexed by datetime."""

    params: dict[str, Any] = {
        "series_id": series_id,
        "file_type": "json",
    }
    if start:
        params["observation_start"] = start
    settings = get_settings()
    if settings.fred_api_key:
        params["api_key"] = settings.fred_api_key

    logger.debug("Fetching FRED series {series_id}", series_id=series_id)
    response = httpx.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    observations = data.get("observations", [])
    if not observations:
        return pd.DataFrame(columns=["value"], dtype=float)

    df = pd.DataFrame(observations)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.set_index("date").sort_index()
    return df[["value"]]
