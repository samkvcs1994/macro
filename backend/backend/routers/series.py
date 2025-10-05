"""Raw series endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import SeriesMeta, SeriesObservation
from ..schemas import SeriesMetaSchema, SeriesPoint, SeriesResponse

router = APIRouter(prefix="/series", tags=["series"])


def _parse_month(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m")


@router.get("/meta", response_model=list[SeriesMetaSchema])
def list_series_meta(session: Session = Depends(get_session)) -> list[SeriesMetaSchema]:
    results = session.execute(select(SeriesMeta)).scalars().all()
    payload = []
    for row in results:
        payload.append(
            SeriesMetaSchema(
                series_id=row.series_id,
                provider=row.provider,
                unit=row.unit,
                frequency=row.frequency,
                description=row.description,
                transform_notes=row.transform_notes,
            )
        )
    return payload


@router.get("/{series_id}", response_model=SeriesResponse)
def get_series(series_id: str, start: Optional[str] = None, end: Optional[str] = None, session: Session = Depends(get_session)) -> SeriesResponse:
    start_dt = _parse_month(start)
    end_dt = _parse_month(end)
    stmt = select(SeriesObservation).where(SeriesObservation.series_id == series_id)
    if start_dt:
        stmt = stmt.where(SeriesObservation.ts >= start_dt)
    if end_dt:
        stmt = stmt.where(SeriesObservation.ts <= end_dt)
    stmt = stmt.order_by(SeriesObservation.ts)
    rows = session.execute(stmt).scalars().all()
    if not rows:
        raise HTTPException(status_code=404, detail=f"Series '{series_id}' not found")
    points = [SeriesPoint(ts=row.ts, value=float(row.value)) for row in rows]
    return SeriesResponse(series_id=series_id, points=points)
