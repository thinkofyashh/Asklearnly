from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from asklearnly.schemas.sync import SyncSummary


def build_summary(**changes: object) -> SyncSummary:
    data: dict[str, object] = {
        "indexed": 2,
        "updated": 1,
        "skipped": 12,
        "removed": 0,
        "failed": 1,
        "failures": [
            {
                "source_id": 21,
                "message": "No searchable text was found in this PDF.",
            }
        ],
        "completed_at": datetime(2026, 9, 19, 8, 31, tzinfo=UTC),
    }
    data.update(changes)

    return SyncSummary.model_validate(data)


def test_sync_summary_accepts_valid_data() -> None:
    summary = build_summary()

    assert summary.failed == 1
    assert summary.failures[0].source_id == 21


def test_sync_summary_serializes_using_camel_case() -> None:
    payload = build_summary().model_dump(by_alias=True, mode="json")

    assert payload["failures"][0]["sourceId"] == 21
    assert "completedAt" in payload
    assert "completed_at" not in payload


def test_sync_summary_rejects_negative_counter() -> None:
    with pytest.raises(ValidationError):
        build_summary(indexed=-1)


def test_sync_summary_rejects_failure_count_mismatch() -> None:
    with pytest.raises(ValidationError):
        build_summary(failed=0)
