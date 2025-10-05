"""Tests for the scheduler helpers."""
from __future__ import annotations

import pytest

from backend.tasks import scheduler


class DummyAsyncResult:
    """Minimal stand-in for Celery's AsyncResult."""

    def __init__(self, identifier: str) -> None:
        self.id = identifier


def test_run_nightly_job_returns_task_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """The scheduler should yield the Celery task identifier."""

    dummy_result = DummyAsyncResult("test-task-id")

    def fake_delay() -> DummyAsyncResult:
        return dummy_result

    monkeypatch.setattr(scheduler.build_indices_task, "delay", fake_delay)

    task_id = scheduler.run_nightly_job()

    assert task_id == "test-task-id"
    assert isinstance(task_id, str)
