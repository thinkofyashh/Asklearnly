from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class DocumentPayload:
    source_id: int
    filename: str
    mime_type: str
    checksum_sha256: str
    content: bytes

    def __post_init__(self) -> None:
        if self.source_id <= 0:
            raise ValueError("source ID must be positive")

        if not self.filename.strip():
            raise ValueError("filename must not be empty")

        if not self.content:
            raise ValueError("document content must not be empty")


@dataclass(frozen=True, slots=True)
class LoadedPage:
    source_id: int
    page_number: int
    text: str
    checksum_sha256: str

    def __post_init__(self) -> None:
        if self.source_id <= 0:
            raise ValueError("source ID must be positive")

        if self.page_number <= 0:
            raise ValueError("page number must be positive")


@runtime_checkable
class DocumentLoader(Protocol):
    def load(self, document: DocumentPayload) -> tuple[LoadedPage, ...]:
        """Extract ordered pages from a document."""
        ...
