"""Pydantic schemas for API payloads."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SeriesPoint(BaseModel):
    ts: datetime
    value: float


class SeriesMetaSchema(BaseModel):
    series_id: str
    provider: str
    unit: str
    frequency: str
    description: Optional[str] = None
    transform_notes: Optional[str] = None


class SeriesResponse(BaseModel):
    series_id: str
    points: List[SeriesPoint]


class IndexComponent(BaseModel):
    name: str
    z_value: float
    weight: float


class IndexValueSchema(BaseModel):
    ts: datetime
    value: float


class IndexResponse(BaseModel):
    name: str
    unit: str = "index"
    points: List[IndexValueSchema]
    vintage_id: Optional[str] = None


class ConfigResponse(BaseModel):
    zscore_window_months: int
    weights_json: dict[str, float] = Field(default_factory=dict)
    rebase_date: Optional[str] = None
    index_scale: float
    index_multiplier: float
    use_fed_net: bool
    step_hold_gli: bool
    smooth_ma_months: int


class VintageListItem(BaseModel):
    vintage_id: str
    created_at: datetime
    notes: Optional[str] = None


class VintageDiffItem(BaseModel):
    ts: datetime
    old: Optional[float] = None
    new: Optional[float] = None
