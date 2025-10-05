"""Database models for the Global Liquidity Indices application."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Numeric, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class SeriesMeta(Base):
    """Metadata describing an underlying time-series."""

    __tablename__ = "series_meta"

    series_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    unit: Mapped[str] = mapped_column(String(16), nullable=False)
    frequency: Mapped[str] = mapped_column(String(8), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    transform_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    observations: Mapped[list[SeriesObservation]] = relationship(back_populates="series")


class SeriesObservation(Base):
    """Time-series observation values."""

    __tablename__ = "series_observation"
    __table_args__ = (PrimaryKeyConstraint("series_id", "ts"),)

    series_id: Mapped[str] = mapped_column(String(64), ForeignKey("series_meta.series_id"), nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)

    series: Mapped[SeriesMeta] = relationship(back_populates="observations")


class Vintage(Base):
    """Represents a snapshot of the full dataset at a point in time."""

    __tablename__ = "vintages"

    vintage_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    code_version: Mapped[str] = mapped_column(String(64), nullable=False)

    snapshots: Mapped[list[SeriesSnapshot]] = relationship(back_populates="vintage")
    index_values: Mapped[list[IndexValue]] = relationship(back_populates="vintage")


class SeriesSnapshot(Base):
    """Series values as they existed for a vintage."""

    __tablename__ = "series_snapshot"
    __table_args__ = (PrimaryKeyConstraint("vintage_id", "series_id", "ts"),)

    vintage_id: Mapped[str] = mapped_column(String(36), ForeignKey("vintages.vintage_id"), nullable=False)
    series_id: Mapped[str] = mapped_column(String(64), nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)

    vintage: Mapped[Vintage] = relationship(back_populates="snapshots")


class IndicesConfig(Base):
    """Runtime configuration for index calculations."""

    __tablename__ = "indices_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    zscore_window_months: Mapped[int] = mapped_column(default=120)
    weights_json: Mapped[dict] = mapped_column(JSON, default=dict)
    rebase_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    index_scale: Mapped[float] = mapped_column(default=100.0)
    index_multiplier: Mapped[float] = mapped_column(default=10.0)
    use_fed_net: Mapped[bool] = mapped_column(Boolean, default=True)
    step_hold_gli: Mapped[bool] = mapped_column(Boolean, default=True)
    smooth_ma_months: Mapped[int] = mapped_column(default=0)


class IndexValue(Base):
    """Calculated index values for a given vintage."""

    __tablename__ = "index_values"
    __table_args__ = (PrimaryKeyConstraint("index_name", "ts", "vintage_id"),)

    index_name: Mapped[str] = mapped_column(String(32), nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    vintage_id: Mapped[str] = mapped_column(String(36), ForeignKey("vintages.vintage_id"), nullable=False)

    vintage: Mapped[Vintage] = relationship(back_populates="index_values")
