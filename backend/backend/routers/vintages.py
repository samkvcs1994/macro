"""Vintages endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import IndexValue, Vintage
from ..schemas import IndexValueSchema, VintageDiffItem, VintageListItem

router = APIRouter(prefix="/vintages", tags=["vintages"])


@router.get("/", response_model=list[VintageListItem])
def list_vintages(session: Session = Depends(get_session)) -> list[VintageListItem]:
    vintages = session.execute(select(Vintage).order_by(Vintage.created_at.desc())).scalars().all()
    return [
        VintageListItem(
            vintage_id=v.vintage_id,
            created_at=v.created_at,
            notes=v.notes,
        )
        for v in vintages
    ]


@router.get("/{vintage_id}/diff", response_model=list[VintageDiffItem])
def vintage_diff(vintage_id: str, index: str = Query(..., alias="index"), session: Session = Depends(get_session)) -> list[VintageDiffItem]:
    stmt = select(IndexValue).where(IndexValue.vintage_id == vintage_id, IndexValue.index_name == index).order_by(IndexValue.ts)
    rows = session.execute(stmt).scalars().all()
    if not rows:
        raise HTTPException(status_code=404, detail="Vintage or index not found")
    return [
        VintageDiffItem(ts=row.ts, new=float(row.value))
        for row in rows
    ]
