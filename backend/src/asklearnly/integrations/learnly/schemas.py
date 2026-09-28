from datetime import datetime
from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field, PositiveInt, StringConstraints, field_validator

from asklearnly.schemas.base import ApiModel

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

Sha256Checksum = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern=r"^[0-9a-fA-F]{64}$")
]


class LearnlyPublishedDocument(ApiModel):
    id: PositiveInt
    slug: NonEmptyText
    original_filename: NonEmptyText
    title: NonEmptyText
    topics: list[NonEmptyText] = Field(default_factory=list)
    mime_type: Literal["application/pdf"]
    checksum_sha256: Sha256Checksum
    size_bytes: PositiveInt
    preview_url: AnyHttpUrl
    download_url: AnyHttpUrl
    updated_at: datetime
    published_at: datetime
    page_count: PositiveInt

    @field_validator("checksum_sha256")
    @classmethod
    def normalize_checksum(cls, checksum: str) -> str:
        return checksum.lower()
