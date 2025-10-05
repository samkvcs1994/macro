"""Simple scheduler for orchestrating nightly refresh."""
from __future__ import annotations

from datetime import datetime

from loguru import logger

from .build_indices import build_indices_task


def run_nightly_job() -> str:
    """Trigger the index rebuild task and return its Celery task id."""

    result = build_indices_task.delay()
    logger.info(
        "Running nightly job",
        run_at=datetime.utcnow(),
        task_id=result.id,
    )
    return result.id
