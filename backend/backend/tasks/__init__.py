"""Celery tasks package."""

from .build_indices import build_indices_task, celery_app

__all__ = ["build_indices_task", "celery_app"]
