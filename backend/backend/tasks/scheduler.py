"""Simple scheduler for orchestrating nightly refresh."""
from __future__ import annotations

from datetime import datetime

from loguru import logger

from .build_indices import build_indices_task


def run_nightly_job() -> str:
    """Trigger the index rebuild task."""

    logger.info("Running nightly job", run_at=datetime.utcnow())
    return build_indices_task.delay()  # type: ignore[return-value]
