from datetime import datetime
from typing import Self

from pydantic import Field, NonNegativeInt, PositiveInt, model_validator

from asklearnly.schemas.base import ApiModel


class SyncFailure(ApiModel):
    source_id: PositiveInt
    message: str = Field(min_length=1)


class SyncSummary(ApiModel):
    failures: list[SyncFailure] = Field(default_factory=list)
    failed: NonNegativeInt
    indexed: NonNegativeInt
    updated: NonNegativeInt
    skipped: NonNegativeInt
    removed: NonNegativeInt
    completed_at: datetime

    @model_validator(mode="after")
    def validate_failure_count(self) -> Self:
        if self.failed != len(self.failures):
            raise ValueError("failed must equal the number of failure details")

        return self
