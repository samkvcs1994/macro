"""Celery task definitions for building indices."""
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pandas as pd
from celery import Celery
from loguru import logger

from ..config import get_settings
from ..db import session_scope
from ..indices.compute_g4 import G4Config, G4Inputs, compute_g4_usd_level
from ..indices.compute_gli_credit import CreditConfig, CreditInputs, compute_gli_credit_usd
from ..indices.composite import blend_indices, scale_index
from ..indices.standardize import zscore
from ..models import IndexValue, Vintage

celery_app = Celery("gli.tasks")
settings = get_settings()
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url


@celery_app.task
def build_indices_task() -> str:
    """Entry point for rebuilding all indices.

    The implementation here is intentionally simplified; in production this would
    orchestrate the full ETL pipeline before persisting results.
    """

    logger.info("Starting index rebuild task")
    vintage_id = str(uuid4())

    # Placeholder toy data; replace with ETL results.
    date_range = pd.date_range("2015-01-31", periods=24, freq="M")
    dummy_series = pd.Series(range(len(date_range)), index=date_range, dtype=float)

    g4 = compute_g4_usd_level(G4Config(), G4Inputs(dummy_series, dummy_series, dummy_series, dummy_series, dummy_series, dummy_series))
    gli_credit = compute_gli_credit_usd(CreditConfig(), CreditInputs(dummy_series, dummy_series, dummy_series))

    g4_z = zscore(g4, window_months=12)
    gli_z = zscore(gli_credit, window_months=12)
    composite_z = blend_indices({"GLI_G4_CB": g4_z, "GLI_Credit": gli_z}, settings.weights_json.to_dict())
    composite = scale_index(composite_z, base=settings.index_scale, mult=settings.index_multiplier)

    with session_scope() as session:
        vintage = Vintage(vintage_id=vintage_id, created_at=datetime.utcnow(), notes="Automated refresh", code_version="dev")
        session.add(vintage)
        session.flush()

        for ts, value in composite.items():
            session.merge(IndexValue(index_name="GLI_Composite", ts=ts, value=value, vintage_id=vintage_id))

    logger.info("Completed index rebuild", vintage_id=vintage_id)
    return vintage_id
