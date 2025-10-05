"""Indices related endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import IndexValue, SeriesObservation
from ..schemas import IndexResponse, IndexValueSchema, SeriesPoint, SeriesResponse

router = APIRouter(prefix="/indices", tags=["indices"])


def _parse_bounds(start: Optional[str], end: Optional[str]) -> tuple[Optional[datetime], Optional[datetime]]:
    fmt = "%Y-%m"
    start_dt = datetime.strptime(start, fmt) if start else None
    end_dt = datetime.strptime(end, fmt) if end else None
    return start_dt, end_dt


@router.get("/", response_model=list[str])
def list_indices(session: Session = Depends(get_session)) -> list[str]:
    results = session.execute(select(IndexValue.index_name).distinct()).scalars().all()
    return sorted(set(results))


@router.get("/{name}", response_model=IndexResponse)
def get_index(name: str, start: Optional[str] = None, end: Optional[str] = None, session: Session = Depends(get_session)) -> IndexResponse:
    start_dt, end_dt = _parse_bounds(start, end)
    stmt = select(IndexValue).where(IndexValue.index_name == name)
    if start_dt:
        stmt = stmt.where(IndexValue.ts >= start_dt)
    if end_dt:
        stmt = stmt.where(IndexValue.ts <= end_dt)
    stmt = stmt.order_by(IndexValue.ts)
    points = [IndexValueSchema(ts=row.ts, value=float(row.value)) for row in session.execute(stmt).scalars().all()]
    if not points:
        raise HTTPException(status_code=404, detail=f"Index '{name}' not found")
    vintage_id = session.execute(
        select(IndexValue.vintage_id)
        .where(IndexValue.index_name == name)
        .order_by(IndexValue.ts.desc())
        .limit(1)
    ).scalar_one_or_none()
    return IndexResponse(name=name, points=points, vintage_id=vintage_id)


@router.get("/{name}/components", response_model=list[SeriesResponse])
def get_index_components(name: str, start: Optional[str] = None, end: Optional[str] = None, session: Session = Depends(get_session)) -> list[SeriesResponse]:
    start_dt, end_dt = _parse_bounds(start, end)
    stmt = select(SeriesObservation).where(SeriesObservation.series_id.like(f"{name}%"))
    if start_dt:
        stmt = stmt.where(SeriesObservation.ts >= start_dt)
    if end_dt:
        stmt = stmt.where(SeriesObservation.ts <= end_dt)
    stmt = stmt.order_by(SeriesObservation.series_id, SeriesObservation.ts)
    rows = session.execute(stmt).scalars().all()
    series: dict[str, list[SeriesPoint]] = {}
    for row in rows:
        points = series.setdefault(row.series_id, [])
        points.append(SeriesPoint(ts=row.ts, value=float(row.value)))
    return [SeriesResponse(series_id=sid, points=pts) for sid, pts in series.items()]
